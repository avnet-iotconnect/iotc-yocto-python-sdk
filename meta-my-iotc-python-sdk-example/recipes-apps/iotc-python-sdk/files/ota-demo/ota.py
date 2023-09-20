import os
import tarfile
import shutil
from urllib.request import urlretrieve 
import json

class OTA:
    def __init__(self, sdk, app_paths):
        self.sdk = sdk
        self.app_paths = app_paths

    def ota_perform_upgrade(self,msg):
        print("\n--- firmware Command Message Received ---")
        print(json.dumps(msg))
        cmdType = None
        if msg != None and len(msg.items()) != 0:
            cmdType = msg["ct"] if msg["ct"] != None else None

        if cmdType != 1:
            self.sdk.sendOTAAckCmd(msg["ack"],4,"OTA FAILED, invalid payload")
            return

        payload_valid: bool = False
        data = msg

        if ("urls" in data) and len(data["urls"]) == 1:                
            if ("url" in data["urls"][0]) and ("fileName" in data["urls"][0]):
                if (data["urls"][0]["fileName"].endswith(".gz")):
                    payload_valid = True   

        if payload_valid is True:
            urls = data["urls"][0]
            self.sdk.sendOTAAckCmd(data["ack"],2,"downloading payload")
            
            # download tarball from url to download_dir
            url: str = urls["url"]
            download_filename: str = urls["fileName"]
            final_folder_dest:str = self.app_paths["main_dir"] + self.app_paths["tarball_download_dir"]
            if os.path.exists(final_folder_dest) == False:
                os.mkdir(final_folder_dest)
            urlretrieve(url, final_folder_dest + download_filename)

            self.sdk.sendOTAAckCmd(data["ack"],3,"payload downloaded")
            
            self.sdk._needs_exit = False
            self.ota_backup_primary()
            try:
                self.ota_extract_to_a_and_move_old_a_to_b(download_filename)
                self.sdk._needs_exit = True
            except:
                self.ota_restore_primary()
                self.sdk.sendOTAAckCmd(data["ack"],4,"OTA FAILED")
                self.sdk._needs_exit = False

            if self.sdk._needs_exit:
                self.ota_delete_primary_backup()
                self.sdk.sendOTAAckCmd(data["ack"],0,"OTA complete, restarting`")
                return


    def ota_extract_to_a_and_move_old_a_to_b(self,tarball_name:str):
        # extract tarball to new directory
        file = tarfile.open(self.app_paths["main_dir"] + self.app_paths["tarball_download_dir"] + tarball_name)
        file.extractall(self.app_paths["main_dir"] + self.app_paths["tarball_extract_dir"])
        file.close()

        # rm secondary dir
        path = self.app_paths["main_dir"] + self.app_paths["secondary_app_dir"]
        shutil.rmtree(path, ignore_errors=True)

        # move primary to secondary
        os.rename(self.app_paths["main_dir"] + self.app_paths["primary_app_dir"], self.app_paths["main_dir"] + self.app_paths["secondary_app_dir"])

        # copy extracted dir to primary dir
        src = self.app_paths["main_dir"] + self.app_paths["tarball_extract_dir"]
        dst = self.app_paths["main_dir"] + self.app_paths["primary_app_dir"]
        shutil.copytree(src, dst)

        # delete temp folders
        shutil.rmtree(self.app_paths["main_dir"] + self.app_paths["tarball_download_dir"], ignore_errors=True)
        shutil.rmtree(self.app_paths["main_dir"] + self.app_paths["tarball_extract_dir"], ignore_errors=True)

    def ota_backup_primary(self):
        src = self.app_paths["main_dir"] + self.app_paths["primary_app_dir"]
        dst = self.app_paths["main_dir"] + self.app_paths["primary_app_backup_folder_name"]
        shutil.copytree(src, dst)

    def ota_restore_primary(self):
        shutil.rmtree(self.app_paths["main_dir"] + self.app_paths["primary_app_dir"], ignore_errors=True)
        os.rename(self.app_paths["main_dir"] + self.app_paths["primary_app_backup_folder_name"], self.app_paths["main_dir"] + self.app_paths["primary_app_dir"])

    def ota_delete_primary_backup(self):
        shutil.rmtree(self.app_paths["main_dir"] + self.app_paths["primary_app_backup_folder_name"], ignore_errors=True)
