// JournalView.tsx
// Component for displaying daily journal entries with navigation and export options.

'use client';

import React, { useState, useEffect } from 'react';

export default function JournalView() {
  const [journals, setJournals] = useState<Record<string, any>>({});
  const [currentDate, setCurrentDate] = useState('');

  useEffect(() => {
    setCurrentDate(new Date().toISOString().split('T')[0]);
    const saved = localStorage.getItem('marriageEqJournals');
    if (saved) setJournals(JSON.parse(saved));
  }, []);



  const currentEntry = journals[currentDate] || {};

  const exportData = (format: string) => {
    let content = '';
    if (format === 'json') {
      content = JSON.stringify(journals, null, 2);
    } else if (format === 'markdown') {
      content = Object.entries(journals).map(([date, entry]: [string, any]) => {
        return `# ${date}\n\n${entry.chatSessions?.map((s: any) => s.messages.map((m: any) => `**${m.role}:** ${m.content}`).join('\n')).join('\n\n') || ''}`;
      }).join('\n\n---\n\n');
    }
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `journal.${format}`;
    a.click();
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Daily Journal</h1>
      <div className="mb-4">
        <input
          type="date"
          value={currentDate}
          onChange={(e) => setCurrentDate(e.target.value)}
          className="p-2 border rounded"
        />
      </div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">{currentDate}</h2>
        {currentEntry.chatSessions ? (
          <div>
            {currentEntry.chatSessions.map((session: any, i: number) => (
              <div key={i} className="mb-4 p-4 border rounded">
                <h3 className="font-semibold">{session.module}</h3>
                {session.messages.map((msg: any, j: number) => (
                  <div key={j} className="mb-2">
                    <strong>{msg.role}:</strong> {msg.spr || msg.content}
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <p>No entries for this date.</p>
        )}
      </div>
      <div>
        <button onClick={() => exportData('json')} className="px-4 py-2 bg-blue-500 text-white rounded mr-2">
          Export JSON
        </button>
        <button onClick={() => exportData('markdown')} className="px-4 py-2 bg-green-500 text-white rounded mr-2">
          Export Markdown
        </button>
        <button onClick={() => exportData('csv')} className="px-4 py-2 bg-purple-500 text-white rounded">
          Export CSV
        </button>
      </div>
    </div>
  );
}