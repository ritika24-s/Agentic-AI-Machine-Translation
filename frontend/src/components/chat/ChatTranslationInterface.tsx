'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Send, Languages, Bot, User, Copy, Check, Loader2, Settings, Globe } from 'lucide-react'
import { motion } from 'framer-motion'
import { ChatMessage, AgentActivity } from '../../interface/chat'


const LANGUAGE_OPTIONS = [
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
  { code: 'ko', name: 'Korean', flag: '🇰🇷' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' }
]

const AGENTS = [
  { name: 'Intelligence Router', color: 'bg-blue-500', icon: '🧠' },
  { name: 'Context Manager', color: 'bg-purple-500', icon: '🧠' },
  { name: 'Translation Specialist', color: 'bg-green-500', icon: '🌍' },
  { name: 'Quality Guardian', color: 'bg-orange-500', icon: '✅' },
  { name: 'Results Synthesizer', color: 'bg-pink-500', icon: '📝' }
]

export default function ChatTranslationInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'system',
      content: 'Welcome! I\'m your AI translation assistant powered by intelligent agents. Send me any text and I\'ll translate it with professional quality. You can also upload documents for translation.',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [targetLang, setTargetLang] = useState('es')
  const [isTranslating, setIsTranslating] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null)
  const [currentAgentActivities, setCurrentAgentActivities] = useState<AgentActivity[]>([])
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`
    }
  }, [inputText])

  // Simulate agent activities during translation
  useEffect(() => {
    if (isTranslating) {
      setCurrentAgentActivities([])
      const activities: AgentActivity[] = []
      
      AGENTS.forEach((agent, index) => {
        setTimeout(() => {
          const activity: AgentActivity = {
            agent_name: agent.name,
            status: 'active',
            message: `Processing with ${agent.name}...`,
            timestamp: new Date().toISOString()
          }
          activities.push(activity)
          setCurrentAgentActivities([...activities])
          
          // Mark as completed
          setTimeout(() => {
            activity.status = 'completed'
            setCurrentAgentActivities([...activities])
          }, 1000)
        }, index * 600)
      })
    }
  }, [isTranslating])

  const handleSendMessage = async () => {
    if (!inputText.trim() || isTranslating) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputText,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsTranslating(true)

    try {
      // Call FastAPI translation endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: inputText,
          target_lang: targetLang,
          source_lang: 'auto'
        })
      })

      // Simulate processing time to show agent activities
      await new Promise(resolve => setTimeout(resolve, 3500))

      if (!response.ok) {
        throw new Error('Translation failed')
      }

      const result = await response.json()

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: result.translated_text || 'Translation completed!',
        translation: result.translated_text,
        metadata: {
          source_lang: result.source_language || 'auto',
          target_lang: result.target_language || targetLang,
          confidence_score: result.confidence_score || 0.95,
          quality_metrics: result.quality_metrics || {
            accuracy_score: 0.95,
            fluency_score: 0.92,
            adequacy_score: 0.94,
            overall_quality: 0.94
          },
          agent_activities: currentAgentActivities,
          processing_time: result.processing_time || 2.3
        },
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error during translation. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTranslating(false)
      setCurrentAgentActivities([])
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const copyToClipboard = async (text: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedMessageId(messageId)
      setTimeout(() => setCopiedMessageId(null), 2000)
    } catch (err) {
      console.error('Failed to copy text')
    }
  }

  const getQualityColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600'
    if (score >= 0.8) return 'text-yellow-600'
    return 'text-orange-600'
  }

  const selectedLanguage = LANGUAGE_OPTIONS.find(lang => lang.code === targetLang)

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Languages className="h-6 w-6 text-blue-600" />
              <h1 className="text-xl font-semibold text-gray-900">AI Translator</h1>
            </div>
            <div className="hidden sm:flex items-center gap-2 text-sm text-gray-600">
              <Globe className="h-4 w-4" />
              <span>Powered by intelligent agents</span>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Language Selector */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">To:</span>
              <select
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
                className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {LANGUAGE_OPTIONS.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Settings className="h-5 w-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.type !== 'user' && (
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <Bot className="h-5 w-5 text-white" />
                  </div>
                </div>
              )}

              <div className={`max-w-2xl ${message.type === 'user' ? 'order-first' : ''}`}>
                <div className={`p-4 rounded-2xl ${
                  message.type === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : message.type === 'system'
                    ? 'bg-gray-100 text-gray-700'
                    : 'bg-white border border-gray-200 shadow-sm'
                }`}>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  
                  {/* Translation Metadata */}
                  {message.metadata && (
                    <div className="mt-3 pt-3 border-t border-gray-100 space-y-2">
                      <div className="flex items-center justify-between text-xs text-gray-600">
                        <span>
                          {message.metadata.source_lang.toUpperCase()} → {message.metadata.target_lang.toUpperCase()}
                        </span>
                        <span>
                          Quality: <span className={getQualityColor(message.metadata.quality_metrics.overall_quality)}>
                            {Math.round(message.metadata.quality_metrics.overall_quality * 100)}%
                          </span>
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span>⚡ {message.metadata.processing_time}s</span>
                        <span>🎯 {Math.round(message.metadata.confidence_score * 100)}% confidence</span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Copy Button */}
                {message.type === 'assistant' && message.content && (
                  <div className="flex items-center gap-2 mt-2">
                    <button
                      onClick={() => copyToClipboard(message.content, message.id)}
                      className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded hover:bg-gray-100 transition-colors"
                    >
                      {copiedMessageId === message.id ? (
                        <>
                          <Check className="h-3 w-3" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" />
                          Copy
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>

              {message.type === 'user' && (
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                    <User className="h-5 w-5 text-gray-600" />
                  </div>
                </div>
              )}
            </motion.div>
          ))}

          {/* Agent Activity Indicator */}
          {isTranslating && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3"
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <Bot className="h-5 w-5 text-white" />
                </div>
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm">
                <div className="flex items-center gap-2 mb-3">
                  <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                  <span className="text-sm font-medium text-gray-900">AI agents are working...</span>
                </div>
                <div className="space-y-2">
                  {AGENTS.map((agent, index) => {
                    const activity = currentAgentActivities.find(a => a.agent_name === agent.name)
                    const status = activity?.status || 'waiting'
                    return (
                      <div key={agent.name} className="flex items-center gap-2 text-xs">
                        <div className={`w-2 h-2 rounded-full ${
                          status === 'completed' ? 'bg-green-500' :
                          status === 'active' ? 'bg-blue-500 animate-pulse' :
                          'bg-gray-300'
                        }`} />
                        <span className={status === 'waiting' ? 'text-gray-400' : 'text-gray-600'}>
                          {agent.icon} {agent.name}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3 items-end">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Type a message to translate to ${selectedLanguage?.name}...`}
                className="w-full resize-none border border-gray-300 rounded-2xl px-4 py-3 pr-12 focus:ring-2 focus:ring-blue-500 focus:border-transparent max-h-32"
                rows={1}
                disabled={isTranslating}
              />
              <div className="absolute right-3 bottom-3 text-xs text-gray-400">
                {inputText.length}/1000
              </div>
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isTranslating}
              className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isTranslating ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </div>
          
          <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
            <div className="flex items-center gap-4">
              <span>Press Enter to send, Shift+Enter for new line</span>
            </div>
            <div className="flex items-center gap-2">
              <span>Translating to {selectedLanguage?.flag} {selectedLanguage?.name}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}