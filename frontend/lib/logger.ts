// Frontend logging utility
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  component: string;
  message: string;
  data?: any;
}

class Logger {
  private isDevelopment = process.env.NODE_ENV === 'development';
  private logs: LogEntry[] = [];
  private maxLogs = 1000; // Keep last 1000 logs in memory

  private log(level: LogLevel, component: string, message: string, data?: any) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      component,
      message,
      data
    };

    // Add to memory logs
    this.logs.push(entry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift(); // Remove oldest log
    }

    // Console output
    const emoji = this.getEmoji(level);
    const prefix = `${emoji} [${component}]`;
    
    if (this.isDevelopment) {
      // Development: More detailed logging
      console.group(`${prefix} ${message}`);
      if (data) {
        console.log('Data:', data);
      }
      console.log('Timestamp:', entry.timestamp);
      console.groupEnd();
    } else {
      // Production: Simple logging
      const logMethod = level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log';
      console[logMethod](`${prefix} ${message}`, data || '');
    }

    // Send to backend analytics in production (optional)
    if (!this.isDevelopment && level === 'error') {
      this.sendToAnalytics(entry);
    }
  }

  private getEmoji(level: LogLevel): string {
    switch (level) {
      case 'debug': return '🔍';
      case 'info': return 'ℹ️';
      case 'warn': return '⚠️';
      case 'error': return '❌';
      default: return '📝';
    }
  }

  private sendToAnalytics(entry: LogEntry) {
    // Optional: Send error logs to backend analytics
    // This can be implemented later for production monitoring
    try {
      // fetch('/api/analytics/log', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(entry)
      // });
    } catch (error) {
      // Silently fail to avoid infinite loops
    }
  }

  debug(component: string, message: string, data?: any) {
    this.log('debug', component, message, data);
  }

  info(component: string, message: string, data?: any) {
    this.log('info', component, message, data);
  }

  warn(component: string, message: string, data?: any) {
    this.log('warn', component, message, data);
  }

  error(component: string, message: string, data?: any) {
    this.log('error', component, message, data);
  }

  // Get logs for debugging
  getLogs(): LogEntry[] {
    return [...this.logs];
  }

  // Clear logs
  clearLogs() {
    this.logs = [];
  }

  // Export logs for debugging
  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

// Create singleton instance
export const logger = new Logger();

// Convenience functions
export const logDebug = (component: string, message: string, data?: any) => 
  logger.debug(component, message, data);

export const logInfo = (component: string, message: string, data?: any) => 
  logger.info(component, message, data);

export const logWarn = (component: string, message: string, data?: any) => 
  logger.warn(component, message, data);

export const logError = (component: string, message: string, data?: any) => 
  logger.error(component, message, data); 