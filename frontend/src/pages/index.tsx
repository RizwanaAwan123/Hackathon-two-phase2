import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

const HomePage: NextPage = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Todo App - Home</title>
        <meta name="description" content="Manage your todos efficiently" />
      </Head>

      <div className="flex items-center justify-center min-h-[80vh] bg-gray-50">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl md:text-5xl">
              <span className="block">Manage your</span>
              <span className="block text-indigo-600 mt-2">todos efficiently</span>
            </h1>
            <p className="mt-4 text-base text-gray-500 sm:text-lg md:text-xl">
              A simple and effective todo application to help you organize your tasks and boost productivity.
            </p>
          </div>
          <div className="mt-8 space-y-4">
            <div className="rounded-md shadow">
              {user ? (
                <Link
                  href="/dashboard"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg"
                >
                  Go to Dashboard
                </Link>
              ) : (
                <Link
                  href="/auth/signin"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg"
                >
                  Sign In
                </Link>
              )}
            </div>
            {!user && (
              <div>
                <Link
                  href="/auth/signup"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 md:py-4 md:text-lg"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;