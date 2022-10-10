import importlib
import os
import glob
import re

# Register event listeners

def register(path: str):
    path_parts = re.split(r"\\|\/", path)
    if path_parts[-1] == '__init__':
        return

    module_name = '.'.join(path_parts)
    importlib.import_module(module_name)

    print(f"[Slack bot] event listener imported: {module_name}")


modules = glob.glob(f"{os.path.dirname(__file__)}/**/*.py", recursive=True)
for module in modules:
    register(re.sub(r".+(?=bot(?!_))|\.py", '', module))
