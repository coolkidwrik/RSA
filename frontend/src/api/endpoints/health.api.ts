import apiClient from '../client';
import type { HealthResponse } from '@/models';

export const healthAPI = {
  check: async (): Promise<HealthResponse> => {
    const response = await apiClient.get('/api/health/');
    return response.data;
  },

  ready: async () => {
    const response = await apiClient.get('/api/health/ready');
    return response.data;
  },

  live: async () => {
    const response = await apiClient.get('/api/health/live');
    return response.data;
  },
};