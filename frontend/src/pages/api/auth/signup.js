// Next.js API route for user signup
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email, username, password } = req.body;

  // Validate input
  if (!email || !username || !password) {
    return res.status(400).json({ detail: 'Email, username, and password are required' });
  }

  // Mock user creation (in a real app, you'd connect to a database)
  const newUser = {
    id: Date.now().toString(), // In a real app, use UUID
    email,
    username,
    created_at: new Date().toISOString()
  };

  // Generate a mock JWT token (in a real app, use proper JWT signing)
  const token = 'mock-jwt-token-' + Date.now();

  res.status(201).json({
    ...newUser,
    access_token: token,
    token_type: 'bearer'
  });
}