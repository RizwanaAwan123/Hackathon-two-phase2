# API Contracts: AI Todo Chatbot

## Chat Endpoint
```
POST /api/chat
```

### Request Schema
```json
{
  "message": "string (required)",
  "conversation_id": "integer (optional, creates new if not provided)"
}
```

### Response Schema
```json
{
  "response": "string",
  "conversation_id": "integer",
  "timestamp": "ISO 8601 datetime",
  "status": "success | error"
}
```

### Error Response Schema
```json
{
  "error": "string",
  "code": "string",
  "timestamp": "ISO 8601 datetime",
  "status": "error"
}
```

## Authentication
All endpoints require authentication via Better Auth headers:
```
Authorization: Bearer {token}
```

## MCP Tool Contracts

### add_task Tool
**Parameters:**
```json
{
  "content": "string (required)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "task_id": "integer",
  "message": "string"
}
```

### list_tasks Tool
**Parameters:**
```json
{
  "status_filter": "string (optional, 'pending' | 'completed')"
}
```

**Response:**
```json
{
  "success": "boolean",
  "tasks": [
    {
      "id": "integer",
      "content": "string",
      "status": "string",
      "created_at": "ISO 8601 datetime"
    }
  ]
}
```

### update_task Tool
**Parameters:**
```json
{
  "task_id": "integer (required)",
  "content": "string (required)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "message": "string"
}
```

### complete_task Tool
**Parameters:**
```json
{
  "task_id": "integer (required)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "message": "string"
}
```

### delete_task Tool
**Parameters:**
```json
{
  "task_id": "integer (required)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "message": "string"
}
```