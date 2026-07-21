import axios from 'axios';
import { API_BASE } from './endpoints';

/**
 * Centralized Axios client
 * - Base URL from env
 * - Auth header injected from localStorage
 * - Error interceptor for 401 → logout
 */
const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
  headers: { 'Content-Type': 'application/json' },
});

// Request: inject auth token if present
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('ets_token');
  if (token) config.headers['Authorization'] = `Bearer ${token}`;
  return config;
});

// Response: handle errors
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('ets_token');
      window.location.hash = '/';
    }
    return Promise.reject(error);
  }
);

export default client;
