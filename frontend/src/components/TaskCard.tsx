import React from 'react';
import { Task, User } from '../types';
import { updateTask, deleteTask } from '../api';
import { Edit2, Trash2, Calendar, User as UserIcon, AlertCircle } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  users: User[];
  currentUser: User;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (task: Task) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ 
  task, 
  users, 
  currentUser, 
  onEdit, 
  onDelete, 
  onUpdate 
}) => {
  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };

  const priorityLabels = {
    low: 'Baixa',
    medium: 'Média',
    high: 'Alta',
    urgent: 'Urgente'
  };

  const handleStatusChange = async (newStatus: Task['status']) => {
    try {
      const updatedTask = await updateTask(task.id, { status: newStatus });
      onUpdate(updatedTask);
    } catch (error) {
      console.error('Error updating task status:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      try {
        await deleteTask(task.id);
        onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && task.status !== 'completed';

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <h4 className="font-medium text-gray-900 text-sm leading-tight">{task.title}</h4>
        <div className="flex items-center space-x-1">
          <button
            onClick={() => onEdit(task)}
            className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
          >
            <Edit2 className="h-4 w-4" />
          </button>
          <button
            onClick={handleDelete}
            className="p-1 text-gray-400 hover:text-red-600 transition-colors"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {task.description && (
        <p className="text-gray-600 text-xs mb-3 line-clamp-2">{task.description}</p>
      )}

      <div className="flex items-center justify-between mb-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${priorityColors[task.priority]}`}>
          {priorityLabels[task.priority]}
        </span>
        
        {isOverdue && (
          <div className="flex items-center text-red-600">
            <AlertCircle className="h-4 w-4 mr-1" />
            <span className="text-xs font-medium">Atrasada</span>
          </div>
        )}
      </div>

      {task.assigned_user_name && (
        <div className="flex items-center text-gray-600 mb-2">
          <UserIcon className="h-4 w-4 mr-1" />
          <span className="text-xs">{task.assigned_user_name}</span>
        </div>
      )}

      {task.due_date && (
        <div className="flex items-center text-gray-600 mb-3">
          <Calendar className="h-4 w-4 mr-1" />
          <span className="text-xs">{formatDate(task.due_date)}</span>
        </div>
      )}

      <div className="flex justify-between items-center">
        <select
          value={task.status}
          onChange={(e) => handleStatusChange(e.target.value as Task['status'])}
          className="text-xs border border-gray-200 rounded px-2 py-1 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="pending">Pendente</option>
          <option value="in_progress">Em Progresso</option>
          <option value="completed">Concluída</option>
          <option value="cancelled">Cancelada</option>
        </select>
        
        <span className="text-xs text-gray-500">
          por {task.created_by_name}
        </span>
      </div>
    </div>
  );
};

export default TaskCard;