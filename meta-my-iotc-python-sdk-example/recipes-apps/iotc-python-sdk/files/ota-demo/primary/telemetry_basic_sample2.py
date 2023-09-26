"""
  ******************************************************************************
  * @file   : iotconnect-sdk-1.0-firmware-python_msg-2_1.py
  * @author : Softweb Solutions An Avnet Company
  * @modify : 02-January-2023
  * @brief  : Firmware part for Python SDK 1.0
  ******************************************************************************
"""

"""
 * Hope you have installed the Python SDK v1.0 as guided in README.md file or from documentation portal. 
 * Import the IoTConnect SDK package and other required packages
"""

# OTA this sample can perform OTA updates, requirements of the OTA payload
# OTA payload must be a single file of file extension .tar.gz
# OTA update version of the main .py file must be called the same as a previous version otherwise it will not load

app_version: str = "2.0"

import sys
import json
import time
import threading
import random

# if iotconnect module is not installed then use the local one
# note: this is if you are running the sample in the git repository folder
try:
    from iotconnect import IoTConnectSDK
except:
    sys.path.append("iotconnect-sdk-1.0")
    from iotconnect import IoTConnectSDK

from datetime import datetime
import os

import tarfile
import shutil
import urllib.request, json

import credentials
UniqueId: str = credentials.UniqueId 
sdk_identity: str = credentials.sdk_identity
SdkOptions: dict = credentials.SdkOptions

app_paths: dict = {
    "app_name": None,
    "primary_app_dir": None,
    "secondary_app_dir": None,
    "tarball_download_dir": None,
    "tarball_extract_dir": None,
    "module_name": None,
    "main_dir": None
}



Sdk=None
interval = 30
directmethodlist={}
ACKdirect=[]
device_list=[]



"""
 * Type    : Callback Function "DeviceCallback()"
 * Usage   : Firmware will receive commands from cloud. You can manage your business logic as per received command.
 * Input   :  
 * Output  : Receive device command, firmware command and other device initialize error response 
"""

def DeviceCallback(msg):
    global Sdk
    print("\n--- Command Message Received in Firmware ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if "ct"in msg else None
    # Other Command
    if cmdType == 0:
        """
        * Type    : Public Method "sendAck()"
        * Usage   : Send device command received acknowledgment to cloud
        * 
        * - status Type
        *     st = 6; // Device command Ack status 
        *     st = 4; // Failed Ack
        * - Message Type
        *     msgType = 5; // for "0x01" device command 
        """
        data=msg
        if data != None:
            #print(data)
            if "id" in data:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"successful",data["id"])  #fail=4,executed= 5,success=7,6=executed ack
            else:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"successful") #fail=4,executed= 5,success=7,6=executed ack
    else:
        print("rule command",msg)



def DeviceConnectionCallback(msg):  
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if msg["ct"] != None else None
    #connection status
    if cmdType == 116:
        #Device connection status e.g. data["command"] = true(connected) or false(disconnected)
        print(json.dumps(msg))

"""
 * Type    : Public Method "UpdateTwin()"
 * Usage   : Update the twin reported property
 * Input   : Desired property "key" and Desired property "value"
 * Output  : 
"""
# key = "<< Desired property key >>"; // Desired property key received from Twin callback message
# value = "<< Desired Property value >>"; // Value of respective desired property
# Sdk.UpdateTwin(key,value)

"""
 * Type    : Callback Function "TwinUpdateCallback()"
 * Usage   : Manage twin properties as per business logic to update the twin reported property
 * Input   : 
 * Output  : Receive twin Desired and twin Reported properties
"""
def TwinUpdateCallback(msg):
    global Sdk
    if msg:
        print("--- Twin Message Received ---")
        print(json.dumps(msg))
        if ("desired" in msg) and ("reported" not in msg):
            for j in msg["desired"]:
                if ("version" not in j) and ("uniqueId" not in j):
                    Sdk.UpdateTwin(j,msg["desired"][j])

