import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://192.168.105.115:8001/ws');

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };
    ws.onclose = () => console.log('WS disconnected');
    ws.onerror = (error) => console.error('WS err:', error);

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = () => {
    if (socket && inputValue.trim() !== '') {
      socket.send(JSON.stringify({ message: inputValue }));
      setInputValue('');
    }
  };

  return (
    <div className="app-container">
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          className="input-box"
          placeholder="Type your message here..."
        />
        <button onClick={handleSendMessage} className="send-button">Send</button>
      </div>
      <h1>Real-time Messages</h1>
      <div className="message-frame">
        <ul className="message-list">
          {messages.map((msg, index) => (
            <li key={index} className="message-item">{msg.message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
