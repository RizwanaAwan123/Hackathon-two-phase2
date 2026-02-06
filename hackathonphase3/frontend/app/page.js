'use client';

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`http://localhost:8000/api/1/chat`, {
        message: input,
        conversation_id: conversationId
      });

      const aiMessage = { role: 'assistant', content: response.data.response };
      setMessages(prev => [...prev, aiMessage]);
      setConversationId(response.data.conversation_id);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { role: 'assistant', content: 'Sorry, there was an error processing your message.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0f0f0f', color: 'white', display: 'flex', flexDirection: 'column' }}>
      <div style={{ textAlign: 'center', padding: '1rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem', background: 'linear-gradient(to right, #a855f7, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          TaskFlowPro
        </h1>
        <p style={{ fontSize: '1.25rem', color: '#9ca3af' }}>
          Premium task management with AI assistance
        </p>
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', maxWidth: '800px', margin: '0 auto', width: '100%', padding: '1rem' }}>
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', backgroundColor: 'rgba(0, 0, 0, 0.4)', borderRadius: '1rem', padding: '1rem' }}>
          {messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: '1rem', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
              <div style={{
                display: 'inline-block',
                padding: '0.5rem 1rem',
                borderRadius: '1rem',
                backgroundColor: msg.role === 'user' ? '#a855f7' : 'rgba(255, 255, 255, 0.1)',
                color: 'white'
              }}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ textAlign: 'left' }}>
              <div style={{
                display: 'inline-block',
                padding: '0.5rem 1rem',
                borderRadius: '1rem',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                color: 'white'
              }}>
                Thinking...
              </div>
            </div>
          )}
        </div>
        <div style={{ display: 'flex' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            style={{
              flex: 1,
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem 0 0 0.5rem',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              backgroundColor: 'rgba(0, 0, 0, 0.4)',
              color: 'white'
            }}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '0 0.5rem 0.5rem 0',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              backgroundColor: '#a855f7',
              color: 'white',
              cursor: 'pointer'
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
