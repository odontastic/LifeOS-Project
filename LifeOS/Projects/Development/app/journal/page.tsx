// app/journal/page.tsx
'use client';

import React from 'react';
import JournalView from '../components/JournalView';

export default function JournalPage() {
  return (
    <div>
      <h1>Journal</h1>
      <JournalView />
    </div>
  );
}