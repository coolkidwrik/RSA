import apiClient from '../client';
import type { RSAKeysResponse } from '@/models';

export const keysAPI = {
  generate: async (): Promise<RSAKeysResponse> => {
    const response = await apiClient.post('/api/keys/generate');
    return response.data;
  },

  getCurrent: async () => {
    const response = await apiClient.get('/api/keys/current');
    return response.data;
  },

  validate: async () => {
    const response = await apiClient.post('/api/keys/validate');
    return response.data;
  },
};