"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Heart,
  MessageCircle,
  TrendingUp,
  Sparkles,
  Calendar,
  Wind,
  Briefcase,
  Users,
  Clock,
  ChevronRight,
  Settings,
  BarChart3,
  Flame,
  ShieldCheck,
} from "lucide-react"
import { useRouter } from 'next/navigation'
import { ThemeToggle } from "@/components/ThemeToggle"

const emotions = [
  { emoji: "😊", label: "Happy", color: "bg-yellow-100 text-yellow-600" },
  { emoji: "😔", label: "Sad", color: "bg-blue-100 text-blue-600" },
  { emoji: "😰", label: "Anxious", color: "bg-purple-100 text-purple-600" },
  { emoji: "😤", label: "Frustrated", color: "bg-red-100 text-red-600" },
  { emoji: "😴", label: "Tired", color: "bg-gray-100 text-gray-600" },
  { emoji: "🤔", label: "Confused", color: "bg-indigo-100 text-indigo-600" },
  { emoji: "😌", label: "Calm", color: "bg-green-100 text-green-600" },
  { emoji: "🙃", label: "Mixed", color: "bg-orange-100 text-orange-600" },
]

const dailyTopics = [
  {
    title: "Monday Motivation",
    subtitle: "How are you starting your week?",
    icon: Sparkles,
    gradient: "from-orange-400 to-pink-400",
  },
  {
    title: "Workplace Stress",
    subtitle: "Dealing with deadline pressure",
    icon: Briefcase,
    gradient: "from-blue-400 to-purple-400",
  },
  {
    title: "Social Connections",
    subtitle: "Feeling isolated lately?",
    icon: Users,
    gradient: "from-green-400 to-teal-400",
  },
]

const quickPractices = [
  {
    title: "Breathing Exercise",
    duration: "3 min",
    icon: Wind,
    color: "bg-blue-50 text-blue-600",
  },
  {
    title: "Daily Affirmations",
    duration: "2 min",
    icon: Heart,
    color: "bg-pink-50 text-pink-600",
  },
  {
    title: "Stress Reframing",
    duration: "5 min",
    icon: TrendingUp,
    color: "bg-green-50 text-green-600",
  },
]

export default function MindEaseHomepage() {
  const [selectedEmotion, setSelectedEmotion] = useState<string | null>(null)
  const [currentTime] = useState(() => {
    const hour = new Date().getHours()
    if (hour < 12) return "morning"
    if (hour < 17) return "afternoon"
    return "evening"
  })
  const router = useRouter()

  const getGreeting = () => {
    const greetings = {
      morning: "Good morning!",
      afternoon: "Good afternoon!",
      evening: "Good evening!",
    }
    return greetings[currentTime as keyof typeof greetings]
  }

  const getSubGreeting = () => {
    const subGreetings = {
      morning: "How are you feeling as you start your day?",
      afternoon: "How's your day going so far?",
      evening: "How are you winding down today?",
    }
    return subGreetings[currentTime as keyof typeof subGreetings]
  }

  return (
    <div className="min-h-screen bg-transparent text-gray-900 dark:text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-6 pt-12">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">MindEase</h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">Anonymous • Secure</p>
          </div>
        </div>
        <div className="flex items-center space-x-1">
          <ThemeToggle />
          <Button variant="ghost" size="sm" className="w-10 h-10 p-0 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white">
            <BarChart3 className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="sm" className="w-10 h-10 p-0 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white">
            <Settings className="w-5 h-5" />
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-6 pb-12 space-y-8">
        {/* Greeting Section */}
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{getGreeting()}</h2>
          <p className="text-gray-600 dark:text-gray-400">{getSubGreeting()}</p>
        </div>

        {/* Emotion Cloud */}
        <Card className="border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">How are you feeling?</h3>
              <Badge variant="outline" className="text-xs border-gray-300 dark:border-gray-700 text-gray-500 dark:text-gray-400">
                Tap to select
              </Badge>
            </div>
            <div className="grid grid-cols-4 gap-3">
              {emotions.map((emotion) => (
                <button
                  key={emotion.label}
                  onClick={() => setSelectedEmotion(emotion.label)}
                  className={`p-3 rounded-xl transition-all duration-200 border border-gray-200 dark:border-gray-800 ${
                    selectedEmotion === emotion.label
                      ? "scale-110 shadow-lg bg-gradient-to-br from-pink-500 to-purple-600 text-white"
                      : "bg-gray-100 dark:bg-gray-800/50 hover:bg-gray-200 dark:hover:bg-gray-800"
                  }`}
                >
                  <div className="text-2xl mb-1">{emotion.emoji}</div>
                  <div className="text-xs font-medium text-gray-700 dark:text-gray-300">{emotion.label}</div>
                </button>
              ))}
            </div>
            {selectedEmotion && (
              <Button
                className="w-full mt-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white"
                onClick={() => router.push('/chat')}
              >
                Start conversation feeling {selectedEmotion.toLowerCase()}
                <ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Quick Start Options */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Quick Start</h3>

          {/* Free-form Chat */}
          <Card
            className="border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
            onClick={() => router.push('/chat')}
          >
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <MessageCircle className="w-6 h-6 text-purple-500 dark:text-purple-400" />
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white">{"What's on your mind?"}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Start a free-form conversation</p>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400 dark:text-gray-600" />
              </div>
            </CardContent>
          </Card>

          {/* Daily Topics */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white">Daily Topics</h4>
              <Badge variant="outline" className="text-xs border-gray-300 dark:border-gray-700 text-gray-500 dark:text-gray-400">
                <Calendar className="w-3 h-3 mr-1" />
                Today
              </Badge>
            </div>
            {dailyTopics.map((topic, index) => (
              <Card key={index} className="border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div
                        className={`w-10 h-10 bg-gradient-to-r ${topic.gradient} rounded-lg flex items-center justify-center`}
                      >
                        <topic.icon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h5 className="font-medium text-gray-900 dark:text-white">{topic.title}</h5>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{topic.subtitle}</p>
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-500 dark:text-gray-700" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Wellness Tools */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Your Journey</h3>
          <div className="grid grid-cols-1 gap-3">
            {quickPractices.map((practice, index) => (
              <Card key={index} className="border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 ${practice.color} rounded-lg flex items-center justify-center`}>
                        <practice.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h5 className="font-medium text-gray-900 dark:text-white">{practice.title}</h5>
                        <div className="flex items-center space-x-2">
                          <Clock className="w-3 h-3 text-gray-500" />
                          <span className="text-sm text-gray-600 dark:text-gray-400">{practice.duration}</span>
                        </div>
                      </div>
                    </div>
                    <Button size="sm" variant="ghost" className="text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300">
                      Start
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
            <Card className="border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center">
                      <Flame className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h5 className="font-medium text-gray-900 dark:text-white">3-day streak!</h5>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Keep it up for a week for a surprise</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="sticky bottom-0 p-4 backdrop-blur-md bg-white/30 dark:bg-black/30 border-t border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
          <ShieldCheck className="w-4 h-4 text-green-500" />
          <span>Anonymous session active. Your data is safe.</span>
          <Button variant="link" className="text-xs text-purple-600 dark:text-purple-500 p-0 h-auto">
            Save progress?
          </Button>
        </div>
      </div>
    </div>
  )
}
