import json
from sqlite3 import connect

sys_status = ["error", "initializing", "waiting",
              "detecting", "controlling", "starting", "stopping", "manual"]

ECRARM_STATUS = {
    "status": sys_status[1],
    "Detector": {
        "ip": "",
        "connect": False,  # True or False
        "data": {
            "class": "none",
            "accord_x": 0,
            "accord_y": 0
        }
    },
    "Controller": {
        "ip": "",
        "connect": False,  # True or False
        "data": {
            "X_Axis": 0,
            "Y_Axis": 0,
            "Z_Axis": 0,
            "W_Axis": 0,
            "R_Axis": 0
        }
    },
    "Web": {
        "bridgeIp": "",
        "bridgeConnect": False,  # True or False
        "data": ""
    }
}


def SHOW_ECRARM_STATUS():
    print(
        f"\n>> Current Status : {json.dumps(ECRARM_STATUS,sort_keys=True,indent=4)}")
    return

# FROM: 데이터 업데이트 주체,str타입
# DATA: 업데이트되는 데이터, str타입으로 넣어주어야 하며,
# updateType이 connect일 경우에는 True / False만
# updateType이 data일 경우에는 JSON format으로 넣어주어야 함.
# ---
# updateType : 업데이트 타입, connect와 data로 나눠짐
# connect일 경우 연결 데이터만 업데이트, data일 경우 내부 데이터들을 업데이트


def UPDATE_ECRARM_STATUS(IP: str, FROM: str, UpdateType: str, DATA: str):
    if UpdateType == "connect":
        if FROM == "Controller":
            ECRARM_STATUS["Controller"]["ip"] = IP
            ECRARM_STATUS["Controller"]["connect"] = DATA
        elif FROM == "Detector":
            ECRARM_STATUS["Detector"]["ip"] = IP
            ECRARM_STATUS["Detector"]["connect"] = DATA
        elif FROM == "Web":
            ECRARM_STATUS["Web"]["bridgeIp"] = IP
            ECRARM_STATUS["Web"]["bridgeConnect"] = DATA
        else:
            print(f'no match FROM')
            return

        print(
            f'\n>> {IP} | connection status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
    elif UpdateType == "data":
        if FROM == "Controller":
            ECRARM_STATUS["Controller"]["data"] = DATA
        elif FROM == "Detector":
            ECRARM_STATUS["Detector"]["data"] = DATA
        elif FROM == "Web":
            ECRARM_STATUS["Web"]["data"] = DATA
        else:
            print(f'no match FROM')
            return

        print(
            f'\n>> {IP} | data status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
    else:
        print(f'no match UpdateType')

    # SHOW_ECRARM_STATUS()
    return


def SENDING_FORMAT(ECRARM_STATUS):
    data = json.dumps({
        "status": ECRARM_STATUS["status"],
        "Detector": { 
            "connect": ECRARM_STATUS["Detector"]["connect"],  # True or False
            "data": {
                "class": ECRARM_STATUS["Detector"]["data"]["class"],
                "accord_x": ECRARM_STATUS["Detector"]["data"]["accord_x"],
                "accord_y": ECRARM_STATUS["Detector"]["data"]["accord_y"]
            }
        },
        "Controller": {
            "connect": ECRARM_STATUS["Controller"]["connect"],  # True or False
            "data": {
                "X_Axis": ECRARM_STATUS["Controller"]["data"]["X_Axis"],
                "Y_Axis": ECRARM_STATUS["Controller"]["data"]["Y_Axis"],
                "Z_Axis": ECRARM_STATUS["Controller"]["data"]["Z_Axis"],
                "W_Axis": ECRARM_STATUS["Controller"]["data"]["W_Axis"],
                "R_Axis": ECRARM_STATUS["Controller"]["data"]["R_Axis"]
            }
        },
        "Web": {
            "bridgeConnect": ECRARM_STATUS["Web"]["bridgeConnect"],  # True or False
            "data": ECRARM_STATUS["Web"]["data"]
        }

    })
    return data


def DISCONNECT_AND_STATUS_UPDATE(IP):
    if ECRARM_STATUS["Controller"]["ip"] == IP:
        ECRARM_STATUS["Controller"]["ip"] = ""
        ECRARM_STATUS["Controller"]["connect"] = False
        print(">> Controller disconnected")
    elif ECRARM_STATUS["Detector"]["ip"] == IP:
        ECRARM_STATUS["Detector"]["ip"] = ""
        ECRARM_STATUS["Detector"]["connect"] = False
        print(">> Detector disconnected")
    elif ECRARM_STATUS["Web"]["bridgeIp"] == IP:
        ECRARM_STATUS["Web"]["bridgeIp"] = ""
        ECRARM_STATUS["Web"]["bridgeConnect"] = False
        print(">> websocket client")
    SHOW_ECRARM_STATUS()
    return


if (__name__ == "__main__"):
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
    UPDATE_ECRARM_STATUS("127.0.0.1", "Detector", "connect", False)
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
