import { ComfyDialog, $el } from "../../scripts/ui.js";
import { ComfyApp, app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const CONNECT_TEXT = "Connect";
const DISCONNECT_TEXT = "Disonnect";

class ConnectDialog extends ComfyDialog {
    constructor(){
        super();
        
        this.element = $el("div.comfy-modal", { parent: document.body }, [
            $el("table.comfy-modal-content.comfy-table", [
                $el(
                    "caption",
                    { textContent: `Connect to ComfyPlus` },
                    $el("button.comfy-btn", {
                      type: "button",
                      textContent: "×",
                      onclick: () => this.hide()
                    })
                ),

                $el("tbody", [
                    $el("tr", [
                        $el("td", [$el("label", {textContent: "Token"})]),
                        $el("td", [$el("input", {id: "ComfyPlus_Anywhere_Token"})])
                    ]),
                    $el("tr", { align: "center" }, [
                        $el("td", { colSpan: 2 }, [
                            $el("button", { textContent: "Connect", type: "button", onclick: () => this.handleSubmit()})
                        ])
                    ]),
                ]),    
            ])
        ]);
    }

    async handleSubmit() {
        const token = document.getElementById('ComfyPlus_Anywhere_Token').value.trim();
        if(token.length <= 0) return alert("Token is required!");

        let resp = await api.fetchApi("/comfyplus_anywhere/connect", {
            method: "POST",
            body: JSON.stringify({token}),
        });

        resp = await resp.json();
        if(resp.code != 0) return;

        this.hide();

        document.getElementById("ComfyPlus_Anywhere_Connect_Button").innerText = DISCONNECT_TEXT;

        let element = document.getElementById("ComfyPlus_Anywhere_Connect_Url");
        if(element) {
            element.href = resp.data.url;
            element.innerText = resp.data.url;
        }
    }

    show() {
        this.element.style.display = "block";
		this.element.style.zIndex = 10001;
	}

    hide() {
        this.element.style.display = "none";
    }
}

app.registerExtension({
	name: "ComfyPlus_Anywhere",

    commands: [
        {
            id: "ComfyPlus.Save",
            icon: 'pi pi-save',
            label: 'Save Workflow',
            menubarLabel: 'Save',
            function: () => {                
                save_workflow();
            }
        }
    ],

    keybindings: [
        {
            commandId: "ComfyPlus.Save",
            targetSelector: "#graph-canvas",
            combo: {key: "S", ctrl: true, alt: false, shift: true}
        }
    ],

    setup() {
        this.is_connected = false;
        this.url = "";

        this.settings = app.ui.settings;
        this.connect_view = new ConnectDialog();

        this.settings.addSetting({
            id: "ComfyPlus_Anywhere.Connect",
            category: ["ComfyPlus", "Connect"],
            name: "Connect to ComfyPlus",
            type: () => $el("button", {
                id: "ComfyPlus_Anywhere_Connect_Button",
                textContent: this.is_connected ? DISCONNECT_TEXT : CONNECT_TEXT,
                type: "button",
                onclick: async () => {
                    const button = document.getElementById("ComfyPlus_Anywhere_Connect_Button");
                    
                    let text = button.innerText;
                    if(text == CONNECT_TEXT) this.connect_view.show();
                    else if(text == DISCONNECT_TEXT) {
                        let resp = await api.fetchApi("/comfyplus_anywhere/disconnect", {method: "POST", body: "{}"});
                        resp = await resp.json();
                        this.check_status(resp);
                    }
                }
            }),
        });

        this.settings.addSetting({
            id: "ComfyPlus_Anywhere.Connect.Url",
            category: ["ComfyPlus", "Connect", "Url"],
            name: "The remote url",
            type: () => $el("a", {
                    id: "ComfyPlus_Anywhere_Connect_Url",
                    textContent: this.url,
                    href: this.url,
                    target: "_blank"
                })
            },
        );

        this.check_status();
        this.load_workflow();
    },

    registerCustomNodes(){

    },

	nodeCreated(node, app) {
		
    },
    
    async check_status(resp) {
        if(resp == null) {
            resp = await api.fetchApi("/comfyplus_anywhere/status", { method: "POST", body: "{}"});
            resp = await resp.json();
        }

        this.is_connected = resp.code == 0;
        this.url = this.is_connected ? resp["data"]["url"] : "";
        
        let button = document.getElementById("ComfyPlus_Anywhere_Connect_Button");
        if(button) button.innerText = this.is_connected ? DISCONNECT_TEXT : CONNECT_TEXT;

        let element = document.getElementById("ComfyPlus_Anywhere_Connect_Url");
        if(element) {
            element.href = this.url;
            element.innerText = this.url;
        }
    },

    async load_workflow() {
        let params = new URLSearchParams(location.search);
        if(!params.has("workflow_id")) return;

        let workflow_id = params.get("workflow_id");
        let resp = await api.fetchApi("/comfyplus_anywhere/workflow/download", {method: "POST", body: JSON.stringify({workflow_id})});
        if(resp.status == 201) return await app.loadGraphData();
        if(resp.status == 200) {
            let workflow = await resp.json();
            await app.loadGraphData(workflow);
        }
    }
})

async function save_workflow() {
    let params = new URLSearchParams(location.search);
    if(!params.has("workflow_id")) return;

    let workflow_id = params.get("workflow_id");
    if(!workflow_id) return;

    const p = await app.graphToPrompt();
    let resp = await api.fetchApi("/comfyplus_anywhere/workflow/save", {method: "POST", body: JSON.stringify({workflow_id, content: p.workflow})});    
    if(resp.status != 200) return app.extensionManager.toast.add({severity: "error", summary: "Error", detail: "保存失败，请稍后重试", life: 3000});
    
    let result = await resp.json();
    if(result.code != 0) return app.extensionManager.toast.add({severity: "error", summary: "Error", detail: result.message, life: 3000});

    app.extensionManager.toast.add({severity: "success", summary: "Success", detail: "保存成功", life: 3000});
}