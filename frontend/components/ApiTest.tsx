"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { api } from "@/lib/api"
import { config } from "@/lib/config"

export default function ApiTest() {
  const [testResult, setTestResult] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)

  const testConnection = async () => {
    setIsLoading(true)
    setTestResult("Testing connection...")
    
    try {
      const result = await api.testConnection()
      setTestResult(JSON.stringify(result, null, 2))
    } catch (error) {
      setTestResult(`Error: ${error}`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">API Connection Test</h2>
        
        <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-700 rounded">
          <p className="text-sm">
            <strong>Current API URL:</strong> {config.API_BASE_URL}
          </p>
          <p className="text-sm">
            <strong>Environment:</strong> {config.IS_LOCAL ? "Local Development" : "Production"}
          </p>
        </div>

        <Button 
          onClick={testConnection} 
          disabled={isLoading}
          className="mb-4"
        >
          {isLoading ? "Testing..." : "Test API Connection"}
        </Button>

        {testResult && (
          <div className="mt-4">
            <h3 className="font-semibold mb-2">Test Result:</h3>
            <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded text-sm overflow-auto">
              {testResult}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
} 