"""
 * Type    : Public data Method "SendData()"
 * Usage   : To publish the data on cloud D2C 
 * Input   : Predefined data object 
 * Output  : 
"""
def sendBackToSDK(sdk, dataArray):
    sdk.SendData(dataArray)
    time.sleep(interval)

def DirectMethodCallback1(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"succeeded"}
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

def DirectMethodCallback(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"fail"}
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

def DeviceChangCallback(msg):
    print(msg)

def InitCallback(response):
    print(response)

def delete_child_callback(msg):
    print(msg)

def attributeDetails(data):
    print ("attribute received in firmware")
    print (data)
    

def init_sdk():
    global sdk_identity,SdkOptions,Sdk,ACKdirect,device_list
    try:
        Sdk = IoTConnectSDK(UniqueId,sdk_identity,SdkOptions,DeviceConnectionCallback)
        
        # do not modify - changes would break OTA behaviour
        import ota
        ota_obj = ota.OTA(Sdk,app_paths)
        Sdk.onOTACommand(ota_obj.ota_perform_upgrade)
        # do not modify - end

        Sdk.onDeviceCommand(DeviceCallback)
        Sdk.onTwinChangeCommand(TwinUpdateCallback)
        Sdk.onDeviceChangeCommand(DeviceChangCallback)
        Sdk.getTwins()
        device_list=Sdk.Getdevice()
    except Exception as ex:
        print(ex.message)


def generate_dummy_payload():
    data = {
    "sw_version": app_version,
    "temperature":random.randint(30, 50),
    "long1":random.randint(6000, 9000),
    "integer1": random.randint(100, 200),
    "decimal1":random.uniform(10.5, 75.5),
    "date1":datetime.utcnow().strftime("%Y-%m-%d"),
    "time1":"11:55:22",
    "bit1":1,
    "string1":"red",
    "datetime1":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "gyro": {
        'bit1':0,
        'boolean1': True,
        'date1': datetime.utcnow().strftime("%Y-%m-%d"),
        "datetime1": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "decimal1":random.uniform(10.5, 75.5),
        "integer1":random.randint(60, 600),
        "latlong1":[random.uniform(10.5, 75.5),random.uniform(10.5, 75.5)],
        "long1":random.randint(60, 600000),
        "string1":"green",
        "time1":"11:44:22",
        "temperature":random.randint(50, 90)
        }
        }
    dObj = [{
        "uniqueId": UniqueId,
        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "data": data
    }]

    return dObj

def generate_weather_payload():

    with urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?latitude=51.45&longitude=-2.59&current_weather=true") as url:
        data = json.load(url)
        print(data)

    to_send = {
    "sw_version": app_version,
    'latitude': data["latitude"],
    'longitude': data["longitude"],
    'timezone': data["timezone"],
    "temperature":data["current_weather"]["temperature"],
    'elevation': data["elevation"],
    'windspeed': data["current_weather"]["windspeed"],
    'winddirection': data["current_weather"]["winddirection"],
    'weathercode': data["current_weather"]["weathercode"],
    'is_day': data["current_weather"]["is_day"],
    'time': data["current_weather"]["time"],
    }

    dObj = [{
        "uniqueId": UniqueId,
        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "data": to_send
    }]

    return dObj

def main(app_paths_in:dict):

    global app_paths 
    app_paths = app_paths_in

    print("basic sample version " + app_version)
    init_sdk()

    try:
        while Sdk._needs_exit == False:
            sendBackToSDK(Sdk, generate_weather_payload())
    except KeyboardInterrupt:
        print ("Keyboard Interrupt Exception")
        # os.execl(sys.executable, sys.executable, *sys.argv)
        os.abort()
        # sys.exit(0)
    except Exception as ex:
        print(ex.message)
        sys.exit(0)

if __name__ == "__main__":
    generate_weather_payload()
    print("execute from main.py")
   # main()
