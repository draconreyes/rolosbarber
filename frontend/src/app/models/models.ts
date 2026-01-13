export interface User {
  id: number;
  username: string;
  email: string;
  role: 'admin' | 'client';
  phone?: string;
  first_name?: string;
  last_name?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  phone?: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface Appointment {
  id?: number;
  client?: number;
  client_details?: User;
  service: 'haircut' | 'beard' | 'combo';
  appointment_date: string;
  appointment_time: string;
  status?: 'pending' | 'confirmed' | 'canceled';
  notes?: string;
  created_at?: string;
  updated_at?: string;
}
