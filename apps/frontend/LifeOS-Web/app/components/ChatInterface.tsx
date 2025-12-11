// ChatInterface.tsx
// Component for the LifeOS Web Interface chat interface.
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

  // Effect for initializing state from local storage, runs only once
  useEffect(() => {
    const storedMessages = localStorage.getItem('chatMessages');
    if (storedMessages) {
      // Safely parse the stored JSON
      try {
        const parsedMessages = JSON.parse(storedMessages);
        if (Array.isArray(parsedMessages)) {
          setMessages(parsedMessages);
        }
      } catch (error) {
        console.error("Failed to parse chat messages from local storage:", error);
        localStorage.removeItem('chatMessages'); // Clear corrupted data
      }
    }

    const storedModule = localStorage.getItem('selectedModule');
    if (storedModule && modulePrompts[storedModule]) {
      setCurrentModule(storedModule);
    }
  }, []); // Empty dependency array ensures this runs only once on mount

  // Effect for updating local storage when messages change
  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const handleModuleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedModule = event.target.value;
    setCurrentModule(selectedModule);
    localStorage.setItem('selectedModule', selectedModule);

    // Add a system message to indicate the module has changed
    const systemMessage = `System: Switched to ${selectedModule} module.`;
    setMessages(prevMessages => [...prevMessages, systemMessage]);
  };

  const handleSendMessage = async () => {
    if (newMessage.trim() === '') return;

    const userMessage = `User: ${newMessage}`;
    // Optimistically update the UI with the user's message
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setNewMessage('');

    try {
      // Securely call the backend API route
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: newMessage,
          module: currentModule, // Optionally pass the current module for context
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      const aiResponse = `AI: ${data.reply}`;
      // Update the UI with the AI's response
      setMessages(prevMessages => [...prevMessages, aiResponse]);

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = 'AI: Sorry, I encountered an error. Please try again.';
      // Update the UI with an error message
      setMessages(prevMessages => [...prevMessages, errorMessage]);
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