import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App component', () => {
  let mockWebSocket;

  beforeEach(() => {
    mockWebSocket = {
      send: jest.fn(),
      onmessage: null,
      onopen: null,
      onclose: null,
      onerror: null,
      close: jest.fn(),
    };

    global.WebSocket = jest.fn(() => mockWebSocket);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('sends a message and displays it on the page', async () => {
    render(<App />);

    const input = screen.getByRole('textbox');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello World' } });
    fireEvent.click(sendButton);

    const messageEvent = { data: JSON.stringify({ message: 'Hello World' }) };
    if (mockWebSocket.onmessage) {
      mockWebSocket.onmessage(messageEvent);
    }

    await waitFor(() => {
      const listItem = screen.getByText('Hello World');
      expect(listItem).toBeInTheDocument();
    });

    expect(mockWebSocket.send).toHaveBeenCalledWith(JSON.stringify({ message: 'Hello World' }));
  });
});
