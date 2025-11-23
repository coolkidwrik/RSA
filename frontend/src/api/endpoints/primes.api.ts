import apiClient from '../client';
import type { PrimeGenerationRequest, PrimeGenerationResponse } from '@/models';

export const primesAPI = {
  generate: async (request: PrimeGenerationRequest): Promise<PrimeGenerationResponse> => {
    const response = await apiClient.post('/api/primes/generate', request);
    return response.data;
  },

  getCurrent: async () => {
    const response = await apiClient.get('/api/primes/current');
    return response.data;
  },

  clear: async () => {
    const response = await apiClient.delete('/api/primes/clear');
    return response.data;
  },
};