import { configureStore } from '@reduxjs/toolkit'

import websocketReducer from 'components/Util/reducer/websocketReducer'

export default configureStore({
  reducer: {
    websocket: websocketReducer
  },
})