# Data Model for Phase II Todo Application

## User Entity
- **Fields**:
  - id: UUID (primary key, auto-generated)
  - email: String (unique, required, validated email format)
  - username: String (unique, required, 3-30 characters)
  - hashed_password: String (required, stored securely)
  - created_at: DateTime (auto-generated on creation)
  - updated_at: DateTime (auto-generated on update)
- **Validation Rules**:
  - Email must be unique and follow standard email format
  - Username must be 3-30 characters and unique
  - Password must be properly hashed before storage
- **Relationships**:
  - One-to-many relationship with Todo entity (one user has many todos)

## Todo Entity
- **Fields**:
  - id: UUID (primary key, auto-generated)
  - title: String (required, maximum 200 characters)
  - description: String (optional, maximum 1000 characters)
  - completed: Boolean (default: false)
  - user_id: UUID (foreign key, required, references User.id)
  - created_at: DateTime (auto-generated on creation)
  - updated_at: DateTime (auto-generated on update)
- **Validation Rules**:
  - Title is required and must be 1-200 characters
  - Description is optional and limited to 1000 characters
  - Completed defaults to false
  - Must have a valid user_id that references an existing user
- **State Transitions**:
  - Default state: completed = false
  - Toggle transition: completed can switch between true/false

## Relationships
- **User → Todo**: One-to-many (one user owns many todos)
- **Todo → User**: Many-to-one (many todos belong to one user)
- **Constraints**:
  - Foreign key constraint ensures referential integrity
  - Cascade delete: If a user is deleted, their todos are also deleted
  - Todos can only be accessed by their owning user

## Database Schema Considerations
- Indexes on user_id for efficient querying of user's todos
- Indexes on email and username for efficient authentication
- UUID primary keys for security (avoid predictable IDs)
- Timestamps for audit trails and potential future features