import './App.css';

import SocketTest from './websocket/webSocketTest';

function App() {
  return (
    <div className="App">
      <button>start</button>
      <button>stop</button>
      <SocketTest></SocketTest>
    </div>
  );
}

export default App;
