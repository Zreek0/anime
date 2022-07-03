import sys
import logging
import importlib
from pathlib import Path

def load_plugins(plugin_name):
    if plugin_name.startswith("__"):
    	pass
    else:
    	path = Path(f"main/plugins/{plugin_name}.py")
    	name = "main.plugins.{}".format(plugin_name)
    	spec = importlib.util.spec_from_file_location(name, path)
    	load = importlib.util.module_from_spec(spec)
    	load.logger = logging.getLogger(plugin_name)
    	spec.loader.exec_module(load)
    	sys.modules["main.plugins." + plugin_name] = load
    	logging.info("main has Imported " + plugin_name)
