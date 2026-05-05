export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assigned_to?: number;
  assigned_user_name?: string;
  due_date?: string;
  created_at: string;
  updated_at: string;
  created_by: number;
  created_by_name: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assigned_to?: number;
  due_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  assigned_to?: number;
  due_date?: string;
}

export interface Notification {
  id: number;
  title: string;
  message: string;
  user_id: number;
  is_read: boolean;
  created_at: string;
}