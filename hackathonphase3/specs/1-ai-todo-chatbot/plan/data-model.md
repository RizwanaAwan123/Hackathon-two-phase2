# Data Model: AI Todo Chatbot

## Task Entity
- **id**: Integer (Primary Key, Auto-increment)
- **content**: String (Required, Max length: 500)
- **status**: String (Enum: 'pending', 'completed', Default: 'pending')
- **created_at**: DateTime (Default: current timestamp)
- **updated_at**: DateTime (Auto-update on modification)
- **user_id**: Integer (Foreign Key to User table)
- **conversation_id**: Integer (Foreign Key to Conversation table)

**Validation Rules:**
- Content must not be empty
- Status must be one of allowed values
- Cannot update completed tasks without uncompleting first

## Conversation Entity
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: Integer (Foreign Key to User table)
- **title**: String (Optional, Max length: 200, Auto-generated from first message if not provided)
- **created_at**: DateTime (Default: current timestamp)
- **updated_at**: DateTime (Auto-update on modification)
- **is_active**: Boolean (Default: true)

**Relationships:**
- One-to-many with Message entity
- One-to-many with Task entity

## Message Entity
- **id**: Integer (Primary Key, Auto-increment)
- **conversation_id**: Integer (Foreign Key to Conversation table)
- **role**: String (Enum: 'user', 'assistant', 'system')
- **content**: Text (Required)
- **timestamp**: DateTime (Default: current timestamp)
- **tool_calls**: JSON (Optional, stores tool call information)
- **tool_responses**: JSON (Optional, stores tool response information)

**Validation Rules:**
- Role must be one of allowed values
- Content must not be empty
- Must belong to an active conversation

## Indexes
- Task: (user_id, status) for efficient filtering
- Conversation: (user_id, is_active) for user conversation retrieval
- Message: (conversation_id, timestamp) for chronological ordering

## State Transitions
- Task: pending → completed (via complete_task operation)
- Conversation: is_active = true → is_active = false (when conversation ends)