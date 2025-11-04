import React, { useState, useEffect, useRef } from 'react';
import { Button, Input, LoadingSpinner, ErrorMessage } from '@genai-med-chat/shared';
import { apiClient } from '@genai-med-chat/shared';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/chat', { message: input });
      const botMessage = { role: 'bot', content: response.content };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message || 'Failed to get response from the bot');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-lg">
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-lg px-4 py-2 rounded-lg shadow ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-gray-800'}`}>
                {msg.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {error && <ErrorMessage message={error} className="m-4" />}

      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-4">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            className="flex-1"
            disabled={loading}
          />
          <Button onClick={handleSend} disabled={loading}>
            {loading ? <LoadingSpinner size="small" /> : 'Send'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Chat;