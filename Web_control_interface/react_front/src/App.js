import './App.css';
import Login from './pages/Login';

// import SocketTest from './websocket/webSocketTest';
import SocketTest from './websocket/webSocketTest2';

function App() {
  return (
    <div className="App">
      <SocketTest></SocketTest>
      <Login></Login>
    </div>
  );
}

export default App;
