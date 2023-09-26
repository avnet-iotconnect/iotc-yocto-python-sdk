import os
import tarfile
import shutil
from urllib.request import urlretrieve 
import json
from iotconnect import IoTConnectSDK

# to pass global from main.py
app_paths: dict = None

def ota_perform_upgrade(self,msg):
    global app_paths
    print("\n--- firmware Command Message Received ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if msg["ct"] != None else None

        if cmdType != 1:
            self.sendOTAAckCmd(msg["ack"],4,"OTA FAILED, invalid payload")
            return

    payload_valid: bool = False
    data = msg

    if ("urls" in data) and len(data["urls"]) == 1:                
        if ("url" in data["urls"][0]) and ("fileName" in data["urls"][0]):
            if (data["urls"][0]["fileName"].endswith(".gz")):
                payload_valid = True   

    if payload_valid is True:
        urls = data["urls"][0]
        self.sendOTAAckCmd(data["ack"],2,"downloading payload")
        
        # download tarball from url to download_dir
        url: str = urls["url"]
        download_filename: str = urls["fileName"]
        final_folder_dest:str = app_paths["main_dir"] + app_paths["tarball_download_dir"]
        if os.path.exists(final_folder_dest) == False:
            os.mkdir(final_folder_dest)
        urlretrieve(url, final_folder_dest + download_filename)

        self.sendOTAAckCmd(data["ack"],3,"payload downloaded")
        
        self._needs_exit = False
        ota_backup_primary()
        try:
            ota_extract_to_a_and_move_old_a_to_b(download_filename)
            self._needs_exit = True
        except:
            ota_restore_primary()
            self.sendOTAAckCmd(data["ack"],4,"OTA FAILED")
            self._needs_exit = False

        if self._needs_exit:
            ota_delete_primary_backup()
            self.sendOTAAckCmd(data["ack"],0,"OTA complete, restarting`")
            return
        
    self.sendOTAAckCmd(msg["ack"],4,"OTA FAILED, invalid payload")


def ota_extract_to_a_and_move_old_a_to_b(tarball_name:str):
    global app_paths
    # extract tarball to new directory
    file = tarfile.open(app_paths["main_dir"] + app_paths["tarball_download_dir"] + tarball_name)
    file.extractall(app_paths["main_dir"] + app_paths["tarball_extract_dir"])
    file.close()

    # rm secondary dir
    path = app_paths["main_dir"] + app_paths["secondary_app_dir"]
    shutil.rmtree(path, ignore_errors=True)

    # move primary to secondary
    os.rename(app_paths["main_dir"] + app_paths["primary_app_dir"], app_paths["main_dir"] + app_paths["secondary_app_dir"])

    # copy extracted dir to primary dir
    src = app_paths["main_dir"] + app_paths["tarball_extract_dir"]
    dst = app_paths["main_dir"] + app_paths["primary_app_dir"]
    shutil.copytree(src, dst)

    # delete temp folders
    shutil.rmtree(app_paths["main_dir"] + app_paths["tarball_download_dir"], ignore_errors=True)
    shutil.rmtree(app_paths["main_dir"] + app_paths["tarball_extract_dir"], ignore_errors=True)

def ota_backup_primary():
    global app_paths
    src = app_paths["main_dir"] + app_paths["primary_app_dir"]
    dst = app_paths["main_dir"] + app_paths["primary_app_backup_folder_name"]
    shutil.copytree(src, dst)

def ota_restore_primary():
    global app_paths
    shutil.rmtree(app_paths["main_dir"] + app_paths["primary_app_dir"], ignore_errors=True)
    os.rename(app_paths["main_dir"] + app_paths["primary_app_backup_folder_name"], app_paths["main_dir"] + app_paths["primary_app_dir"])

def ota_delete_primary_backup():
    global app_paths
    shutil.rmtree(app_paths["main_dir"] + app_paths["primary_app_backup_folder_name"], ignore_errors=True)



# bind ota logic to the SDK's callback
IoTConnectSDK._listner_ota_callback = ota_perform_upgrade