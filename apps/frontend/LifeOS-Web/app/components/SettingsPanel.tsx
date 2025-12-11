// SettingsPanel.tsx
// Component for managing app settings including module prompts, categories, personal context, notifications, and data management.

'use client';

import React, { useState, useEffect } from 'react';

export default function SettingsPanel() {
  const [settings, setSettings] = useState({
    modulePrompt: '',
    riskCategories: ['Physical Security', 'Household Reliability', 'Parenting Example', 'Emotional Attunement', 'Follow-Through'],
    personalContext: { familyDetails: '', schedule: '' },
    notifications: false,
  });

  useEffect(() => {
    const saved = localStorage.getItem('marriageEqSettings');
    if (saved) setSettings(JSON.parse(saved));
  }, []);

  const saveSettings = () => {
    localStorage.setItem('marriageEqSettings', JSON.stringify(settings));
  };

  const handleCategoryChange = (index: number, value: string) => {
    const newCategories = [...settings.riskCategories];
    newCategories[index] = value;
    setSettings({ ...settings, riskCategories: newCategories });
  };

  const addCategory = () => {
    setSettings({ ...settings, riskCategories: [...settings.riskCategories, ''] });
  };

  const removeCategory = (index: number) => {
    const newCategories = settings.riskCategories.filter((_, i) => i !== index);
    setSettings({ ...settings, riskCategories: newCategories });
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Module Prompt Editor</h2>
        <textarea
          className="w-full p-2 border rounded"
          rows={10}
          value={settings.modulePrompt}
          onChange={(e) => setSettings({ ...settings, modulePrompt: e.target.value })}
          placeholder="Edit module prompts here..."
        />
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Risk Audit Categories</h2>
        {settings.riskCategories.map((category, index) => (
          <div key={index} className="flex mb-2">
            <input
              type="text"
              className="flex-1 p-2 border rounded mr-2"
              value={category}
              onChange={(e) => handleCategoryChange(index, e.target.value)}
            />
            <button
              onClick={() => removeCategory(index)}
              className="px-4 py-2 bg-red-500 text-white rounded"
            >
              Remove
            </button>
          </div>
        ))}
        <button onClick={addCategory} className="px-4 py-2 bg-green-500 text-white rounded">
          Add Category
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Personal Context</h2>
        <div className="mb-4">
          <label className="block mb-1">Family Details</label>
          <textarea
            className="w-full p-2 border rounded"
            value={settings.personalContext.familyDetails}
            onChange={(e) => setSettings({
              ...settings,
              personalContext: { ...settings.personalContext, familyDetails: e.target.value }
            })}
            placeholder="Enter family details..."
          />
        </div>
        <div>
          <label className="block mb-1">Schedule</label>
          <textarea
            className="w-full p-2 border rounded"
            value={settings.personalContext.schedule}
            onChange={(e) => setSettings({
              ...settings,
              personalContext: { ...settings.personalContext, schedule: e.target.value }
            })}
            placeholder="Enter schedule..."
          />
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Notifications</h2>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={settings.notifications}
            onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
            className="mr-2"
          />
          Enable notifications
        </label>
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Data Management</h2>
        <button className="px-4 py-2 bg-blue-500 text-white rounded mr-2" onClick={() => {
          const data = localStorage.getItem('marriageEqData');
          if (data) {
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'marriage-eq-backup.json';
            a.click();
          }
        }}>
          Backup Data
        </button>
        <input
          type="file"
          accept=".json"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) {
              const reader = new FileReader();
              reader.onload = (e) => {
                try {
                  const data = JSON.parse(e.target?.result as string);
                  localStorage.setItem('marriageEqData', JSON.stringify(data));
                  alert('Data restored successfully');
                } catch {
                  alert('Invalid file format');
                }
              };
              reader.readAsText(file);
            }
          }}
          className="mr-2"
        />
        <button className="px-4 py-2 bg-red-500 text-white rounded" onClick={() => {
          if (confirm('Are you sure you want to clear all data?')) {
            localStorage.clear();
            alert('Data cleared');
          }
        }}>
          Clear Data
        </button>
      </div>

      <button onClick={saveSettings} className="px-6 py-3 bg-green-600 text-white rounded text-lg">
        Save Settings
      </button>
    </div>
  );
}