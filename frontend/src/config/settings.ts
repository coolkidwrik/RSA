// centralized configuration
export const config = {
  api: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: 30000,
  },
  rsa: {
    defaultBitLength: 512,
    minBitLength: 256,
    maxBitLength: 2048,
    defaultMillerRabinRounds: 10,
    minMillerRabinRounds: 1,
    maxMillerRabinRounds: 100,
  },
  ui: {
    maxMessageLength: parseInt(import.meta.env.VITE_MAX_MESSAGE_LENGTH || '10000'),
    numberDisplayLength: 60,
    enableAdvancedMode: import.meta.env.VITE_ENABLE_ADVANCED_MODE === 'true',
  },
  app: {
    name: 'RSA Encryption System',
    version: '1.0.0',
  },
} as const;

export default config;