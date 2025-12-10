// app/layout.tsx

import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Marriage EQ OS',
  description: 'A platform for relationship health',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav>
          <ul>
            <li>
              <Link href="/">Home</Link>
            </li>
            <li>
              <Link href="/chat">Chat</Link>
            </li>
            <li>
              <Link href="/journal">Journal</Link>
            </li>
            <li>
              <Link href="/risk-audit">Risk Audit</Link>
            </li>
            <li>
              <Link href="/settings">Settings</Link>
            </li>
          </ul>
        </nav>
        {children}
      </body>
    </html>
  );
}