import { configureStore } from '@reduxjs/toolkit'

<<<<<<< HEAD:Web_control_interface/react_front/src/store.js
import counterReducer from './reducer/counterReducer'
=======
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/store.js
import websocketReducer from './reducer/websocketReducer'

export default configureStore({
  reducer: {
<<<<<<< HEAD:Web_control_interface/react_front/src/store.js
    counter: counterReducer,
=======
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/store.js
    websocket: websocketReducer
  },
})