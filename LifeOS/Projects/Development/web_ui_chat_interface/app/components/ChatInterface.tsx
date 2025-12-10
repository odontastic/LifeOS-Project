// ChatInterface.tsx
// Component for the Marriage EQ OS chat interface.
// Dependencies: React, Tailwind CSS
// This component handles message display, input, module selection, and local storage.

import React, { useState, useEffect } from 'react';

const modulePrompts = {
  'Base': "You are my Personal Life OS with a specialized focus on emotional intelligence, marriage health, and Catholic virtue development...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
  'Morning Kickstart': "MORNING KICKSTART MODE ACTIVATED\n\nYour job: Help me start the day with clarity, presence, and wife-focused awareness...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
  'Crisis Support': "CRISIS MODE ACTIVATED\n\nYou've indicated: Wife is upset / I messed up / Conflict happening...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
  'Risk Audit': "WEEKLY RISK AUDIT (Through Her Lens)\n\nThis is a *security assessment* from your wife's perspective...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
  'Pattern Spotter': "WEEKLY PATTERN ANALYSIS\n\nAnswer these questions honestly. I'll help you see what you're missing...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
  'Mini Journal': "EVENING CHECK-IN (3 minutes)\n\nQuick daily capture...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
};

const ChatInterface = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [currentModule, setCurrentModule] = useState('Base');
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    // Load chat history from local storage
    const storedMessages = localStorage.getItem('chatMessages');
    if (storedMessages) {
      setMessages(JSON.parse(storedMessages));
    }

    // Load selected module from local storage
    const storedModule = localStorage.getItem('selectedModule');
    if (storedModule) {
      setCurrentModule(storedModule);
    }

    // Add system message based on selected module
    const systemMessage = modulePrompts[currentModule] || 'Base Prompt';
    setMessages([...messages, `System: ${systemMessage}`]);

  }, [currentModule, messages]);

  const handleModuleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedModule = event.target.value;
    setCurrentModule(selectedModule);
    localStorage.setItem('selectedModule', selectedModule);

    // Add system message when module changes
    const systemMessage = modulePrompts[selectedModule] || 'Base Prompt';
    setMessages([...messages, `System: ${systemMessage}`]);
  };

  const handleSendMessage = async () => {
    if (newMessage.trim() !== '') {
      setMessages([...messages, `User: ${newMessage}`]);
      setNewMessage('');

      try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.CLAUDE_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'claude-3-opus-20240229',
            max_tokens: 200,
            messages: [{ 'role': 'user', 'content': newMessage }]
          }),
        });

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        setMessages([...messages, `User: ${newMessage}`, `AI: ${aiResponse}`]);
        // Simplified SPR Compression: Extract key insights and recommendations
        const sprSummary = `Key Insights: ${messages.slice(-5).map(msg => msg.split(':')[1]).join(', ')}\nRecommendations: Based on recent conversation, consider...`;
        localStorage.setItem('chatMessages', JSON.stringify({ summary: sprSummary, fullMessages: [...messages, `User: ${newMessage}`, `AI: ${aiResponse}`] }));

      } catch (error) {
        console.error('Error calling Claude API:', error);
        setMessages([...messages, `User: ${newMessage}`, `AI: Error generating response`]);
        localStorage.setItem('chatMessages', JSON.stringify([...messages, `User: ${newMessage}`, `AI: Error generating response`]));
      }
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-800 text-white">
      {/* Module Selection */}
      <div className="p-4">
        <label htmlFor="moduleSelect" className="block text-sm font-medium text-gray-300">Select Module:</label>
        <select
          id="moduleSelect"
          value={currentModule}
          onChange={handleModuleChange}
          className="mt-2 block w-full rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:w-64"
        >
          {Object.keys(modulePrompts).map((module) => (
            <option key={module} value={module}>{module}</option>
          ))}
        </select>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((message, index) => (
          <div key={index} className="mb-2">
            {message}
          </div>
        ))}
      </div>

      {/* Input Field and Send Button */}
      <div className="p-4">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          className="flex-1 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 w-full mr-2"
          placeholder="Type your message..."
        />
        <button
          onClick={handleSendMessage}
          className="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;