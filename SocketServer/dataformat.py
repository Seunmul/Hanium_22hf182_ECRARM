import json
from sqlite3 import connect

sys_status = ["error", "initializing", "waiting",
              "detecting", "controlling", "starting", "stopping", "manual"]

ECRARM_STATUS = {
    "status": sys_status[1],
    "ip": "",
    "from": "Web",  # Rpi,Tx2,Web
    "Detector": {
        "connect": False,  # True or False
        "data": {
            "class": "none",
            "x": 0,
            "y": 0
        }
    },
    "Controller": {
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
        "bridgeConnect": False,  # True or False
        "command": ""
    }
}

# FROM: 데이터 업데이트 주체,str타입
# DATA: 업데이트되는 데이터, str타입으로 넣어주어야 하며,
# updateType이 connect일 경우에는 True / False만
# updateType이 data일 경우에는 JSON format으로 넣어주어야 함.
# ---
# updateType : 업데이트 타입, connect와 data로 나눠짐
# connect일 경우 연결 데이터만 업데이트, data일 경우 내부 데이터들을 업데이트
#


def UPDATE_ECRARM_STATUS(FROM: str, UpdateType: str, DATA: str):
    update = True
    if UpdateType == "connect":
        if FROM == "Controller":
            ECRARM_STATUS["Controller"]["connect"] = DATA
        elif FROM == "Detector":
            ECRARM_STATUS["Detector"]["connect"] = DATA
        elif FROM == "Web":
            ECRARM_STATUS["Web"]["connect"] = DATA
        else:
            print(f'no match FROM')
            return
        print(
            f'>> connection status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
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
        print(f'>> data status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
    else:
        print(f'no match UpdateType')
    return


if (__name__ == "__main__"):
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
    UPDATE_ECRARM_STATUS("Detector", "connect", False)
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
