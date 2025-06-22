const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  // Test endpoints
  testConnection: async () => {
    const response = await fetch(`${API_BASE_URL}/api/v1/test`);
    return response.json();
  },

  getEmotions: async () => {
    const response = await fetch(`${API_BASE_URL}/api/v1/test/emotions`);
    return response.json();
  },

  getTopics: async () => {
    const response = await fetch(`${API_BASE_URL}/api/v1/test/topics`);
    return response.json();
  },

  // Auth endpoints
  createAnonymousSession: async () => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/anonymous`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });
    return response.json();
  },

  // Chat endpoints
  createChatSession: async (sessionData: any, token?: string) => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/chat/session`, {
      method: 'POST',
      headers,
      body: JSON.stringify(sessionData),
    });
    return response.json();
  },

  sendMessage: async (messageData: any, token?: string) => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/chat/message`, {
      method: 'POST',
      headers,
      body: JSON.stringify(messageData),
    });
    return response.json();
  },

  // Wellness endpoints
  createMoodEntry: async (moodData: any, token?: string) => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/wellness/mood`, {
      method: 'POST',
      headers,
      body: JSON.stringify(moodData),
    });
    return response.json();
  },
}; 