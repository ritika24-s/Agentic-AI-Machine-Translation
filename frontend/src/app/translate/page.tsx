'use client'

import React, { useState, useEffect } from 'react'
import { Send, Languages, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

// Types matching your FastAPI backend
interface TranslationRequest {
  text: string
  source_lang?: string
  target_lang: string
  context?: string
}

interface TranslationResponse {
  translated_text: string
  source_language: string
  target_language: string
  confidence_score: number
  agent_activities: AgentActivity[]
  quality_metrics: QualityMetrics
}

interface AgentActivity {
  agent_name: string
  status: 'active' | 'completed' | 'waiting'
  message: string
  timestamp: string
}

interface QualityMetrics {
  accuracy_score: number
  fluency_score: number
  adequacy_score: number
  overall_quality: number
}

const AGENTS = [
  { name: 'Intelligence Router', color: 'bg-blue-500', role: 'Analyzing text complexity' },
  { name: 'Context Manager', color: 'bg-purple-500', role: 'Managing conversation context' },
  { name: 'Translation Specialist', color: 'bg-green-500', role: 'Performing translation' },
  { name: 'Quality Guardian', color: 'bg-orange-500', role: 'Quality assurance' },
  { name: 'Results Synthesizer', color: 'bg-pink-500', role: 'Finalizing results' }
]

export default function TranslationInterface() {
  const [inputText, setInputText] = useState('')
  const [targetLang, setTargetLang] = useState('es')
  const [translation, setTranslation] = useState<TranslationResponse | null>(null)
  const [isTranslating, setIsTranslating] = useState(false)
  const [agentActivities, setAgentActivities] = useState<AgentActivity[]>([])
  const [error, setError] = useState<string | null>(null)

  // Simulate real-time agent updates (replace with actual WebSocket)
  useEffect(() => {
    if (isTranslating) {
      const intervals: NodeJS.Timeout[] = []
      
      AGENTS.forEach((agent, index) => {
        const timeout = setTimeout(() => {
          setAgentActivities(prev => [
            ...prev,
            {
              agent_name: agent.name,
              status: 'active',
              message: agent.role,
              timestamp: new Date().toISOString()
            }
          ])
          
          // Mark as completed after 1 second
          setTimeout(() => {
            setAgentActivities(prev => 
              prev.map(activity => 
                activity.agent_name === agent.name 
                  ? { ...activity, status: 'completed' }
                  : activity
              )
            )
          }, 1000)
        }, index * 800)
        
        intervals.push(timeout)
      })
      
      return () => intervals.forEach(clearTimeout)
    }
  }, [isTranslating])

  const handleTranslate = async () => {
    if (!inputText.trim()) return

    setIsTranslating(true)
    setError(null)
    setAgentActivities([])
    setTranslation(null)

    try {
      // Call your FastAPI backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          target_lang: targetLang,
          source_lang: 'auto' // Let your agents detect
        } as TranslationRequest)
      })

      if (!response.ok) {
        throw new Error(`Translation failed: ${response.statusText}`)
      }

      const result: TranslationResponse = await response.json()
      
      // Simulate processing time to show agents working
      setTimeout(() => {
        setTranslation(result)
        setIsTranslating(false)
      }, 4000)

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Translation failed')
      setIsTranslating(false)
    }
  }

  const getAgentStatus = (agentName: string) => {
    const activity = agentActivities.find(a => a.agent_name === agentName)
    return activity?.status || 'waiting'
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center justify-center gap-2">
          <Languages className="h-8 w-8 text-blue-600" />
          Agentic AI Translator
        </h1>
        <p className="text-gray-600">Powered by intelligent agent collaboration</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Translation Input/Output */}
        <div className="lg:col-span-2 space-y-4">
          {/* Input Section */}
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
            <div className="p-4 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">
                  Source Text
                </label>
                <select 
                  value={targetLang} 
                  onChange={(e) => setTargetLang(e.target.value)}
                  className="text-sm border border-gray-300 rounded px-2 py-1"
                >
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="it">Italian</option>
                  <option value="pt">Portuguese</option>
                </select>
              </div>
            </div>
            <div className="p-4">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter text to translate..."
                className="w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isTranslating}
              />
              <div className="flex justify-between items-center mt-3">
                <span className="text-sm text-gray-500">
                  {inputText.length} characters
                </span>
                <button
                  onClick={handleTranslate}
                  disabled={!inputText.trim() || isTranslating}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isTranslating ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                  Translate
                </button>
              </div>
            </div>
          </div>

          {/* Translation Result */}
          {(translation || isTranslating) && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-gray-200 shadow-sm"
            >
              <div className="p-4 border-b border-gray-100">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-700">
                    Translation
                  </label>
                  {translation && (
                    <div className="flex items-center gap-2 text-sm text-green-600">
                      <CheckCircle className="h-4 w-4" />
                      {Math.round(translation.quality_metrics.overall_quality * 100)}% Quality
                    </div>
                  )}
                </div>
              </div>
              <div className="p-4">
                {isTranslating ? (
                  <div className="h-32 flex items-center justify-center text-gray-500">
                    <div className="text-center">
                      <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2" />
                      Processing with AI agents...
                    </div>
                  </div>
                ) : translation ? (
                  <div className="space-y-3">
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-gray-900">{translation.translated_text}</p>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                      <div>
                        <span className="text-gray-500">Accuracy:</span>
                        <span className="ml-1 font-medium">
                          {Math.round(translation.quality_metrics.accuracy_score * 100)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-500">Fluency:</span>
                        <span className="ml-1 font-medium">
                          {Math.round(translation.quality_metrics.fluency_score * 100)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-500">Confidence:</span>
                        <span className="ml-1 font-medium">
                          {Math.round(translation.confidence_score * 100)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-500">Languages:</span>
                        <span className="ml-1 font-medium">
                          {translation.source_language} → {translation.target_language}
                        </span>
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>
            </motion.div>
          )}

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-50 border border-red-200 rounded-lg p-4"
            >
              <div className="flex items-center gap-2 text-red-700">
                <AlertCircle className="h-5 w-5" />
                <span className="font-medium">Translation Error</span>
              </div>
              <p className="text-red-600 mt-1">{error}</p>
            </motion.div>
          )}
        </div>

        {/* Agent Activity Panel */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="p-4 border-b border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900">Agent Activity</h3>
            <p className="text-sm text-gray-600">Real-time agent collaboration</p>
          </div>
          <div className="p-4 space-y-3">
            {AGENTS.map((agent, index) => {
              const status = getAgentStatus(agent.name)
              return (
                <motion.div
                  key={agent.name}
                  initial={{ opacity: 0.3 }}
                  animate={{ 
                    opacity: status === 'waiting' ? 0.4 : 1,
                    scale: status === 'active' ? 1.02 : 1
                  }}
                  className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                    status === 'active' ? 'bg-blue-50 border-blue-200' :
                    status === 'completed' ? 'bg-green-50 border-green-200' :
                    'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div className={`w-3 h-3 rounded-full ${agent.color} ${
                    status === 'active' ? 'animate-pulse' : ''
                  }`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {agent.name}
                    </p>
                    <p className="text-xs text-gray-600 truncate">
                      {agent.role}
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    {status === 'completed' && (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    )}
                    {status === 'active' && (
                      <Loader2 className="h-4 w-4 text-blue-600 animate-spin" />
                    )}
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}