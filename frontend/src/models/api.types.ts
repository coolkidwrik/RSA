// API type definitions
export interface PrimeGenerationRequest {
  bit_length: number;
  miller_rabin_rounds: number;
}

export interface PrimeGenerationResponse {
  p: string;
  q: string;
  generation_time: number;
  bit_length: number;
  miller_rabin_rounds: number;
}

export interface PublicKey {
  n: string;
  e: string;
}

export interface PrivateKey {
  n: string;
  d: string;
}

export interface RSAParameters {
  n: string;
  phi_n: string;
  e: string;
  d: string;
}

export interface RSAKeysResponse {
  public_key: PublicKey;
  private_key: PrivateKey;
  parameters: RSAParameters;
}

export interface EncryptionRequest {
  message: string;
  n: string;
  e: string;
}

export interface BlockInfo {
  block_number: number;
  original_value: string;
  encrypted_value: string;
  original_hex: string;
  encrypted_hex: string;
}

export interface EncryptionResponse {
  encrypted_blocks: string[];
  block_info: BlockInfo[];
  total_blocks: number;
  message_length: number;
}

export interface DecryptionRequest {
  encrypted_blocks: string[];
  n: string;
  d: string;
}

export interface DecryptionResponse {
  decrypted_message: string;
  success: boolean;
  block_count: number;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  primes_available: boolean;
  keys_generated: boolean;
  system_info: Record<string, string>;
}

export interface ErrorResponse {
  error: string;
  detail: string;
  timestamp?: string;
}