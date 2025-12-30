/**
 * Chat API Client
 * Handles communication with Phase III chatbot backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  response: string;
  status: string;
  language: string;
}

/**
 * Send a chat message to the AI assistant
 *
 * @param userId - User ID
 * @param message - User's message
 * @param conversationHistory - Previous messages in the conversation
 * @returns Promise with assistant's response
 */
export async function sendChatMessage(
  userId: number,
  message: string,
  conversationHistory: ChatMessage[]
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      message,
      conversation_history: conversationHistory,
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
