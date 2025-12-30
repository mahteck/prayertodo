import ChatInterface from '@/components/chat/ChatInterface';

export const metadata = {
  title: 'Chat Assistant - SalaatFlow',
  description: 'Chat with SalaatFlow AI Assistant for managing spiritual tasks and worship',
};

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-6 text-center">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-orange-300 mb-2">
            SalaatFlow AI Assistant
          </h1>
          <p className="text-gray-400 text-lg">
            Manage your spiritual journey through natural conversation
          </p>
          <div className="flex items-center justify-center gap-4 mt-4 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              Powered by OpenAI GPT-4
            </span>
            <span>•</span>
            <span>English + Urdu Support</span>
          </div>
        </div>

        {/* Chat Interface */}
        <ChatInterface userId={1} />

        {/* Quick Tips */}
        <div className="mt-6 max-w-5xl mx-auto">
          <details className="bg-gray-900 rounded-lg p-4 border border-gray-800">
            <summary className="cursor-pointer text-orange-500 font-medium">
              💡 Quick Tips & Examples
            </summary>
            <div className="mt-4 space-y-3 text-sm text-gray-400">
              <div>
                <strong className="text-gray-300">Task Management:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 space-y-1">
                  <li>"Add a task to pray Fajr at Masjid Al-Huda tomorrow at 5:30 AM"</li>
                  <li>"Show me all my pending Farz tasks"</li>
                  <li>"Mark my Asr prayer task as completed"</li>
                  <li>"Delete my charity task" (will ask for confirmation)</li>
                </ul>
              </div>
              <div>
                <strong className="text-gray-300">Masjid & Prayer Times:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 space-y-1">
                  <li>"Show masjids in North Nazimabad"</li>
                  <li>"What time is Fajr at Masjid Al-Huda?"</li>
                  <li>"North Nazimabad main Masjid Al-Huda ka Jummah time kya hai?"</li>
                </ul>
              </div>
              <div>
                <strong className="text-gray-300">Daily Hadith:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 space-y-1">
                  <li>"Show me today's hadith"</li>
                  <li>"Aaj ka hadith sunao" (in Urdu)</li>
                </ul>
              </div>
              <div>
                <strong className="text-gray-300">Recurring Reminders:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 space-y-1">
                  <li>"Kal se daily Fajr se 20 minutes pehle mujhe remind karna"</li>
                  <li>"Create a daily reminder for Isha prayer"</li>
                </ul>
              </div>
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}
