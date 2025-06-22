// Configuration for API endpoints
// To use local backend, set NEXT_PUBLIC_API_URL=http://localhost:8000 in your environment
// To use deployed backend, set NEXT_PUBLIC_API_URL=https://mindease-gigu.onrender.com (default)

export const config = {
  API_BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'https://mindease-gigu.onrender.com',
  IS_LOCAL: process.env.NEXT_PUBLIC_API_URL === 'http://localhost:8000',
  IS_PRODUCTION: process.env.NEXT_PUBLIC_API_URL === 'https://mindease-gigu.onrender.com' || !process.env.NEXT_PUBLIC_API_URL,
} 