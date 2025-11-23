# RSA Encryption Frontend

Modern, type-safe React frontend built with Vite and TypeScript.

## Architecture

- **Config Layer**: Centralized configuration
- **Types Layer**: TypeScript type definitions
- **API Layer**: Axios-based API client with endpoints
- **Hooks Layer**: Custom React hooks for state management
- **Components Layer**: Reusable React components
- **Utils Layer**: Helper functions and utilities

## Project Structure

```
src/
├── config/          # Configuration
├── models/           # TypeScript types
├── api/             # API client and endpoints
├── hooks/           # Custom hooks
├── components/      # React components
│   ├── common/      # Reusable components
│   ├── rsa/         # RSA-specific components
│   └── layout/      # Layout components
└── utils/           # Utility functions
```

## Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_ENABLE_ADVANCED_MODE=false
VITE_MAX_MESSAGE_LENGTH=10000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code
- `npm run type-check` - Check TypeScript types

## Tech Stack

- React 19
- TypeScript
- Vite
- Axios
- Tailwind CSS (via CDN)
- Lucide React (icons)

## Backend Integration

The frontend communicates with the Python FastAPI backend running on port 8000. All API calls are proxied through Vite's dev server.

## Code Organization

### Config
Centralized configuration in `src/config/settings.ts`

### Types
All TypeScript types in `src/models/`

### API
- `api/client.ts` - Axios instance with interceptors
- `api/endpoints/` - API endpoint functions organized by domain

### Hooks
- `useRSA` - Main RSA operations
- `useBackendStatus` - Backend health monitoring
- `useCopyToClipboard` - Clipboard utilities

### Components
- `common/` - Reusable UI components
- `rsa/` - RSA-specific components
- `layout/` - Layout components

### Utils
- `formatters.ts` - Number and text formatting
- `validators.ts` - Input validation
- `constants.ts` - Application constants