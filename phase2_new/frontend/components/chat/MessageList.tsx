'use client';

/**
 * Message List Component
 * Displays chat messages with auto-scroll and markdown support
 */

import { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function MessageList({ messages }: { messages: Message[] }) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-950">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[75%] p-4 rounded-lg shadow-lg ${
              msg.role === 'user'
                ? 'bg-orange-500 text-white'
                : 'bg-gray-800 text-gray-100 border border-gray-700'
            }`}
          >
            {/* Markdown content */}
            <div className={`prose ${msg.role === 'user' ? 'prose-invert' : 'prose-invert'} max-w-none`}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.content}
              </ReactMarkdown>
            </div>

            {/* Timestamp */}
            <div className={`text-xs mt-2 ${msg.role === 'user' ? 'text-orange-100' : 'text-gray-400'}`}>
              {msg.timestamp.toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
              })}
            </div>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
