from ctypes import cdll, c_char_p
from aiohttp import web
import threading
import platform
import asyncio
import aiohttp
import pickle
import shutil
import socket
import json
import sys
import os

from comfy.cli_args import args
import server

CWD = os.path.abspath(os.path.dirname(__file__))
STATUS_FILE = os.path.join(CWD, "status.dat")

# HOST = "https://comfyplus.run"
HOST = "http://43.134.68.113:8001"

frpc_worker = None
if sys.platform == "win32":
    frpc = cdll.LoadLibrary(os.path.join(CWD, "libs", "win32", "libfrpc.dll"))
elif sys.platform == "linux":
    frpc = cdll.LoadLibrary(os.path.join(CWD, "libs", "linux", "libfrpc.so"))
elif sys.platform == "darwin":
    frpc = cdll.LoadLibrary(os.path.join(CWD, "libs", "darwin", platform.processor(), "libfrpc.so"))
else:
    frpc = None

@server.PromptServer.instance.routes.post("/comfyplus_anywhere/connect")
async def _(request):        
    body = await request.json()
    token = body.get("token", None)
    _, resp = await start_connection(token)    
    return web.json_response(resp)    


@server.PromptServer.instance.routes.post("/comfyplus_anywhere/disconnect")
async def _(request):
    global frpc_worker

    if frpc_worker is None or not os.path.exists(STATUS_FILE):
        return web.json_response({"code": 0, "message": "not connected"})

    data = pickle.load(open(STATUS_FILE, "rb"))
    token, url = data["token"], data["url"]
    
    async with aiohttp.ClientSession(HOST) as session:
        async with session.post("/api/v1/instance/connect/cancel", json={"token": token}) as resp:
            resp = await resp.json()
        
        if resp["code"] != 0:
            return web.json_response(resp)  

    frpc.Stop()
    
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)
    
    return web.json_response({"code": 0})


@server.PromptServer.instance.routes.post("/comfyplus_anywhere/status")
async def _(request):
    if frpc_worker is None or not os.path.exists(STATUS_FILE):
        return web.json_response({"code": -1, "message": "not connected"})
    
    data = pickle.load(open(STATUS_FILE, "rb"))
    flag, resp = await check_connection(data["url"])
    if not flag:
        return web.json_response(resp)
    
    return web.json_response({"code": 0, "data": {"url": data["url"]}})


@server.PromptServer.instance.routes.post("/comfyplus_anywhere/check")
async def _(request):
    return web.json_response({"code": 0})


async def start_connection(token):
    global frpc_worker

    # 1.check parameters
    if not token:
        return False, {"code": -1, "message": "The parameter is required: token"}
    
    # 2.request connection
    async with aiohttp.ClientSession(HOST) as session:
        async with session.post("/api/v1/instance/connect/request", json={"token": token, "localIp": "127.0.0.1", "localPort": args.port}) as resp:
            resp = await resp.json()
        
        if resp["code"] != 0:
            return False, resp
    
    # 3.start frpc
    if frpc is None:
        return False,{"code": -2, "message": f"Not support: {sys.platform}"}
    
    def start_handler(config):    
        result = frpc.Start(config.encode())
        print(result)
    
    frpc_worker = threading.Thread(target=start_handler, args=(resp["data"]["config"],), name="frpc", daemon=True)
    frpc_worker.start()

    # 4.check it
    await asyncio.sleep(1)
    url = resp["data"]["url"]
    flag, resp = await check_connection(url)
    if not flag:
        return False, resp
        
    # 5.complete!
    async with aiohttp.ClientSession(HOST) as session:
        async with session.post("/api/v1/instance/connect/complete", json={"token": token, "localIp": "127.0.0.1", "localPort": args.port}) as resp:
            resp = await resp.json()
        
        if resp["code"] != 0:
            frpc.Stop()
            return False, resp
    
    # 6.save
    pickle.dump({"token": token, "url": url}, open(STATUS_FILE, "wb"))
    
    return True, {"code": 0, "data": {"url": url}}


async def check_connection(url):
    for retry in range(5, -1, -1):
        try:
            async with aiohttp.ClientSession(url) as session:
                async with session.post("/api/comfyplus_anywhere/check", json={}) as resp:
                    resp = await resp.json()
                
                if resp["code"] != 0:
                    return False, resp
        except Exception as ex:
            if retry <= 0:
                frpc.Stop()
                return False, {"code": -3, "message": "Check the connection: failed"}
            await asyncio.sleep(1)    
    return True, None


@server.PromptServer.instance.routes.post("/comfyplus_anywhere/workflow/download")
async def _(request):        
    body = await request.json()

    workflow_id = body.get("workflow_id", None)
    if not workflow_id:
        return {"code": -1, "message": f"The paramater is required: {workflow_id}"}
    
    if not os.path.exists(STATUS_FILE):
        return {"code": -1, "message": "Please connect to the server"}
    token = pickle.load(open(STATUS_FILE, "rb"))["token"]
    
    async with aiohttp.ClientSession(HOST) as session:
        async with session.get(f"/api/v1/instance/workflow/download?workflow_id={workflow_id}", headers={"Authorization": token}) as resp:
            if resp.status != 200:
                return web.Response(status=resp.status)

            resp = await resp.read()

    return web.Response(body=resp)


@server.PromptServer.instance.routes.post("/comfyplus_anywhere/workflow/save")
async def _(request):        
    body = await request.json()

    workflow_id = body.get("workflow_id", None)
    if not workflow_id:
        return {"code": -1, "message": f"The paramater is required: workflow_id"}
    
    content = body.get("content", None)
    if not content:
        return {"code": -1, "message": f"The paramater is required: content"}

    if not os.path.exists(STATUS_FILE):
        return {"code": -1, "message": "Please connect to the server"}
    token = pickle.load(open(STATUS_FILE, "rb"))["token"]
    
    async with aiohttp.ClientSession(HOST) as session:
        async with session.post(f"/api/v1/instance/workflow/save?workflow_id={workflow_id}", data=json.dumps(content).encode("utf-8"), headers={"Authorization": token}) as resp:
            if resp.status != 200:
                return web.Response(status=resp.status)

            resp = await resp.read()
                
    return web.Response(body=resp)


if os.path.exists(STATUS_FILE):
    async def main():        
        while True:
            try:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.settimeout(1)
                tcp_socket.connect(("127.0.0.1", int(args.port)))
                tcp_socket.close()
                break
            except Exception as ex:
                await asyncio.sleep(1)
        await start_connection(pickle.load(open(STATUS_FILE, "rb"))["token"])
    
    loop = asyncio.get_event_loop()
    loop.create_task(main())