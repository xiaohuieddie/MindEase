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
} from "lucide-react"

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
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-peach-50 to-cream-50">
      {/* Header */}
      <div className="flex items-center justify-between p-6 pt-12">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-500 rounded-full flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">MindEase</h1>
            <p className="text-xs text-gray-500">Anonymous • Secure</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="ghost" size="sm" className="w-10 h-10 p-0">
            <BarChart3 className="w-5 h-5 text-gray-600" />
          </Button>
          <Button variant="ghost" size="sm" className="w-10 h-10 p-0">
            <Settings className="w-5 h-5 text-gray-600" />
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-6 space-y-8">
        {/* Greeting Section */}
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold text-gray-900">{getGreeting()}</h2>
          <p className="text-gray-600">{getSubGreeting()}</p>
        </div>

        {/* Emotion Cloud */}
        <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">How are you feeling?</h3>
              <Badge variant="secondary" className="text-xs">
                Tap to select
              </Badge>
            </div>
            <div className="grid grid-cols-4 gap-3">
              {emotions.map((emotion) => (
                <button
                  key={emotion.label}
                  onClick={() => setSelectedEmotion(emotion.label)}
                  className={`p-3 rounded-xl transition-all duration-200 ${
                    selectedEmotion === emotion.label
                      ? "scale-110 shadow-lg " + emotion.color
                      : "bg-gray-50 hover:bg-gray-100"
                  }`}
                >
                  <div className="text-2xl mb-1">{emotion.emoji}</div>
                  <div className="text-xs font-medium text-gray-700">{emotion.label}</div>
                </button>
              ))}
            </div>
            {selectedEmotion && (
              <Button
                className="w-full mt-4 bg-orange-500 hover:bg-orange-600 text-white"
                onClick={() => {
                  /* Navigate to chat with emotion context */
                }}
              >
                Start conversation feeling {selectedEmotion.toLowerCase()}
                <ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Quick Start Options */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">Quick Start</h3>

          {/* Free-form Chat */}
          <Card className="border-0 shadow-lg bg-gradient-to-r from-orange-400 to-orange-500 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <MessageCircle className="w-6 h-6" />
                  <div>
                    <h4 className="font-semibold">{"What's on your mind?"}</h4>
                    <p className="text-sm opacity-90">Start a free-form conversation</p>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5" />
              </div>
            </CardContent>
          </Card>

          {/* Daily Topics */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-medium text-gray-900">Daily Topics</h4>
              <Badge variant="outline" className="text-xs">
                <Calendar className="w-3 h-3 mr-1" />
                Today
              </Badge>
            </div>
            {dailyTopics.map((topic, index) => (
              <Card key={index} className="border-0 shadow-md bg-white/80 backdrop-blur-sm">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div
                        className={`w-10 h-10 bg-gradient-to-r ${topic.gradient} rounded-lg flex items-center justify-center`}
                      >
                        <topic.icon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h5 className="font-medium text-gray-900">{topic.title}</h5>
                        <p className="text-sm text-gray-600">{topic.subtitle}</p>
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-400" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Wellness Tools */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">Quick Wellness</h3>
          <div className="grid grid-cols-1 gap-3">
            {quickPractices.map((practice, index) => (
              <Card key={index} className="border-0 shadow-md bg-white/80 backdrop-blur-sm">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 ${practice.color} rounded-lg flex items-center justify-center`}>
                        <practice.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h5 className="font-medium text-gray-900">{practice.title}</h5>
                        <div className="flex items-center space-x-2">
                          <Clock className="w-3 h-3 text-gray-500" />
                          <span className="text-sm text-gray-600">{practice.duration}</span>
                        </div>
                      </div>
                    </div>
                    <Button size="sm" variant="ghost" className="text-orange-600 hover:text-orange-700">
                      Start
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="space-y-4 pb-8">
          <h3 className="text-lg font-semibold text-gray-900">Your Journey</h3>
          <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="text-center space-y-4">
                <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-500 rounded-full flex items-center justify-center mx-auto">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">3 days streak</h4>
                  <p className="text-sm text-gray-600">{"You've been consistent with check-ins"}</p>
                </div>
                <Button variant="outline" className="w-full border-green-200 text-green-700 hover:bg-green-50">
                  View mood trends
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Bottom Navigation Hint */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-sm border-t border-gray-200 p-4">
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span>Anonymous session active</span>
          <Button variant="link" className="text-xs text-orange-600 p-0 h-auto">
            Save progress?
          </Button>
        </div>
      </div>
    </div>
  )
}
