// RiskAudit.tsx
// Interactive component for weekly risk audit with 5 categories × 7 days grid, scoring, and AI analysis.

'use client';

import React, { useState, useEffect } from 'react';

const categories = ['Physical Security', 'Household Reliability', 'Parenting Example', 'Emotional Attunement', 'Follow-Through'];

export default function RiskAudit() {
  // State for the audit data, which is a grid of categories and days.
  const [audit, setAudit] = useState<Record<string, string>>({});
  // State for the score, which is the number of '✓' marks.
  const [score, setScore] = useState(0);
  // State for the AI's analysis of the audit data.
  const [analysis, setAnalysis] = useState('');
  // State to track whether the AI analysis is in progress.
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('marriageEqRiskAudit');
    if (saved) setAudit(JSON.parse(saved));
  }, []);

  useEffect(() => {
    const total = Object.values(audit).filter(v => v === '✓').length;
    setScore(total);
  }, [audit]);

  const toggleValue = (category: string, day: number) => {
    const key = `${category}-${day}`;
    const current = audit[key] || '';
    const next = current === '' ? '✓' : current === '✓' ? '~' : current === '~' ? '✗' : '';
    setAudit({ ...audit, [key]: next });
    localStorage.setItem('marriageEqRiskAudit', JSON.stringify({ ...audit, [key]: next }));
  };

  const getColor = () => {
    if (score >= 20) return 'text-green-600';
    if (score >= 10) return 'text-yellow-600';
    return 'text-red-600';
  };

  /**
   * Sends the audit data to the backend for analysis and updates the state
   * with the AI's response.
   */
  const handleAiAnalysis = async () => {
    setIsLoading(true);
    setAnalysis('');
    try {
      const response = await fetch('/api/analyze/risk_audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ audit_data: audit }),
      });
      const data = await response.json();
      if (data.error) {
        setAnalysis(`Error: ${data.error}`);
      } else {
        setAnalysis(data.analysis);
      }
    } catch (error) {
      setAnalysis('An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Weekly Risk Audit</h1>
      <div className="mb-4">
        <p className={`text-lg font-semibold ${getColor()}`}>
          Score: {score}/35 ✓ marks
        </p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border">
          <thead>
            <tr>
              <th className="border p-2">Category</th>
              {Array.from({ length: 7 }, (_, i) => (
                <th key={i} className="border p-2">Day {i + 1}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {categories.map(category => (
              <tr key={category}>
                <td className="border p-2 font-semibold">{category}</td>
                {Array.from({ length: 7 }, (_, day) => (
                  <td key={day} className="border p-2 text-center">
                    <button
                      onClick={() => toggleValue(category, day)}
                      className="w-8 h-8 border rounded hover:bg-gray-100"
                    >
                      {audit[`${category}-${day}`] || ''}
                    </button>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-6">
        <button className="px-4 py-2 bg-blue-500 text-white rounded">
          AI Analysis (Placeholder)
        </button>
      </div>
    </div>
  );
}