import React, { useState, useEffect } from 'react';
import './App.css';

const WebSocketChat = () => {
    const [clientId] = useState(Date.now());
    const [messages, setMessages] = useState([]);
    const [messageText, setMessageText] = useState('');
    const [ws, setWs] = useState(null);

    useEffect(() => {
        const socket = new WebSocket(`ws://127.0.0.1:8080/ws/${clientId}`);
        setWs(socket);

        socket.onmessage = (event) => {
            setMessages(prevMessages => [...prevMessages, event.data]);
        };

        return () => {
            socket.close();
        };
    }, [clientId]);

    const sendMessage = (event) => {
        event.preventDefault();
        if (ws && messageText.trim()) {
            ws.send(messageText);
            setMessageText('');
        }
    };

    return (
        <div className="chat-container">
            <h1 className="chat-title">WebSocket Chat</h1>
            <h2 className="chat-id">Your ID: <span>{clientId}</span></h2>
            <form className="chat-form" onSubmit={sendMessage}>
                <input
                    type="text"
                    className="chat-input"
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    autoComplete="off"
                    placeholder="Type a message..."
                />
                <button type="submit" className="chat-button">Send</button>
            </form>
            <ul className="chat-messages">
                {messages.map((message, index) => (
                    <li key={index} className="chat-message">{message}</li>
                ))}
            </ul>
        </div>
    );
};

export default WebSocketChat;
