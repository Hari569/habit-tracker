// API service for habit tracker
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
    axios.defaults.baseURL = API_BASE_URL;
    
    // Add token to all requests
    axios.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  removeToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  // Auth endpoints
  async login(email, password) {
    const response = await axios.post('/auth/login', { email, password });
    this.setToken(response.data.access_token);
    return response.data;
  }

  async register(email, password, fullName = null) {
    const response = await axios.post('/auth/register', {
      email,
      password,
      full_name: fullName
    });
    return response.data;
  }

  async getCurrentUser() {
    const response = await axios.get('/auth/me');
    return response.data;
  }

  // Habit endpoints
  async getHabits() {
    const response = await axios.get('/habits/');
    return response.data;
  }

  async createHabit(habit) {
    const response = await axios.post('/habits/', habit);
    return response.data;
  }

  async updateHabit(habitId, habit) {
    const response = await axios.put(`/habits/${habitId}`, habit);
    return response.data;
  }

  async deleteHabit(habitId) {
    const response = await axios.delete(`/habits/${habitId}`);
    return response.data;
  }

  async getHabitsForDate(date) {
    const response = await axios.get(`/habits/date/${date}`);
    return response.data;
  }

  // Completion endpoints
  async completeHabit(habitId, date) {
    const response = await axios.post('/completions/', {
      habit_id: habitId,
      completion_date: date
    });
    return response.data;
  }

  async uncompleteHabit(habitId, date) {
    const response = await axios.delete('/completions/', {
      params: { habit_id: habitId, completion_date: date }
    });
    return response.data;
  }

  async getCompletions() {
    const response = await axios.get('/completions/');
    return response.data;
  }

  // Analytics endpoints
  async getCompletionRate(habitId = null, days = 30) {
    const params = { days };
    if (habitId) params.habit_id = habitId;
    
    const response = await axios.get('/analytics/completion-rate', { params });
    return response.data;
  }

  async getStreaks(habitId = null) {
    const params = {};
    if (habitId) params.habit_id = habitId;
    
    const response = await axios.get('/analytics/streaks', { params });
    return response.data;
  }

  async getAnalyticsSummary() {
    const response = await axios.get('/analytics/summary');
    return response.data;
  }
}

const apiService = new ApiService();