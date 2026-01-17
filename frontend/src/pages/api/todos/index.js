// Next.js API route for todos
let todos = []; // In-memory storage for demo purposes

export default async function handler(req, res) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Mock authentication check (in a real app, validate the JWT token)
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ detail: 'Unauthorized' });
  }

  switch (req.method) {
    case 'GET':
      // Return mock todos for the user
      res.status(200).json(todos);
      break;

    case 'POST':
      const { title, description, completed } = req.body;

      if (!title) {
        return res.status(400).json({ detail: 'Title is required' });
      }

      const newTodo = {
        id: Date.now().toString(),
        title,
        description: description || '',
        completed: completed || false,
        user_id: 'mock-user-id', // In a real app, extract from token
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      todos.push(newTodo);
      res.status(201).json(newTodo);
      break;

    case 'PUT':
    case 'PATCH':
      // For demo, we'll skip individual todo updates
      res.status(501).json({ detail: 'Not implemented in demo' });
      break;

    case 'DELETE':
      // For demo, we'll skip individual todo deletion
      res.status(501).json({ detail: 'Not implemented in demo' });
      break;

    default:
      res.status(405).json({ message: 'Method not allowed' });
  }
}