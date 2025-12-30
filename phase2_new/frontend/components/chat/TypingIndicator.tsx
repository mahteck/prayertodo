/**
 * Typing Indicator Component
 * Shows animated dots when agent is processing
 */

export default function TypingIndicator({ visible }: { visible: boolean }) {
  if (!visible) return null;

  return (
    <div className="px-4 py-2">
      <div className="flex items-center gap-2 text-gray-400">
        <div className="flex gap-1">
          <span
            className="w-2 h-2 bg-orange-500 rounded-full animate-bounce"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-2 h-2 bg-orange-500 rounded-full animate-bounce"
            style={{ animationDelay: '150ms' }}
          />
          <span
            className="w-2 h-2 bg-orange-500 rounded-full animate-bounce"
            style={{ animationDelay: '300ms' }}
          />
        </div>
        <span className="text-sm">SalaatFlow is typing...</span>
      </div>
    </div>
  );
}
