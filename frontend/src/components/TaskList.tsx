import React from 'react';
import { Task, User } from '../types';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  users: User[];
  currentUser: User;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({ 
  tasks, 
  users, 
  currentUser, 
  onEdit, 
  onDelete, 
  onUpdate 
}) => {
  const tasksByStatus = {
    pending: tasks.filter(task => task.status === 'pending'),
    in_progress: tasks.filter(task => task.status === 'in_progress'),
    completed: tasks.filter(task => task.status === 'completed'),
    cancelled: tasks.filter(task => task.status === 'cancelled')
  };

  const statusLabels = {
    pending: 'Pendentes',
    in_progress: 'Em Progresso',
    completed: 'Concluídas',
    cancelled: 'Canceladas'
  };

  const statusColors = {
    pending: 'bg-yellow-50 border-yellow-200',
    in_progress: 'bg-blue-50 border-blue-200',
    completed: 'bg-green-50 border-green-200',
    cancelled: 'bg-gray-50 border-gray-200'
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center">
          <div className="text-gray-400 text-2xl">📝</div>
        </div>
        <h3 className="mt-4 text-lg font-medium text-gray-900">Nenhuma tarefa encontrada</h3>
        <p className="mt-2 text-gray-500">Comece criando sua primeira tarefa!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6">
      {Object.entries(tasksByStatus).map(([status, statusTasks]) => (
        <div key={status} className={`rounded-xl border-2 ${statusColors[status as keyof typeof statusColors]} p-4`}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">
              {statusLabels[status as keyof typeof statusLabels]}
            </h3>
            <span className="bg-white px-2 py-1 rounded-full text-sm font-medium text-gray-600">
              {statusTasks.length}
            </span>
          </div>
          
          <div className="space-y-3">
            {statusTasks.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                users={users}
                currentUser={currentUser}
                onEdit={onEdit}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            ))}
            
            {statusTasks.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <p className="text-sm">Nenhuma tarefa neste status</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;