
'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatbotComponentProps {
  onTasksChange?: () => void;  // Callback to notify parent when tasks change
  token?: string; // JWT token to extract user information
}

const ChatbotComponent: React.FC<ChatbotComponentProps> = ({ onTasksChange, token }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I\'m your AI assistant. You can ask me to manage your tasks using natural language. Try saying "Add a task to buy groceries" or "Show my tasks".' }
  ]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Helper function to decode JWT token
  const decodeToken = (token: string) => {
    try {
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }

      // Decode the payload (second part)
      const payload = parts[1];
      // Add padding if needed
      const paddedPayload = payload + '='.repeat((4 - (payload.length % 4)) % 4);
      const decodedPayload = atob(paddedPayload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Send the message to our backend using the same API URL as other endpoints
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chat`, {
        message: input,
        conversation_id: conversationId
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const aiMessage: Message = { role: 'assistant', content: response.data.response };
      setMessages(prev => [...prev, aiMessage]);

      // Check if the response indicates tasks were modified and trigger refresh
      const responseText = response.data.response.toLowerCase();
      if (responseText.includes('added') || responseText.includes('updated') ||
          responseText.includes('deleted') || responseText.includes('completed') ||
          responseText.includes('marked') || responseText.includes('task')) {
        if (onTasksChange) {
          onTasksChange();
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = { role: 'assistant', content: 'Sorry, there was an error processing your message. Please try again.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 flex flex-col h-[500px] max-w-2xl mx-auto">
      {/* Chat Header */}
      <div className="bg-indigo-600 text-white p-4 rounded-t-lg">
        <h3 className="text-lg font-semibold">AI Todo Assistant</h3>
        <p className="text-sm opacity-80">Ask me to manage your tasks with natural language</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-indigo-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message (e.g., 'Add task: Buy groceries')"
            className="flex-1 border border-gray-300 rounded-l-lg p-2 resize-none h-12 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            rows={1}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className={`px-4 py-2 rounded-r-lg text-white font-medium ${
              loading || !input.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700'
            }`}
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500 text-center">
          Commands: add [task], show todos, complete [num], delete [num], help
        </div>
      </div>
    </div>
  );
};

export default ChatbotComponent;