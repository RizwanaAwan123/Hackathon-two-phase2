import { Todo, TodoCreate, TodoUpdate } from '../../types/todo';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';

interface TodoListProps {
  todos: Todo[];
  onAdd: (todo: TodoCreate) => void;
  onUpdate: (id: string, data: TodoUpdate) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

export default function TodoList({ todos, onAdd, onUpdate, onDelete, onToggle }: TodoListProps) {
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Your Todos</h2>
      <TodoForm onSubmit={onAdd} />
      {todos.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No todos yet. Add one above!</p>
        </div>
      ) : (
        <div>
          {todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggle={onToggle}
              onUpdate={onUpdate}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}