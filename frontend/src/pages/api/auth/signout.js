// Next.js API route for user signout
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  // In a real app, you might invalidate the token here
  res.status(200).json({ message: 'Successfully signed out' });
}