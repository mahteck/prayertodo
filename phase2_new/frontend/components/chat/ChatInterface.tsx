'use client';

/**
 * Chat Interface Component
 * Main container that orchestrates the chat experience
 */

import { useState } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import { sendChatMessage } from '@/lib/chatApi';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatInterface({ userId = 1 }: { userId?: number }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'As-salamu alaykum! ✨\n\nI\'m SalaatFlow Assistant, here to help you manage your spiritual tasks and daily worship.\n\n**I can help you:**\n- Create prayer and spiritual tasks\n- Find masjids and prayer times\n- Get daily hadith\n- Set up prayer reminders\n\n**Try saying:**\n- "Add a task to pray Fajr tomorrow at 5:30 AM"\n- "Show me masjids in North Nazimabad"\n- "Aaj ka hadith sunao"\n- "What time is Jummah at Masjid Al-Huda?"\n\nHow may I assist you today?',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message: string) => {
    // Add user message immediately
    const userMessage: Message = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Show typing indicator
    setIsLoading(true);

    try {
      // Prepare conversation history (exclude current message)
      const history = messages.map(({ role, content }) => ({ role, content }));

      // Send to API
      const response = await sendChatMessage(userId, message, history);

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Show error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'I encountered an error while processing your request. Please make sure the backend is running and try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-5xl mx-auto bg-gray-900 rounded-lg shadow-2xl border border-gray-800 overflow-hidden">
      <MessageList messages={messages} />
      <TypingIndicator visible={isLoading} />
      <MessageInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
