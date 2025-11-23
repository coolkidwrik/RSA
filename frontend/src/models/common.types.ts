// common types
export type BackendStatus = 'checking' | 'connected' | 'error';

export type RSAStep = 1 | 2 | 3 | 4;

export interface APIError {
  message: string;
  status?: number;
  detail?: string;
}

export interface ButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning';
  className?: string;
}

export interface InputProps {
  value: string | number;
  onChange: (value: string | number) => void;
  type?: 'text' | 'number' | 'textarea';
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  min?: number;
  max?: number;
  className?: string;
}