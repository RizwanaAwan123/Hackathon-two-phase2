import { ReactNode } from 'react';
import Head from 'next/head';

interface ResponsiveLayoutProps {
  title: string;
  children: ReactNode;
  description?: string;
}

export default function ResponsiveLayout({ title, children, description = 'Todo Application' }: ResponsiveLayoutProps) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="min-h-screen bg-gray-50">
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </div>
    </>
  );
}