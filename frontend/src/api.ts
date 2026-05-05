import axios from 'axios';
import { User, Task, TaskCreate, TaskUpdate, Notification } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const register = async (name: string, email: string, password: string) => {
  const response = await api.post('/users/register', { name, email, password });
  return response.data;
};

export const login = async (email: string, password: string) => {
  const response = await api.post('/users/login', { email, password });
  return response.data;
};

// User APIs
export const getUsers = async (): Promise<User[]> => {
  const response = await api.get('/users');
  return response.data;
};

// Task APIs
export const getTasks = async (): Promise<Task[]> => {
  const response = await api.get('/tasks');
  return response.data;
};

export const createTask = async (task: TaskCreate): Promise<Task> => {
  const response = await api.post('/tasks', task);
  return response.data;
};

export const updateTask = async (id: number, task: TaskUpdate): Promise<Task> => {
  const response = await api.put(`/tasks/${id}`, task);
  return response.data;
};

export const deleteTask = async (id: number): Promise<void> => {
  await api.delete(`/tasks/${id}`);
};

// Notification APIs
export const getNotifications = async (): Promise<Notification[]> => {
  const response = await api.get('/notifications');
  return response.data;
};

export const markNotificationAsRead = async (id: number): Promise<void> => {
  await api.put(`/notifications/${id}/read`);
};