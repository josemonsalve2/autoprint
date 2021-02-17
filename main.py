from config.params import ap_params
import json
import os
from config.debug import log
from folder_watcher.fwatcher import Watcher



""" Read parameters from JSON file CONFIG_FILE on the root folder
"""
def params_reader():
    if os.path.exists(ap_params["CONFIG_FILE"]):
        log.info(f"Using configuration file {ap_params['CONFIG_FILE']}")
        try:
            with open(ap_params["CONFIG_FILE"]) as f:
                params = json.load(f)
                # Iterate over params and search in JSON config file
                for key, val in ap_params.items():
                    if key in params[0]:
                        ap_params[key] = params[0][key]
                        log.info(f"Setting {key} = {params[0][key]}")

        except Exception as e:
            log.error(f"ERROR When opening Config file {ap_params['CONFIG_FILE']} \n {str(e)}")
    else:
        log.info("Configuration file not found. Using default values")

if __name__ == "__main__":
    params_reader()
    watch = Watcher()
    watch.create_observers()
    watch.run()
