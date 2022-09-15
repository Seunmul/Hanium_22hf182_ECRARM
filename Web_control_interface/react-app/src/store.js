import { configureStore } from '@reduxjs/toolkit'

import websocketReducer from './reducer/websocketReducer'

export default configureStore({
  reducer: {
    websocket: websocketReducer
  },
})