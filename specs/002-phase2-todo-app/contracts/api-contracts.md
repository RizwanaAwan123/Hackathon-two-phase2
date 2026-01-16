# API Contracts for Phase II Todo Application

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Creates a new user account
**Request Body**:
```json
{
  "email": "string (required, valid email format)",
  "username": "string (required, 3-30 characters)",
  "password": "string (required, min 8 characters)"
}
```
**Response (201)**:
```json
{
  "id": "uuid",
  "email": "string",
  "username": "string",
  "created_at": "datetime"
}
```
**Response (400)**: Invalid input data
**Response (409)**: Email or username already exists

### POST /api/auth/signin
**Description**: Authenticates a user and returns session token
**Request Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```
**Response (200)**:
```json
{
  "token": "string (JWT token)",
  "user": {
    "id": "uuid",
    "email": "string",
    "username": "string"
  }
}
```
**Response (401)**: Invalid credentials

### POST /api/auth/signout
**Description**: Ends the current user session
**Authentication**: Required (Bearer token)
**Response (200)**: Empty body

## Todo Endpoints

### GET /api/todos
**Description**: Retrieves all todos for the authenticated user
**Authentication**: Required (Bearer token)
**Response (200)**:
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "user_id": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```
**Response (401)**: Unauthorized

### POST /api/todos
**Description**: Creates a new todo for the authenticated user
**Authentication**: Required (Bearer token)
**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 1000 chars)",
  "completed": "boolean (optional, default: false)"
}
```
**Response (201)**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**Response (400)**: Invalid input data
**Response (401)**: Unauthorized

### PUT /api/todos/{todo_id}
**Description**: Updates an existing todo
**Authentication**: Required (Bearer token)
**Path Parameter**: todo_id (UUID)
**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```
**Response (200)**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**Response (400)**: Invalid input data
**Response (401)**: Unauthorized
**Response (404)**: Todo not found

### DELETE /api/todos/{todo_id}
**Description**: Deletes a todo
**Authentication**: Required (Bearer token)
**Path Parameter**: todo_id (UUID)
**Response (204)**: Empty body
**Response (401)**: Unauthorized
**Response (404)**: Todo not found

### PATCH /api/todos/{todo_id}/toggle-complete
**Description**: Toggles the completion status of a todo
**Authentication**: Required (Bearer token)
**Path Parameter**: todo_id (UUID)
**Response (200)**:
```json
{
  "completed": "boolean"
}
```
**Response (401)**: Unauthorized
**Response (404)**: Todo not found