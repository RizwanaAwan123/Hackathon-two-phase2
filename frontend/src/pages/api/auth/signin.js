// Next.js API route for user signin
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email, password } = req.body;

  // Validate input
  if (!email || !password) {
    return res.status(400).json({ detail: 'Email and password are required' });
  }

  // Mock user validation (in a real app, you'd check against a database)
  // For demo purposes, accept any credentials
  const mockUser = {
    id: 'mock-user-id',
    email,
    username: 'demo_user',
  };

  // Generate a mock JWT token (in a real app, use proper JWT signing)
  const token = 'mock-jwt-token-' + Date.now();

  res.status(200).json({
    access_token: token,
    token_type: 'bearer',
    user: mockUser
  });
}