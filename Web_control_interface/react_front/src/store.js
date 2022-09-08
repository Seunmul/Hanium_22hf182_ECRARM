import { configureStore } from '@reduxjs/toolkit'

import counterReducer from './reducer/counterReducer'
import websocketReducer from './reducer/websocketReducer'

export default configureStore({
  reducer: {
    counter: counterReducer,
    websocket: websocketReducer
  },
})