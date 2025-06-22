"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChevronLeft, MoreVertical, Send, Mic, PlusCircle } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { logger } from "@/lib/logger"

interface Message {
  id: number
  sender: "user" | "bot"
  text: string
  avatar?: string
  timestamp?: Date
}

interface ChatSession {
  session_id: string
  token: string
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [session, setSession] = useState<ChatSession | null>(null)
  const [isInitialized, setIsInitialized] = useState(false)
  const router = useRouter()
  const messagesEndRef = useRef<null | HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize chat session on component mount
  useEffect(() => {
    const initializeChat = async () => {
      logger.info('ChatBot', 'Initializing chat session');
      
      try {
        setIsLoading(true)
        
        // Create anonymous session
        logger.info('ChatBot', 'Creating anonymous session');
        const sessionResponse = await api.createAnonymousSession()
        
        if (sessionResponse.access_token) {
          logger.info('ChatBot', 'Anonymous session created successfully', { 
            userId: sessionResponse.user_id 
          });
          
          setSession({
            session_id: sessionResponse.user_id, // Using user_id as session_id for now
            token: sessionResponse.access_token
          })

          // Create chat session
          logger.info('ChatBot', 'Creating chat session');
          const chatSessionResponse = await api.createChatSession({
            session_type: "free_form",
            emotion_context: "general_wellness"
          }, sessionResponse.access_token)

          if (chatSessionResponse.session_id) {
            logger.info('ChatBot', 'Chat session created successfully', { 
              sessionId: chatSessionResponse.session_id 
            });
            
            // Update session with actual session_id
            setSession(prev => prev ? {
              ...prev,
              session_id: chatSessionResponse.session_id
            } : null)
            
            // Add welcome message
            const welcomeMessage: Message = {
              id: Date.now(),
              sender: "bot",
              text: "Hello! I'm MindEase, your AI mental wellness companion. I'm here to support you with any thoughts, feelings, or concerns you'd like to discuss. How are you feeling today?",
              avatar: "/placeholder-logo.svg",
              timestamp: new Date()
            };
            
            setMessages([welcomeMessage])
            logger.info('ChatBot', 'Welcome message added');
          } else {
            logger.warn('ChatBot', 'Chat session creation failed - no session_id returned');
          }
        } else {
          logger.error('ChatBot', 'Anonymous session creation failed - no access_token returned');
        }
      } catch (error: any) {
        logger.error('ChatBot', 'Failed to initialize chat', { error: error.message });
        
        const errorMessage: Message = {
          id: Date.now(),
          sender: "bot",
          text: "I'm having trouble connecting right now. Please try again in a moment.",
          avatar: "/placeholder-logo.svg",
          timestamp: new Date()
        }
        setMessages([errorMessage])
      } finally {
        setIsLoading(false)
        setIsInitialized(true)
        logger.info('ChatBot', 'Chat initialization completed');
      }
    }

    initializeChat()
  }, [])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !session || isLoading) {
      logger.debug('ChatBot', 'Message send blocked', { 
        hasInput: !!input.trim(), 
        hasSession: !!session, 
        isLoading 
      });
      return;
    }

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: input,
      avatar: "/placeholder-user.jpg",
      timestamp: new Date()
    }
    
    logger.info('ChatBot', 'Sending user message', { 
      messageLength: input.length,
      sessionId: session.session_id 
    });
    
    setMessages((prev) => [...prev, userMessage])
    const currentInput = input
    setInput("")
    setIsLoading(true)

    try {
      const response = await api.sendMessage({
        content: currentInput,
        session_id: session.session_id,
        session_type: "free_form"
      }, session.token)

      if (response.message) {
        const botMessage: Message = {
          id: Date.now() + 1,
          sender: "bot",
          text: response.message,
          avatar: "/placeholder-logo.svg",
          timestamp: new Date()
        }
        setMessages((prev) => [...prev, botMessage])
        
        logger.info('ChatBot', 'AI response received', { 
          responseLength: response.message.length,
          sessionId: session.session_id 
        });
        
        // Handle crisis detection
        if (response.crisis_detected && response.crisis_resources) {
          logger.warn('ChatBot', 'Crisis detected - showing resources', { 
            sessionId: session.session_id,
            crisisResources: response.crisis_resources 
          });
          
          const crisisMessage: Message = {
            id: Date.now() + 2,
            sender: "bot",
            text: `⚠️ Crisis Resources: ${response.crisis_resources.message}\n\nHotline: ${response.crisis_resources.hotline}\nText Line: ${response.crisis_resources.text_line}`,
            avatar: "/placeholder-logo.svg",
            timestamp: new Date()
          }
          setMessages((prev) => [...prev, crisisMessage])
        }
      } else {
        logger.warn('ChatBot', 'AI response missing message content');
        // Handle error response
        const errorMessage: Message = {
          id: Date.now() + 1,
          sender: "bot",
          text: "I'm sorry, I'm having trouble processing your message right now. Please try again.",
          avatar: "/placeholder-logo.svg",
          timestamp: new Date()
        }
        setMessages((prev) => [...prev, errorMessage])
      }
    } catch (error: any) {
      logger.error('ChatBot', 'Failed to send message', { 
        error: error.message,
        sessionId: session.session_id 
      });
      
      const errorMessage: Message = {
        id: Date.now() + 1,
        sender: "bot",
        text: "I'm sorry, there was an error sending your message. Please check your connection and try again.",
        avatar: "/placeholder-logo.svg",
        timestamp: new Date()
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackClick = () => {
    logger.info('ChatBot', 'User navigating back');
    router.back();
  };

  return (
    <div className="flex flex-col h-screen bg-transparent text-gray-900 dark:text-white">
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 w-full max-w-4xl mx-auto">
        <Button variant="ghost" size="icon" onClick={handleBackClick} className="text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800">
          <ChevronLeft className="w-6 h-6" />
        </Button>
        <div className="flex flex-col items-center">
          <h1 className="text-lg font-semibold">MindEase Chat</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">AI Mental Wellness Companion</p>
        </div>
        <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800">
          <MoreVertical className="w-6 h-6" />
        </Button>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-6 w-full max-w-4xl mx-auto space-y-6">
        {!isInitialized && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500 mx-auto mb-4"></div>
              <p className="text-gray-500 dark:text-gray-400">Initializing chat...</p>
            </div>
          </div>
        )}
        
        {isInitialized && messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-end gap-3 ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.sender === "bot" && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                 <div className="w-4 h-4 bg-white rounded-sm transform rotate-45"></div>
              </div>
            )}
            <div
              className={`max-w-xs md:max-w-md p-4 rounded-2xl ${
                msg.sender === "user"
                  ? "bg-gradient-to-br from-pink-500 to-purple-600 text-white rounded-br-none"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-bl-none"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
            </div>
             {msg.sender === "user" && (
              <Image
                src={msg.avatar!}
                alt="User Avatar"
                width={32}
                height={32}
                className="rounded-full"
              />
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex items-end gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center flex-shrink-0">
              <div className="w-4 h-4 bg-white rounded-sm transform rotate-45"></div>
            </div>
            <div className="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-2xl rounded-bl-none p-4">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </main>

      {/* Input Form */}
      <footer className="p-4 bg-white dark:bg-black border-t border-gray-200 dark:border-gray-800">
        <form
          onSubmit={handleSendMessage}
          className="flex items-center gap-2 rounded-full bg-gray-100 dark:bg-gray-900/50 p-2 w-full max-w-4xl mx-auto"
        >
          <Input
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setInput(e.target.value)
            }
            placeholder={isLoading ? "Please wait..." : "Type your message..."}
            disabled={isLoading || !isInitialized}
            className="flex-1 bg-transparent border-none focus:ring-0 text-gray-900 dark:text-white placeholder-gray-500 px-2"
          />
          <Button type="button" variant="ghost" size="icon" className="text-gray-500 dark:text-gray-400" disabled={isLoading}>
            <Mic className="w-5 h-5" />
          </Button>
          <Button 
            type="submit" 
            variant="ghost" 
            size="icon" 
            className="text-gray-500 dark:text-gray-400 hover:text-pink-500"
            disabled={isLoading || !isInitialized || !input.trim()}
          >
            <Send className="w-5 h-5" />
          </Button>
        </form>
      </footer>
    </div>
  )
} 