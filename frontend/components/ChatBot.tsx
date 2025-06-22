"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChevronLeft, MoreVertical, Send, Mic, PlusCircle } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"

interface Message {
  id: number
  sender: "user" | "bot"
  text: string
  avatar?: string
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: "bot",
      text: "Describe to me the basic principles of healthy eating. Briefly, but with all the important aspects, please. also you can tell me a little more about the topic of sports and training",
      avatar: "/placeholder-logo.svg", // Using placeholder for the futuristic icon
    },
    {
      id: 2,
      sender: "user",
      text: "Basic principles of a healthy diet: Balance: Make sure your diet contains all the essential macro and micronutrients in the correct proportions: carbohydrates, proteins, fats, vitamins and minerals. It is important to maintain a balance of calories to meet your body's needs, but not to overeat.",
      avatar: "/placeholder-user.jpg",
    },
  ])
  const [input, setInput] = useState("")
  const router = useRouter()
  const messagesEndRef = useRef<null | HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: input,
      avatar: "/placeholder-user.jpg",
    }
    setMessages((prev) => [...prev, userMessage])
    setInput("")

    // Simulate bot reply
    setTimeout(() => {
      const botMessage: Message = {
        id: Date.now() + 1,
        sender: "bot",
        text: "That's a great summary. To expand on sports, consistent training combined with this diet would yield the best results. What are your fitness goals?",
        avatar: "/placeholder-logo.svg",
      }
      setMessages((prev) => [...prev, botMessage])
    }, 1000)
  }

  return (
    <div className="flex flex-col h-screen bg-transparent text-gray-900 dark:text-white">
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 w-full max-w-4xl mx-auto">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800">
          <ChevronLeft className="w-6 h-6" />
        </Button>
        <div className="flex flex-col items-center">
          <h1 className="text-lg font-semibold">Text writer</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">Healthy eating tips</p>
        </div>
        <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800">
          <MoreVertical className="w-6 h-6" />
        </Button>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-6 w-full max-w-4xl mx-auto space-y-6">
        {messages.map((msg) => (
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
              <p className="text-sm">{msg.text}</p>
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
            placeholder="Send message..."
            className="flex-1 bg-transparent border-none focus:ring-0 text-gray-900 dark:text-white placeholder-gray-500 px-2"
          />
          <Button type="button" variant="ghost" size="icon" className="text-gray-500 dark:text-gray-400">
            <Mic className="w-5 h-5" />
          </Button>
          <Button type="submit" variant="ghost" size="icon" className="text-gray-500 dark:text-gray-400">
            <PlusCircle className="w-5 h-5" />
          </Button>
        </form>
      </footer>
    </div>
  )
} 