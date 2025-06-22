import { config } from './config';
import { logger } from './logger';

const API_BASE_URL = config.API_BASE_URL;

// Helper function to log API calls
const logApiCall = (method: string, endpoint: string, data?: any, response?: any, error?: any) => {
  const logData = {
    method,
    endpoint,
    url: `${API_BASE_URL}${endpoint}`,
    timestamp: new Date().toISOString(),
    data,
    response,
    error: error?.message || error
  };

  if (error) {
    logger.error('API', `${method} ${endpoint} failed`, logData);
  } else {
    logger.info('API', `${method} ${endpoint} successful`, logData);
  }
};

export const api = {
  // Health check endpoint
  testConnection: async () => {
    const endpoint = '/health';
    logger.info('API', `Testing connection to ${API_BASE_URL}${endpoint}`);
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      const data = await response.json();
      
      logApiCall('GET', endpoint, null, data);
      return data;
    } catch (error: any) {
      logApiCall('GET', endpoint, null, null, error);
      throw error;
    }
  },

  // Auth endpoints
  createAnonymousSession: async () => {
    const endpoint = '/api/v1/auth/anonymous';
    logger.info('API', `Creating anonymous session`);
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${data.detail || 'Unknown error'}`);
      }
      
      logApiCall('POST', endpoint, {}, data);
      logger.info('Auth', `Anonymous session created successfully`, { userId: data.user_id });
      return data;
    } catch (error: any) {
      logApiCall('POST', endpoint, {}, null, error);
      logger.error('Auth', `Failed to create anonymous session`, { error: error.message });
      throw error;
    }
  },

  // Chat endpoints
  createChatSession: async (sessionData: any, token?: string) => {
    const endpoint = '/api/v1/chat/session';
    logger.info('API', `Creating chat session`, { sessionType: sessionData.session_type });
    
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
        logger.debug('API', `Using authentication token`);
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(sessionData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${data.detail || 'Unknown error'}`);
      }
      
      logApiCall('POST', endpoint, sessionData, data);
      logger.info('Chat', `Chat session created successfully`, { sessionId: data.session_id });
      return data;
    } catch (error: any) {
      logApiCall('POST', endpoint, sessionData, null, error);
      logger.error('Chat', `Failed to create chat session`, { error: error.message });
      throw error;
    }
  },

  sendMessage: async (messageData: any, token?: string) => {
    const endpoint = '/api/v1/chat/message';
    logger.info('API', `Sending message`, { 
      sessionId: messageData.session_id,
      messageLength: messageData.content?.length || 0
    });
    
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(messageData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${data.detail || 'Unknown error'}`);
      }
      
      logApiCall('POST', endpoint, { ...messageData, content: messageData.content?.substring(0, 100) + '...' }, data);
      
      if (data.crisis_detected) {
        logger.warn('Chat', `Crisis detected in message`, { 
          sessionId: messageData.session_id,
          crisisResources: data.crisis_resources 
        });
      } else {
        logger.info('Chat', `Message sent successfully`, { 
          sessionId: messageData.session_id,
          responseLength: data.message?.length || 0
        });
      }
      
      return data;
    } catch (error: any) {
      logApiCall('POST', endpoint, { ...messageData, content: messageData.content?.substring(0, 100) + '...' }, null, error);
      logger.error('Chat', `Failed to send message`, { 
        sessionId: messageData.session_id,
        error: error.message 
      });
      throw error;
    }
  },

  // Wellness endpoints
  createMoodEntry: async (moodData: any, token?: string) => {
    const endpoint = '/api/v1/wellness/mood';
    logger.info('API', `Creating mood entry`, { moodType: moodData.mood_type });
    
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(moodData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${data.detail || 'Unknown error'}`);
      }
      
      logApiCall('POST', endpoint, moodData, data);
      logger.info('Wellness', `Mood entry created successfully`, { moodType: moodData.mood_type });
      return data;
    } catch (error: any) {
      logApiCall('POST', endpoint, moodData, null, error);
      logger.error('Wellness', `Failed to create mood entry`, { error: error.message });
      throw error;
    }
  },
}; 