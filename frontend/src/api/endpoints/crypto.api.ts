import apiClient from '../client';
import type { 
  EncryptionRequest, 
  EncryptionResponse,
  DecryptionRequest,
  DecryptionResponse 
} from '@/models';

export const cryptoAPI = {
  encrypt: async (request: EncryptionRequest): Promise<EncryptionResponse> => {
    const response = await apiClient.post('/api/crypto/encrypt', request);
    return response.data;
  },

  decrypt: async (request: DecryptionRequest): Promise<DecryptionResponse> => {
    const response = await apiClient.post('/api/crypto/decrypt', request);
    return response.data;
  },
};