import { Todo, TodoCreate, TodoUpdate } from '../types/todo';

// Use relative URLs for Vercel deployment compatibility
const API_BASE_URL = typeof window === 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || '')
  : '';

class ApiService {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  async getTodos(): Promise<Todo[]> {
    const response = await fetch(`${API_BASE_URL}/api/todos`, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch todos: ${response.status}`);
    }

    return response.json();
  }

  async createTodo(todo: TodoCreate): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/api/todos`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(todo),
    });

    if (!response.ok) {
      throw new Error(`Failed to create todo: ${response.status}`);
    }

    return response.json();
  }

  async updateTodo(id: string, todo: TodoUpdate): Promise<Todo> {
    const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(todo),
    });

    if (!response.ok) {
      throw new Error(`Failed to update todo: ${response.status}`);
    }

    return response.json();
  }

  async deleteTodo(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete todo: ${response.status}`);
    }
  }

  async toggleTodoCompletion(id: string): Promise<{ completed: boolean }> {
    const response = await fetch(`${API_BASE_URL}/api/todos/${id}/toggle-complete`, {
      method: 'PATCH',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle todo: ${response.status}`);
    }

    return response.json();
  }
}

export default new ApiService();