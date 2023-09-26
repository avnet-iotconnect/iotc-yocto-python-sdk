#!/usr/bin/python3
import os
import sys
from importlib import import_module, reload

# import both so the ota logic is bound to the SDK's ota handler, any files using IoTConnectSDK will now call the logic from ota during OTA events
from iotconnect import IoTConnectSDK
import ota


# this the runner of the demo, used to show A/B updates
# the actual code lives inside a folder called `primary_app_dir`
# should it fail, an attempt will be made to run the previous code in `secondary_app_dir`

# this sample can perform OTA updates, requirements of the OTA payload
# OTA payload must be a single file of file extension .tar.gz
# the updated application .py file  must be called the same as a previous version otherwise it will not load, refer to app_name

# Stuff to change
app_name: str = "telemetry_basic_sample.py"
primary_app_dir: str = "/primary/"
secondary_app_dir: str = "/secondary/"
tarball_download_dir = "/.temp_ota/"
tarball_extract_dir: str = "/.temp_extracted/"
primary_backup_extension:str = ".backup"

module_name:str = app_name.replace(".py","")
main_dir: str = os.path.dirname(__file__)
primary_app_backup_folder_name:str = primary_app_dir.rstrip("/") + primary_backup_extension


app_paths: dict = {
    "app_name": app_name,
    "primary_app_dir": primary_app_dir,
    "secondary_app_dir": secondary_app_dir,
    "tarball_download_dir": tarball_download_dir,
    "tarball_extract_dir": tarball_extract_dir,
    "module_name": module_name,
    "main_dir": main_dir,
    "primary_app_backup_folder_name" : primary_app_backup_folder_name
}

# assign app paths to ota handler
ota.app_paths = app_paths

def run_app(to_run_path: str):
    try:
        print("Running app on "+ to_run_path)

        module_path: str = to_run_path.replace(app_name,"")
        sys.path.append(module_path)
        module = import_module(module_name)
        reload(module)
        module.main()
    except Exception as ex:
        sys.path.remove(module_path)
        print("App failed")
        print(str(ex))
        raise


if __name__ == "__main__":

    secondary_exists: bool = False
    secondary_path: str = main_dir + secondary_app_dir + app_name    
    if os.path.exists(secondary_path):
        secondary_exists = True

    primary_exists: bool = False
    primary_path: str = main_dir + primary_app_dir + app_name
    if os.path.exists(primary_path):
        primary_exists = True

    if primary_exists and secondary_exists:
        print("Primary and Secondary exist, running")
        try:
            run_app(primary_path)
        except Exception:
            print("Primary app has failed trying backup")
            run_app(secondary_path)

    elif primary_exists:
        print("Only Primary exists, running")
        run_app(primary_path)

    elif secondary_exists:
        print("Only Secondary exists, running")
        run_app(secondary_path)
    
    else:
        print("No valid application exists to run")
