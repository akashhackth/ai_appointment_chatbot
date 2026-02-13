import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/api/auth/refresh`, {
            refreshToken,
          });
          
          const { accessToken } = response.data;
          localStorage.setItem('accessToken', accessToken);
          
          // Retry original request
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: { email: string; password: string; fullName: string; phoneNumber?: string }) =>
    api.post('/api/auth/register', data),
  
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  
  refreshToken: (refreshToken: string) =>
    api.post('/api/auth/refresh', { refreshToken }),
  
  getCurrentUser: () =>
    api.get('/api/auth/me'),
};

// Chat API
export const chatAPI = {
  sendMessage: (message: string, sessionId?: string) =>
    api.post('/api/chat/message', { message, sessionId }),
  
  getChatHistory: (sessionId: string, limit = 50) =>
    api.get(`/api/chat/history/${sessionId}`, { params: { limit } }),
  
  getSessions: () =>
    api.get('/api/chat/sessions'),
  
  createSession: () =>
    api.post('/api/chat/session'),
  
  endSession: (sessionId: string) =>
    api.delete(`/api/chat/session/${sessionId}`),
  
  getChatbotToken: () =>
    api.post('/api/chatbot/token'),
};

export default api;
