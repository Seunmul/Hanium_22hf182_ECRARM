<<<<<<< HEAD:Web_control_interface/react_front/src/reducer/websocketReducer.js
import { createSlice } from '@reduxjs/toolkit'

const websocketSlice = createSlice({
    name: 'ws',
    initialState: {
        connect: false,
        connectionStatus: 0,
        data: {
            "status": "initializing",
            "Detector": {
                "connect": false,
                "data": {
                    "class": "none",
                    "x": "0",
                    "y": "0",
                }
            },
            "Controller": {
                "connect": false,
                "data": {
                    "X_Axis": "0",
                    "Y_Axis": "0",
                    "Z_Axis": "0",
                    "W_Axis": "0",
                    "R_Axis": "0"
                }
            },
            "Web": {
                "bridgeConnect": false,
                "data": ""
            }
        },
        receivedDataList: []
    },
    reducers: {
        connected: (state, action) => {
            state.connect = true
            console.log(action.type)
        },
        disconnected: (state, action) => {
            state.connect = false
            console.log(action.type)
        },
        updateWebSocketConnection: (state, action) => {
            state.connectionStatus = action.payload
            console.log(action.type)
        }
        ,
        updateSystemStatus: (state, action) => {
            state.data = action.payload
            console.log(action.type)
        },
        updateReceivedDataList: (state, action) => {
            state.receivedDataList = [...state.receivedDataList, action.payload]
            console.log(action.type)
        },
        clearReceivedDataList: (state, action) => {
            state.receivedDataList = []
            console.log(action.type)
        }

    }
})


export { websocketSlice }
// Action creators are generated for each case reducer function
export const { connected, disconnected, updateWebSocketConnection,
    updateSystemStatus, updateReceivedDataList, clearReceivedDataList } = websocketSlice.actions

export default websocketSlice.reducer
=======
import { createSlice } from "@reduxjs/toolkit";

const websocketSlice = createSlice({
  name: "websocket",
  initialState: {
    connectionHandleMsg: "",
    connectionStatus: 0,
    sendingMessage: "",
    isDataReceived: false,
    data: {
      status: "initializing",
      Detector: {
        connect: false,
        data: {
          class: "none",
          x: "0",
          y: "0",
        },
      },
      Controller: {
        connect: false,
        data: {
          X_Axis: "0",
          Y_Axis: "0",
          Z_Axis: "0",
          W_Axis: "0",
          R_Axis: "0",
        },
      },
      Web: {
        bridgeConnect: false,
        data: "",
      },
    },
    receivedDataList: [],
  },
  reducers: {
    connectionHandler:(state,action)=>{
      state.connectionHandleMsg = action.payload;
      console.log(action.type)
    },
    updateSendingMessage: (state, action) => {
      state.sendingMessage = action.payload;
      console.log(action.type);
    },
    updateWebSocketConnection: (state, action) => {
      state.connectionStatus = action.payload;
      console.log(action.type);
    },
    updateSystemStatus: (state, action) => {
      state.data = action.payload;
      console.log(action.type);
    },
    updateReceivedDataList: (state, action) => {
      state.receivedDataList = [...state.receivedDataList, action.payload];
      console.log(action.type);
    },
    clearReceivedDataList: (state, action) => {
      state.receivedDataList = [];
      console.log(action.type);
    },
    setIsDataReceived: (state, action) => {
      state.isDataReceived = action.payload;
      console.log(action.type);
    },
  },
});

export { websocketSlice };
// Action creators are generated for each case reducer function
export const {
  connectionHandler,
  updateSendingMessage,
  updateWebSocketConnection,
  updateSystemStatus,
  updateReceivedDataList,
  clearReceivedDataList,
  setIsDataReceived,
} = websocketSlice.actions;

export default websocketSlice.reducer;
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/reducer/websocketReducer.js
