import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create an axios instance with default configuration
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 900000, // 15 minutes timeout for course generation
});

// Add request interceptor to include auth token in all authenticated requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Course API Services
export const courseService = {
  // Generate a course using external API
  generateCourse: async (prompt, experienceLevel, personality, learningStyle, intensity = 'medium') => {
    try {
      const response = await api.post('/api/courses/generate-course', {
        prompt,
        experience_level: experienceLevel,
        personality,
        learning_style: learningStyle,
        intensity,
      }, {
        timeout: 900000, // 15 minutes specifically for course generation
      });
      return response.data;
    } catch (error) {
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        throw new Error('La generación del curso está tomando más tiempo del esperado. Esto es normal para cursos complejos. Por favor, intenta de nuevo.');
      }
      throw new Error(error.response?.data?.detail || 'Failed to generate course');
    }
  },
  
  // Save a course
  saveCourse: async (courseData) => {
    try {
      const response = await api.post('/api/courses/save', courseData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to save course');
    }
  },
  
  // Get all courses for current user
  getCourses: async () => {
    try {
      const response = await api.get('/api/courses/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch courses');
    }
  },
  
  // Get a specific course by ID
  getCourse: async (courseId) => {
    try {
      const response = await api.get(`/api/courses/${courseId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch course');
    }
  },
  
  // Delete a course
  deleteCourse: async (courseId) => {
    try {
      const response = await api.delete(`/api/courses/${courseId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete course');
    }
  },
  
  // Solicitar un reemplazo para un tema que ya conoces
  requestTopicReplacement: async (requestData) => {
    try {
      const response = await api.post('/api/courses/replace-topic', requestData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get topic replacement');
    }
  },
  
  // Solicitar un reemplazo para un módulo que ya conoces
  requestModuleReplacement: async (requestData) => {
    try {
      const response = await api.post('/api/courses/replace-module', requestData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get module replacement');
    }
  },
};

export default api; 