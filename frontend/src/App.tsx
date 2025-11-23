// src/App.tsx
import React, { useState, useEffect } from 'react';
import { Loader2, Key, Lock, Unlock, Settings, CheckCircle, XCircle, Info, Copy } from 'lucide-react';

// Type Definitions
interface PrimeGenerationResponse {
  p: string;
  q: string;
  generation_time: number;
  bit_length: number;
  miller_rabin_rounds: number;
}

interface PublicKey {
  n: string;
  e: string;
}

interface PrivateKey {
  n: string;
  d: string;
}

interface RSAParameters {
  n: string;
  phi_n: string;
  e: string;
  d: string;
}

interface RSAKeysResponse {
  public_key: PublicKey;
  private_key: PrivateKey;
  parameters: RSAParameters;
}

interface BlockInfo {
  block_number: number;
  original_value: string;
  encrypted_value: string;
  original_hex: string;
  encrypted_hex: string;
}

interface EncryptionResponse {
  encrypted_blocks: string[];
  block_info: BlockInfo[];
  total_blocks: number;
  message_length: number;
}

interface DecryptionResponse {
  decrypted_message: string;
  success: boolean;
  block_count: number;
}

type BackendStatus = 'checking' | 'connected' | 'error';

// API Base URL - Vite uses import.meta.env instead of process.env
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const App: React.FC = () => {
  const [step, setStep] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  
  // Prime generation state
  const [bitLength, setBitLength] = useState<number>(512);
  const [millerRounds, setMillerRounds] = useState<number>(10);
  const [primes, setPrimes] = useState<PrimeGenerationResponse | null>(null);
  
  // Keys state
  const [keys, setKeys] = useState<RSAKeysResponse | null>(null);
  
  // Encryption state
  const [message, setMessage] = useState<string>('Hello RSA!');
  const [encryptedData, setEncryptedData] = useState<EncryptionResponse | null>(null);
  const [decryptedMessage, setDecryptedMessage] = useState<string>('');
  
  // Backend health check
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking');
  
  // Check backend connection on mount
  useEffect(() => {
    checkBackendHealth();
  }, []);
  
  const checkBackendHealth = async (): Promise<void> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health/`);
      if (response.ok) {
        setBackendStatus('connected');
      } else {
        setBackendStatus('error');
      }
    } catch (err) {
      setBackendStatus('error');
      setError('Cannot connect to backend. Make sure it\'s running on port 8000');
    }
  };
  
  // API call helper with better error handling
  const apiCall = async <T,>(
    endpoint: string, 
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET', 
    data: unknown = null
  ): Promise<T> => {
    try {
      const config: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };
      
      if (data) {
        config.body = JSON.stringify(data);
      }
      
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (err) {
      if (err instanceof Error && err.message.includes('Failed to fetch')) {
        throw new Error('Cannot connect to backend. Make sure the server is running.');
      }
      throw err;
    }
  };
  
  // Generate primes
  const generatePrimes = async (): Promise<void> => {
    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall<PrimeGenerationResponse>(
        '/api/primes/generate', 
        'POST', 
        {
          bit_length: bitLength,
          miller_rabin_rounds: millerRounds
        }
      );
      
      setPrimes(response);
      setKeys(null);
      setEncryptedData(null);
      setDecryptedMessage('');
      setStep(2);
    } catch (err) {
      setError(`Prime generation failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Generate keys
  const generateKeys = async (): Promise<void> => {
    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall<RSAKeysResponse>('/api/keys/generate', 'POST');
      setKeys(response);
      setEncryptedData(null);
      setDecryptedMessage('');
      setStep(3);
    } catch (err) {
      setError(`Key generation failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Encrypt message
  const encryptMessage = async (): Promise<void> => {
    if (!message.trim()) {
      setError('Please enter a message to encrypt');
      return;
    }
    
    if (!keys) {
      setError('No keys available. Generate keys first.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall<EncryptionResponse>(
        '/api/crypto/encrypt', 
        'POST', 
        {
          message: message,
          n: keys.public_key.n,
          e: keys.public_key.e
        }
      );
      
      setEncryptedData(response);
      setDecryptedMessage('');
      setStep(4);
    } catch (err) {
      setError(`Encryption failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Decrypt message
  const decryptMessage = async (): Promise<void> => {
    if (!encryptedData || !keys) {
      setError('No encrypted data or keys available');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall<DecryptionResponse>(
        '/api/crypto/decrypt', 
        'POST', 
        {
          encrypted_blocks: encryptedData.encrypted_blocks,
          n: keys.private_key.n,
          d: keys.private_key.d
        }
      );
      
      setDecryptedMessage(response.decrypted_message);
    } catch (err) {
      setError(`Decryption failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Run full demo
  const runFullDemo = async (): Promise<void> => {
    setStep(1);
    setError('');
    await generatePrimes();
    setTimeout(async () => {
      await generateKeys();
      setTimeout(async () => {
        await encryptMessage();
        setTimeout(async () => {
          await decryptMessage();
        }, 1000);
      }, 1000);
    }, 1000);
  };
  
  // Format large numbers for display
  const formatLargeNumber = (num: string | undefined, maxLength: number = 60): string => {
    if (!num) return 'Not generated';
    const str = num.toString();
    if (str.length <= maxLength) return str;
    const half = Math.floor(maxLength / 2);
    return `${str.substring(0, half)}...${str.substring(str.length - half)}`;
  };
  
  // Copy to clipboard
  const copyToClipboard = async (text: string): Promise<void> => {
    try {
      await navigator.clipboard.writeText(text);
      alert('Copied to clipboard!');
    } catch (err) {
      alert('Failed to copy');
    }
  };
  
  // Get background color for status
  const getStatusColor = (status: BackendStatus): string => {
    switch (status) {
      case 'connected':
        return '#d1fae5';
      case 'error':
        return '#fee2e2';
      default:
        return '#e5e7eb';
    }
  };
  
  // Get text color for status
  const getStatusTextColor = (status: BackendStatus): string => {
    switch (status) {
      case 'connected':
        return '#065f46';
      case 'error':
        return '#991b1b';
      default:
        return '#374151';
    }
  };
  
  // Get indicator color for status
  const getIndicatorColor = (status: BackendStatus): string => {
    switch (status) {
      case 'connected':
        return '#10b981';
      case 'error':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🔐 RSA Encryption System
          </h1>
          <p className="text-gray-600">Full-Stack Implementation: React (Vite + TypeScript) + Python Backend</p>
          
          {/* Backend Status Indicator */}
          <div 
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium"
            style={{
              backgroundColor: getStatusColor(backendStatus),
              color: getStatusTextColor(backendStatus)
            }}
          >
            <div 
              className="w-2 h-2 rounded-full animate-pulse"
              style={{ backgroundColor: getIndicatorColor(backendStatus) }}
            />
            Backend: {backendStatus === 'connected' ? 'Connected' : 
                     backendStatus === 'error' ? 'Disconnected' : 'Checking...'}
          </div>
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
            <XCircle className="text-red-500 mr-3 flex-shrink-0 mt-0.5" size={20} />
            <div className="flex-1">
              <span className="text-red-700">{error}</span>
              {error.includes('Cannot connect') && (
                <div className="mt-2 text-sm text-red-600">
                  <strong>Troubleshooting:</strong>
                  <ul className="list-disc ml-5 mt-1">
                    <li>Make sure Python backend is running: <code className="bg-red-100 px-1 rounded">uvicorn main:app --reload</code></li>
                    <li>Check that port 8000 is not blocked</li>
                    <li>Verify CORS settings in backend/.env</li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Progress Steps */}
        <div className="flex justify-center mb-8">
          {[1, 2, 3, 4].map((stepNum) => (
            <div key={stepNum} className="flex items-center">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all
                ${step >= stepNum ? 'bg-blue-500 text-white scale-110' : 'bg-gray-200 text-gray-500'}
              `}>
                {stepNum}
              </div>
              {stepNum < 4 && (
                <div className={`w-16 h-1 transition-all ${step > stepNum ? 'bg-blue-500' : 'bg-gray-200'}`} />
              )}
            </div>
          ))}
        </div>
        
        <div className="grid gap-6">
          {/* Step 1: Prime Generation */}
          <div className={`bg-white rounded-lg shadow-md p-6 transition-all ${step !== 1 ? 'opacity-60' : ''}`}>
            <div className="flex items-center mb-4">
              <Settings className="text-blue-500 mr-3" size={24} />
              <h2 className="text-xl font-semibold">Step 1: Generate Large Primes</h2>
            </div>
            
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Prime Bit Length
                </label>
                <input
                  type="number"
                  min={256}
                  max={2048}
                  value={bitLength}
                  onChange={(e) => setBitLength(parseInt(e.target.value))}
                  className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={loading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Miller-Rabin Rounds
                </label>
                <input
                  type="number"
                  min={1}
                  max={100}
                  value={millerRounds}
                  onChange={(e) => setMillerRounds(parseInt(e.target.value))}
                  className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={loading}
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={generatePrimes}
                  disabled={loading || backendStatus !== 'connected'}
                  className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center"
                >
                  {loading && <Loader2 className="animate-spin mr-2" size={16} />}
                  Generate Primes
                </button>
              </div>
            </div>
            
            {primes && (
              <>
                <div className="grid md:grid-cols-2 gap-4 mb-3">
                  <div className="bg-gray-50 p-4 rounded-md">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-semibold">Prime p:</h3>
                      <button onClick={() => copyToClipboard(primes.p)} className="text-blue-500 hover:text-blue-700">
                        <Copy size={16} />
                      </button>
                    </div>
                    <code className="text-xs break-all">{formatLargeNumber(primes.p)}</code>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-md">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-semibold">Prime q:</h3>
                      <button onClick={() => copyToClipboard(primes.q)} className="text-blue-500 hover:text-blue-700">
                        <Copy size={16} />
                      </button>
                    </div>
                    <code className="text-xs break-all">{formatLargeNumber(primes.q)}</code>
                  </div>
                </div>
                <div className="text-sm text-gray-600">
                  Generation time: {primes.generation_time.toFixed(3)}s | Bit length: {primes.bit_length} | Rounds: {primes.miller_rabin_rounds}
                </div>
              </>
            )}
          </div>
          
          {/* Step 2: Key Generation */}
          <div className={`bg-white rounded-lg shadow-md p-6 transition-all ${step !== 2 ? 'opacity-60' : ''}`}>
            <div className="flex items-center mb-4">
              <Key className="text-green-500 mr-3" size={24} />
              <h2 className="text-xl font-semibold">Step 2: Generate RSA Keys</h2>
            </div>
            
            <button
              onClick={generateKeys}
              disabled={loading || !primes}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white py-2 px-4 rounded-md transition-colors flex items-center mb-4"
            >
              {loading && <Loader2 className="animate-spin mr-2" size={16} />}
              Generate Key Pair
            </button>
            
            {keys && (
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-green-50 p-4 rounded-md border border-green-200">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold">Public Key (n, e):</h3>
                    <Copy 
                      size={16} 
                      className="cursor-pointer text-green-600 hover:text-green-800"
                      onClick={() => copyToClipboard(JSON.stringify(keys.public_key, null, 2))}
                    />
                  </div>
                  <div className="text-xs space-y-2">
                    <div><strong>n:</strong> <code className="break-all">{formatLargeNumber(keys.public_key.n, 40)}</code></div>
                    <div><strong>e:</strong> <code>{keys.public_key.e}</code></div>
                  </div>
                </div>
                <div className="bg-red-50 p-4 rounded-md border border-red-200">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold">Private Key (n, d):</h3>
                    <Copy 
                      size={16} 
                      className="cursor-pointer text-red-600 hover:text-red-800"
                      onClick={() => copyToClipboard(JSON.stringify(keys.private_key, null, 2))}
                    />
                  </div>
                  <div className="text-xs space-y-2">
                    <div><strong>n:</strong> <code className="break-all">{formatLargeNumber(keys.private_key.n, 40)}</code></div>
                    <div><strong>d:</strong> <code className="break-all">{formatLargeNumber(keys.private_key.d, 40)}</code></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Step 3: Encryption */}
          <div className={`bg-white rounded-lg shadow-md p-6 transition-all ${step !== 3 ? 'opacity-60' : ''}`}>
            <div className="flex items-center mb-4">
              <Lock className="text-orange-500 mr-3" size={24} />
              <h2 className="text-xl font-semibold">Step 3: Encrypt Message</h2>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message to Encrypt:
              </label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="w-full p-2 border rounded-md h-24 focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                placeholder="Enter your message here..."
                disabled={loading}
              />
            </div>
            
            <button
              onClick={encryptMessage}
              disabled={loading || !keys}
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white py-2 px-4 rounded-md transition-colors flex items-center mb-4"
            >
              {loading && <Loader2 className="animate-spin mr-2" size={16} />}
              Encrypt Message
            </button>
            
            {encryptedData && (
              <div className="bg-orange-50 p-4 rounded-md border border-orange-200">
                <h3 className="font-semibold mb-2">Encrypted Blocks ({encryptedData.total_blocks}):</h3>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {encryptedData.block_info.map((block) => (
                    <div key={block.block_number} className="text-xs bg-white p-2 rounded border">
                      <div><strong>Block {block.block_number}:</strong></div>
                      <div className="text-gray-600">Encrypted: {formatLargeNumber(block.encrypted_value, 50)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* Step 4: Decryption */}
          <div className={`bg-white rounded-lg shadow-md p-6 transition-all ${step !== 4 ? 'opacity-60' : ''}`}>
            <div className="flex items-center mb-4">
              <Unlock className="text-purple-500 mr-3" size={24} />
              <h2 className="text-xl font-semibold">Step 4: Decrypt Message</h2>
            </div>
            
            <button
              onClick={decryptMessage}
              disabled={loading || !encryptedData}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white py-2 px-4 rounded-md transition-colors flex items-center mb-4"
            >
              {loading && <Loader2 className="animate-spin mr-2" size={16} />}
              Decrypt Message
            </button>
            
            {decryptedMessage && (
              <div className="bg-purple-50 p-4 rounded-md border border-purple-200">
                <h3 className="font-semibold mb-2">Decrypted Message:</h3>
                <div className="bg-white p-3 rounded border">
                  <code className="text-sm">{decryptedMessage}</code>
                </div>
                {decryptedMessage === message && (
                  <div className="mt-2 text-green-600 flex items-center text-sm">
                    <CheckCircle size={16} className="mr-1" />
                    <span>Decryption successful! Message matches original.</span>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
        
        {/* Full Demo Button */}
        <div className="text-center mt-8">
          <button
            onClick={runFullDemo}
            disabled={loading || backendStatus !== 'connected'}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white py-3 px-8 rounded-lg font-semibold transition-all duration-300 flex items-center mx-auto shadow-lg"
          >
            {loading && <Loader2 className="animate-spin mr-2" size={20} />}
            Run Full Demo
          </button>
        </div>
        
        {/* Info Panel */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-8">
          <div className="flex items-center mb-2">
            <Info className="text-blue-500 mr-2" size={20} />
            <h3 className="font-semibold text-blue-800">Architecture Details</h3>
          </div>
          <div className="text-sm text-blue-700 space-y-1">
            <p><strong>Frontend:</strong> React + Vite + TypeScript (Type-safe development)</p>
            <p><strong>Backend:</strong> Python FastAPI with structured endpoints</p>
            <p><strong>API Docs:</strong> <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="underline">http://localhost:8000/docs</a></p>
            <p><strong>Build Tool:</strong> Vite for instant updates and optimized builds</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;