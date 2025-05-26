import axios from 'axios';
import api from './api';

export const subscriptionService = {
  // Get all available subscription plans
  getPlans: async () => {
    try {
      const response = await api.get('/api/subscription/plans');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch subscription plans');
    }
  },
  
  // Get current user subscription details
  getSubscription: async () => {
    try {
      const response = await api.get('/api/subscription/');
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        // No subscription found, return a default
        return null;
      }
      throw new Error(error.response?.data?.detail || 'Failed to fetch subscription details');
    }
  },
  
  // Update user's subscription plan
  updatePlan: async (plan) => {
    try {
      const response = await api.post('/api/subscription/', { plan });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update subscription plan');
    }
  }
};

export default subscriptionService; 