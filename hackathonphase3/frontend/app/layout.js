import './globals.css';

export const metadata = {
  title: 'TaskFlowPro',
  description: 'Premium task management with AI assistance',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
