import importlib
import shutil
import os

from .server import *

version =  "v0.0.1"
print(f"### Loading: ComfyPlus_Anywhere ({version})")

WEB_DIRECTORY = "./web"
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

