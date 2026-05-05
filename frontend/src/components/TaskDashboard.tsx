import React, { useState, useEffect } from 'react';
import { User, Task } from '../types';
import Header from './Header';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import NotificationPanel from './NotificationPanel';
import { getTasks, getUsers } from '../api';
import { Plus } from 'lucide-react';

interface TaskDashboardProps {
  user: User;
  onLogout: () => void;
}

const TaskDashboard: React.FC<TaskDashboardProps> = ({ user, onLogout }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [tasksData, usersData] = await Promise.all([
        getTasks(),
        getUsers()
      ]);
      setTasks(tasksData);
      setUsers(usersData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks(prev => [newTask, ...prev]);
    setShowTaskForm(false);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(prev => prev.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    ));
    setEditingTask(null);
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(prev => prev.filter(task => task.id !== taskId));
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCloseForm = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        user={user} 
        onLogout={onLogout}
        onShowNotifications={() => setShowNotifications(true)}
      />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Minhas Tarefas</h1>
            <p className="mt-2 text-gray-600">Gerencie suas tarefas e colabore com sua equipe</p>
          </div>
          <button
            onClick={() => setShowTaskForm(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            <Plus className="h-5 w-5 mr-2" />
            Nova Tarefa
          </button>
        </div>

        <TaskList
          tasks={tasks}
          users={users}
          currentUser={user}
          onEdit={handleEditTask}
          onDelete={handleTaskDeleted}
          onUpdate={handleTaskUpdated}
        />
      </main>

      {showTaskForm && (
        <TaskForm
          users={users}
          editingTask={editingTask}
          onClose={handleCloseForm}
          onTaskCreated={handleTaskCreated}
          onTaskUpdated={handleTaskUpdated}
        />
      )}

      {showNotifications && (
        <NotificationPanel
          onClose={() => setShowNotifications(false)}
        />
      )}
    </div>
  );
};

export default TaskDashboard;