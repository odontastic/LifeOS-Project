// app/settings/page.tsx
'use client';

import React from 'react';
import SettingsPanel from '../components/SettingsPanel';

export default function SettingsPage() {
  return (
    <div>
      <h1>Settings</h1>
      <SettingsPanel />
    </div>
  );
}