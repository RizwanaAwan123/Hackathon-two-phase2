const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 8002; // Using port 8002 for phase4

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend')));

// In-memory storage for todos (for demo purposes)
let todos = [];
let nextId = 1;

// Routes
// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'TodoX Chatbot Backend is running!' });
});

// Get all todos
app.get('/api/todos', (req, res) => {
  res.json(todos);
});

// Create a new todo
app.post('/api/todos', (req, res) => {
  const { title, description } = req.body;
  
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  
  const newTodo = {
    id: nextId++,
    title,
    description: description || '',
    completed: false,
    createdAt: new Date().toISOString()
  };
  
  todos.push(newTodo);
  res.status(201).json(newTodo);
});

// Update a todo
app.put('/api/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { title, description, completed } = req.body;
  
  const todoIndex = todos.findIndex(todo => todo.id === id);
  
  if (todoIndex === -1) {
    return res.status(404).json({ error: 'Todo not found' });
  }
  
  if (title !== undefined) todos[todoIndex].title = title;
  if (description !== undefined) todos[todoIndex].description = description;
  if (completed !== undefined) todos[todoIndex].completed = completed;
  
  todos[todoIndex].updatedAt = new Date().toISOString();
  
  res.json(todos[todoIndex]);
});

// Delete a todo
app.delete('/api/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  
  const todoIndex = todos.findIndex(todo => todo.id === id);
  
  if (todoIndex === -1) {
    return res.status(404).json({ error: 'Todo not found' });
  }
  
  todos.splice(todoIndex, 1);
  res.status(204).send();
});

// Chat endpoint - Process natural language commands
app.post('/api/chat', (req, res) => {
  const { message } = req.body;
  
  if (!message) {
    return res.status(400).json({ message: "Please provide a message" });
  }
  
  // Simple command parsing
  const lowerMsg = message.toLowerCase().trim();
  let response = "";
  
  if (lowerMsg.includes("add") || lowerMsg.includes("create") || lowerMsg.includes("new")) {
    // Extract task from message (simple extraction)
    let taskText = message.replace(/^(add|create|new)\s+/i, "").trim();
    
    if (taskText) {
      const newTodo = {
        id: nextId++,
        title: taskText,
        description: '',
        completed: false,
        createdAt: new Date().toISOString()
      };
      
      todos.push(newTodo);
      response = `✅ Added task: "${taskText}". You now have ${todos.length} tasks.`;
    } else {
      response = "I didn't understand the task you want to add. Please say something like 'add buy groceries'.";
    }
  } 
  else if (lowerMsg.includes("list") || lowerMsg.includes("show") || lowerMsg.includes("all")) {
    if (todos.length === 0) {
      response = "📋 You have no tasks yet. Add some tasks!";
    } else {
      const taskList = todos.map((todo, index) => 
        `${index + 1}. [${todo.completed ? '✅' : '⭕'}] ${todo.title}`
      ).join('\n');
      response = `📋 Your tasks:\n${taskList}`;
    }
  }
  else if (lowerMsg.includes("complete") || lowerMsg.includes("done") || lowerMsg.includes("finish")) {
    // Find task number in message
    const match = message.match(/\d+/);
    if (match) {
      const taskNum = parseInt(match[0]) - 1; // Convert to 0-indexed
      
      if (taskNum >= 0 && taskNum < todos.length) {
        todos[taskNum].completed = true;
        response = `✅ Marked task "${todos[taskNum].title}" as completed!`;
      } else {
        response = `❌ Task #${match[0]} not found. You have ${todos.length} tasks.`;
      }
    } else {
      response = "Which task would you like to mark as complete? Please specify a number.";
    }
  }
  else if (lowerMsg.includes("delete") || lowerMsg.includes("remove")) {
    const match = message.match(/\d+/);
    if (match) {
      const taskNum = parseInt(match[0]) - 1; // Convert to 0-indexed
      
      if (taskNum >= 0 && taskNum < todos.length) {
        const deletedTask = todos.splice(taskNum, 1)[0];
        response = `🗑️ Deleted task: "${deletedTask.title}"`;
      } else {
        response = `❌ Task #${match[0]} not found. You have ${todos.length} tasks.`;
      }
    } else {
      response = "Which task would you like to delete? Please specify a number.";
    }
  }
  else if (lowerMsg.includes("help")) {
    response = `I can help you manage your tasks! Try commands like:
- "add buy milk" - Add a new task
- "show todos" - List all tasks
- "complete 1" - Mark task #1 as completed
- "delete 2" - Delete task #2
- "help" - Show this help message`;
  }
  else {
    response = `I'm not sure how to handle that. Type "help" to see available commands.`;
  }
  
  res.json({ 
    message: response,
    todos: todos
  });
});

// Serve frontend
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`TodoX Chatbot Backend running on http://localhost:${PORT}`);
  console.log(`API available at http://localhost:${PORT}/api`);
  console.log(`Health check at http://localhost:${PORT}/health`);
});