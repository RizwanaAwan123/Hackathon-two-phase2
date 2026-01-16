import { useState } from 'react';
import { Todo, TodoUpdate } from '../../types/todo';
import TodoForm from './TodoForm';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onUpdate: (id: string, data: TodoUpdate) => void;
  onDelete: (id: string) => void;
}

export default function TodoItem({ todo, onToggle, onUpdate, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [tempDescription, setTempDescription] = useState(todo.description || '');

  const handleUpdate = (data: TodoUpdate) => {
    onUpdate(todo.id, data);
    setIsEditing(false);
  };

  const handleToggle = () => {
    onToggle(todo.id);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <div className={`p-4 mb-2 rounded-md shadow ${todo.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <TodoForm
          onSubmit={(data) => handleUpdate(data)}
          onCancel={() => setIsEditing(false)}
          initialData={{ title: todo.title, description: tempDescription }}
          isEditing={true}
        />
      ) : (
        <div>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={handleToggle}
                className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <span
                className={`ml-3 text-lg ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}
              >
                {todo.title}
              </span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsEditing(true)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </div>
          {todo.description && (
            <p className="ml-7 mt-1 text-gray-600">{todo.description}</p>
          )}
          <p className="ml-7 text-xs text-gray-400">
            Created: {new Date(todo.created_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}