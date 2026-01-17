// Next.js API route for toggling todo completion
import fs from 'fs';
import path from 'path';

// Simple file-based storage for demo purposes
const TODOS_FILE = path.join(process.cwd(), 'todos.json');

export default async function handler(req, res) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Mock authentication check (in a real app, validate the JWT token)
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ detail: 'Unauthorized' });
  }

  const { id } = req.query;

  if (req.method === 'PATCH') {
    try {
      // Read existing todos
      let todos = [];
      if (fs.existsSync(TODOS_FILE)) {
        const data = fs.readFileSync(TODOS_FILE, 'utf8');
        todos = JSON.parse(data);
      }

      // Find the todo to update
      const todoIndex = todos.findIndex(todo => todo.id === id);
      if (todoIndex === -1) {
        return res.status(404).json({ detail: 'Todo not found' });
      }

      // Toggle completion
      todos[todoIndex].completed = !todos[todoIndex].completed;
      todos[todoIndex].updated_at = new Date().toISOString();

      // Save updated todos
      fs.writeFileSync(TODOS_FILE, JSON.stringify(todos, null, 2));

      res.status(200).json({ completed: todos[todoIndex].completed });
    } catch (error) {
      console.error('Error toggling todo completion:', error);
      res.status(500).json({ detail: 'Internal server error' });
    }
  } else if (req.method === 'PUT' || req.method === 'PATCH') {
    try {
      const { title, description, completed } = req.body;

      // Read existing todos
      let todos = [];
      if (fs.existsSync(TODOS_FILE)) {
        const data = fs.readFileSync(TODOS_FILE, 'utf8');
        todos = JSON.parse(data);
      }

      // Find the todo to update
      const todoIndex = todos.findIndex(todo => todo.id === id);
      if (todoIndex === -1) {
        return res.status(404).json({ detail: 'Todo not found' });
      }

      // Update the todo
      if (title !== undefined) todos[todoIndex].title = title;
      if (description !== undefined) todos[todoIndex].description = description;
      if (completed !== undefined) todos[todoIndex].completed = completed;
      todos[todoIndex].updated_at = new Date().toISOString();

      // Save updated todos
      fs.writeFileSync(TODOS_FILE, JSON.stringify(todos, null, 2));

      res.status(200).json(todos[todoIndex]);
    } catch (error) {
      console.error('Error updating todo:', error);
      res.status(500).json({ detail: 'Internal server error' });
    }
  } else if (req.method === 'DELETE') {
    try {
      // Read existing todos
      let todos = [];
      if (fs.existsSync(TODOS_FILE)) {
        const data = fs.readFileSync(TODOS_FILE, 'utf8');
        todos = JSON.parse(data);
      }

      // Find the todo to delete
      const todoIndex = todos.findIndex(todo => todo.id === id);
      if (todoIndex === -1) {
        return res.status(404).json({ detail: 'Todo not found' });
      }

      // Remove the todo
      todos.splice(todoIndex, 1);

      // Save updated todos
      fs.writeFileSync(TODOS_FILE, JSON.stringify(todos, null, 2));

      res.status(200).json({ message: 'Todo deleted successfully' });
    } catch (error) {
      console.error('Error deleting todo:', error);
      res.status(500).json({ detail: 'Internal server error' });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}