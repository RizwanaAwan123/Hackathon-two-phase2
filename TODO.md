# TODO: Fix Auth Forms 404 Errors

## Completed Tasks
- [x] Updated SignUpForm.tsx to use useAuth.signUp instead of direct fetch to '/api/auth/signup'
- [x] Updated SignInForm.tsx to use useAuth.signIn instead of direct fetch to '/api/auth/signin'
- [x] Removed duplicate auth logic from forms, now using centralized useAuth hook

## Pending Tasks
- [ ] Ensure NEXT_PUBLIC_API_URL is set in frontend/.env.local to point to backend (http://localhost:8000)
- [ ] Start the FastAPI backend server on port 8000
- [ ] Test sign up functionality
- [ ] Test sign in functionality
- [ ] Verify no more 404 errors for auth requests
