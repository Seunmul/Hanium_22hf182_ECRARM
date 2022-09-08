import React from 'react'
import { createContext, useReducer } from 'react'

const webSocketUrl = "ws://155.230.25.98:8888"

// websocket 연결 try
  const connectWebSocket = () => {
    console.log("---\nopen socket")
    ws.current = new WebSocket(webSocketUrl);
    setSocketStatus(0);
    ws.current.onopen = () => {
      console.log("connected to " + webSocketUrl);
      setSocketConnected(true);
      setSocketStatus(ws.current.readyState)
    };
    ws.current.onerror = (error) => {
      console.log("connection error " + webSocketUrl);
      setSocketConnected(false);
      setSocketStatus(ws.current.readyState)
      console.log(error);
    };
    ws.current.onclose = (error) => {
      console.log("disconnect from " + webSocketUrl);
      setSocketConnected(false);
      setSocketStatus(ws.current.readyState)
      console.log(error);
    };
    ws.current.onmessage = (evt) => {
      const data = evt.data;
      console.log(data);
      setRecivedMsg((prev) => data);
      setReceivedMessageList((prevItems) => [...prevItems, data]);
    };
  }

// reducer
const initialState = {
    admin: false
}
const WebSocketReducer = (state, action) => {
    switch(action.type) {
        case 'SET_ADMIN': 
        return {
            ...state,
            admin: !state.admin
        }
        default: 
            console.log("Doesn't have action type");
    }
}

// context
export const WebSocketContext = createContext({});

// provider
export const WebSocketProvider = ({ children }) => {
    const [state, dispatch] = useReducer(WebSocketReducer, initialState);
    const { admin } = state;
    return (
        <WebSocketContext.Provider value={{ dispatch, admin }}>
            { children }
        </WebSocketContext.Provider>
    )
}





