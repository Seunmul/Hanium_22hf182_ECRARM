import json

sys_status = ["error", "initializing", "waiting",
              "detecting", "controlling", "starting", "stopping", "manual"]
web_client_ip_list = []

ECRARM_STATUS = {
    "status": sys_status[1],
    "Detector": {
        "ip": "",
        "connect": False,  # True or False
        "data": {
            "class": "none",
            "x": "0",
            "y": "0"
        }
    },
    "Controller": {
        "ip": "",
        "connect": False,  # True or False
        "data": {
            "X_Axis": "0",
            "Y_Axis": "0",
            "Z_Axis": "0",
            "W_Axis": "0",
            "R_Axis": "0"
        }
    },
    "Web": {
        "bridgeIp": "",
        "bridgeConnect": False,  # True or False
        "data": ""
    }
}


def SEND_STATUS(ECRARM_STATUS: dict):
    data = json.dumps({
        "status": ECRARM_STATUS["status"],
        "Detector": {
            "connect": ECRARM_STATUS["Detector"]["connect"],  # True or False
            "data": {
                "class": ECRARM_STATUS["Detector"]["data"]["class"],
                "x": ECRARM_STATUS["Detector"]["data"]["x"],
                "y": ECRARM_STATUS["Detector"]["data"]["y"]
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
            # True or False
            "bridgeConnect": ECRARM_STATUS["Web"]["bridgeConnect"],
            "data": ECRARM_STATUS["Web"]["data"]
        }
    })
    return data


def SHOW_ECRARM_STATUS(ECRARM_STATUS: dict):
    print(
        f"\n>> Current Status : {json.dumps(ECRARM_STATUS,sort_keys=True,indent=4)}")
    return


def UPDATE_SYS_STATUS(ECRARM_STATUS: dict, updatingStatus):
    connection_status = ECRARM_STATUS["Controller"]["connect"] and ECRARM_STATUS[
        "Detector"]["connect"] and ECRARM_STATUS["Web"]["bridgeConnect"]
    # print(updatingStatus)
    if (not connection_status):
        ECRARM_STATUS["status"] = sys_status[1]
        print('>> [STATUS] initializing program ....')
    else:
        ECRARM_STATUS["status"] = "waiting"
        if (updatingStatus == "starting"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] starting!!!!')

        elif (updatingStatus == "detecting"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] detecting ....')

        elif (updatingStatus == "detecting_finished"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] detecting finished')

        elif (updatingStatus == "controlling"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] controlling arm ....')

        elif (updatingStatus == "controlling_finished"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] controlling finished')

        elif (updatingStatus == "stopping"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] stopping')
        
        elif (updatingStatus == "manual"):
            ECRARM_STATUS["status"] = updatingStatus
            print('>> [STATUS] manual controlling')
        
        else:
            print('>> [STATUS] waiting web interface command ....')
    return

# ECRARM_STATUS : ??????????????? ?????????
# IP : ????????? ??????
# FROM: ????????? ???????????? ??????,str??????
# DATA: ?????????????????? ?????????, str???????????? ??????????????? ??????,
# updateType??? connect??? ???????????? True / False???
# updateType??? data??? ???????????? JSON format?????? ??????????????? ???.
# ---
# updateType : ???????????? ??????, connect??? data??? ?????????
# connect??? ?????? ?????? ???????????? ????????????, data??? ?????? ?????? ??????????????? ????????????


def UPDATE_ECRARM_STATUS(ECRARM_STATUS: dict, IP: str, FROM: str, TYPE: str,
                         DATA: str, updatingStatus: str = sys_status[1]):
    if TYPE == "connect":
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
            # f'\n>> {IP} | connection status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
            f'\n>> {IP} | connection status updated : {FROM} ')
    elif TYPE == "data":
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
            # f'\n>> {IP} | data status updated \n{FROM} : {ECRARM_STATUS[FROM]}')
            f'\n>> {IP} | data status updated : {FROM} ')
    else:
        print(f'no match UpdateType')
    UPDATE_SYS_STATUS(ECRARM_STATUS, updatingStatus)
    # SHOW_ECRARM_STATUS()
    return


def DISCONNECT_AND_STATUS_UPDATE(ECRARM_STATUS: dict, IP: str):
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
        print(">> websocket client disconnected")
    UPDATE_SYS_STATUS(ECRARM_STATUS, updatingStatus=sys_status[1])
    SHOW_ECRARM_STATUS(ECRARM_STATUS)
    return


def INITIALIZE_DATA_STATUS(ECRARM_STATUS: dict):
    ECRARM_STATUS["status"] = sys_status[1]
    ECRARM_STATUS["Detector"]["data"] = {
        "class": "none",
        "x": "0",
        "y": "0"
    }
    ECRARM_STATUS["Controller"]["data"] = {
        "X_Axis": "0",
        "Y_Axis": "0",
        "Z_Axis": "0",
        "W_Axis": "0",
        "R_Axis": "0"
    }
    ECRARM_STATUS["Web"]["data"] = ""
    UPDATE_SYS_STATUS(ECRARM_STATUS, updatingStatus=sys_status[1])
    SHOW_ECRARM_STATUS(ECRARM_STATUS)
    return


if (__name__ == "__main__"):
    print("dataformat.py")
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
    # UPDATE_ECRARM_STATUS("127.0.0.1", "Detector", "connect", False)
    # print(json.dumps(ECRARM_STATUS, sort_keys=True, indent=4))
