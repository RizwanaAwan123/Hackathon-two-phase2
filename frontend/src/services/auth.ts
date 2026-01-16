// This file will contain authentication-related API utilities
// It's already integrated in the useAuth hook, but we can add additional utilities here

export interface User {
  id: string;
  email: string;
  username: string;
}

export interface SignUpData {
  email: string;
  username: string;
  password: string;
}

export interface SignInData {
  email: string;
  password: string;
}

// Additional auth utilities can be added here if needed
// For example, token refresh, password reset, etc.