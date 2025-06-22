"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Download, Trash2, Eye, EyeOff } from "lucide-react"
import { logger } from "@/lib/logger"

interface LogEntry {
  timestamp: string
  level: 'debug' | 'info' | 'warn' | 'error'
  component: string
  message: string
  data?: any
}

export default function LogViewer() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isVisible, setIsVisible] = useState(false)
  const [filterLevel, setFilterLevel] = useState<'all' | 'debug' | 'info' | 'warn' | 'error'>('all')

  // Update logs every second
  useEffect(() => {
    const interval = setInterval(() => {
      setLogs(logger.getLogs())
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  const clearLogs = () => {
    logger.clearLogs()
    setLogs([])
  }

  const downloadLogs = () => {
    const logData = logger.exportLogs()
    const blob = new Blob([logData], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `mindease-logs-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'warn': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      case 'info': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'debug': return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
    }
  }

  const filteredLogs = logs.filter(log => 
    filterLevel === 'all' || log.level === filterLevel
  )

  if (!isVisible) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          onClick={() => setIsVisible(true)}
          variant="outline"
          size="sm"
          className="bg-white dark:bg-gray-800 shadow-lg"
        >
          <Eye className="w-4 h-4 mr-2" />
          Show Logs ({logs.length})
        </Button>
      </div>
    )
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 w-96 max-h-96">
      <Card className="shadow-xl">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm">Frontend Logs</CardTitle>
            <div className="flex items-center gap-2">
              <select
                value={filterLevel}
                onChange={(e) => setFilterLevel(e.target.value as any)}
                className="text-xs px-2 py-1 border rounded"
              >
                <option value="all">All</option>
                <option value="debug">Debug</option>
                <option value="info">Info</option>
                <option value="warn">Warn</option>
                <option value="error">Error</option>
              </select>
              <Button
                onClick={downloadLogs}
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0"
              >
                <Download className="w-3 h-3" />
              </Button>
              <Button
                onClick={clearLogs}
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0"
              >
                <Trash2 className="w-3 h-3" />
              </Button>
              <Button
                onClick={() => setIsVisible(false)}
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0"
              >
                <EyeOff className="w-3 h-3" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="max-h-64 overflow-y-auto space-y-2">
            {filteredLogs.length === 0 ? (
              <p className="text-xs text-gray-500 text-center py-4">No logs yet</p>
            ) : (
              filteredLogs.slice(-50).map((log, index) => (
                <div key={index} className="text-xs border-l-2 border-gray-200 pl-2">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge className={`text-xs ${getLevelColor(log.level)}`}>
                      {log.level.toUpperCase()}
                    </Badge>
                    <span className="text-gray-500">{log.component}</span>
                    <span className="text-gray-400 text-xs">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-1">{log.message}</p>
                  {log.data && (
                    <details className="text-gray-500">
                      <summary className="cursor-pointer">Data</summary>
                      <pre className="text-xs mt-1 bg-gray-50 dark:bg-gray-800 p-2 rounded overflow-x-auto">
                        {JSON.stringify(log.data, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 