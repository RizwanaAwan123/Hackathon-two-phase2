import { NextPage } from 'next';
import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import Head from 'next/head';
import TodoList from '../components/Todo/TodoList';
import ChatbotComponent from '../components/Chatbot/ChatbotComponent';
import { Todo, TodoCreate, TodoUpdate } from '../types/todo';

const ChatDashboardPage: NextPage = () => {
  const { user, token, signOut, loading } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Fetch todos function
  const fetchTodos = async () => {
    if (!token) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/todos`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          signOut(); // Token expired or invalid
          return;
        }
        throw new Error('Failed to fetch todos');
      }

      const data: Todo[] = await response.json();
      setTodos(data);
    } catch (err) {
      setError('Failed to load todos');
      console.error(err);
    }
  };

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, [token, signOut]);

  const handleAddTodo = async (todoData: TodoCreate) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          signOut();
          return;
        }
        throw new Error('Failed to add todo');
      }

      const newTodo: Todo = await response.json();
      setTodos([...todos, newTodo]);
    } catch (err) {
      setError('Failed to add todo');
      console.error(err);
    }
  };

  const handleUpdateTodo = async (id: string, todoData: TodoUpdate) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          signOut();
          return;
        }
        throw new Error('Failed to update todo');
      }

      const updatedTodo: Todo = await response.json();
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          signOut();
          return;
        }
        throw new Error('Failed to delete todo');
      }

      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError('Failed to delete todo');
      console.error(err);
    }
  };

  const handleToggleTodo = async (id: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/todos/${id}/toggle-complete`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          signOut();
          return;
        }
        throw new Error('Failed to toggle todo');
      }

      const result = await response.json();
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed: result.completed } : todo
      ));
    } catch (err) {
      setError('Failed to toggle todo');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    // User is not authenticated, redirect will happen via useAuth
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Chat Dashboard - Todo App</title>
        <meta name="description" content="Your AI-powered todo dashboard" />
      </Head>

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">AI Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user.username}!</span>
            <button
              onClick={signOut}
              className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="py-8">
        <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="lg:col-span-1">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
                <TodoList
                  todos={todos}
                  onAdd={handleAddTodo}
                  onUpdate={handleUpdateTodo}
                  onDelete={handleDeleteTodo}
                  onToggle={handleToggleTodo}
                />
              </div>
            </div>

            <div className="lg:col-span-1">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">AI Assistant</h2>
                <ChatbotComponent
                  token={token}
                  onTasksChange={() => {
                    // Refresh the todos when the chatbot makes changes
                    fetchTodos();
                  }}
                />
              </div>
            </div>
          </div>

          <div className="mt-8 text-center text-sm text-gray-500">
            <p>Use the AI assistant to manage your tasks with natural language commands!</p>
            <p className="mt-1">Examples: "Add a task to buy groceries", "Show my tasks", "Mark task 1 as complete", "Delete task 2"</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChatDashboardPage;