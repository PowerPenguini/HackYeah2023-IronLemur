import Chat from "./components/Chat";
import Message from "./components/Message";
import Nav from "./components/Nav";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Nav />
      <Message />
      <Chat />
    </div>
  );
}

export default App;
