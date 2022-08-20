import './App.css';
import Login from './pages/Login';

// import SocketTest from './websocket/webSocketTest';
import SocketTest from './component/websocket/webSocket';
import Home from './pages/Home';

function App() {
  return (
    <div className="App">
      <SocketTest></SocketTest>
      <Home></Home>
    </div>
  );
}

export default App;
