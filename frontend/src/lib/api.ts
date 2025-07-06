// lib/api.ts - FastAPI Integration
import { io, Socket } from 'socket.io-client'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

// Types matching your FastAPI Pydantic models
export interface TranslationRequest {
  text: string
  source_lang?: string
  target_lang: string
  context?: string
  domain?: string
  style?: 'formal' | 'informal' | 'technical'
}

export interface TranslationResponse {
  translated_text: string
  source_language: string
  target_language: string
  confidence_score: number
  agent_activities: AgentActivity[]
  quality_metrics: QualityMetrics
  translation_id: string
  processing_time: number
}

export interface AgentActivity {
  agent_name: string
  status: 'waiting' | 'active' | 'completed' | 'error'
  message: string
  timestamp: string
  details?: Record<string, any>
}

export interface QualityMetrics {
  accuracy_score: number
  fluency_score: number
  adequacy_score: number
  overall_quality: number
  mqm_score?: number
  error_count?: number
}

export interface ConversationContext {
  conversation_id: string
  messages: Array<{
    text: string
    translation: string
    timestamp: string
    language_pair: string
  }>
  terminology: Record<string, string>
  style_preferences: Record<string, any>
}

// API Client Class
export class TranslationAPI {
  private baseURL: string
  private socket: Socket | null = null

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Initialize WebSocket connection for real-time updates
  initializeWebSocket(onAgentUpdate?: (activity: AgentActivity) => void) {
    this.socket = io(WS_URL, {
      transports: ['websocket'],
      autoConnect: false
    })

    this.socket.on('agent_activity', (activity: AgentActivity) => {
      if (onAgentUpdate) onAgentUpdate(activity)
    })

    this.socket.on('translation_progress', (progress: { 
      translation_id: string
      progress: number
      current_agent: string 
    }) => {
      console.log('Translation progress:', progress)
    })

    this.socket.connect()
    return this.socket
  }

  // Disconnect WebSocket
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  // Main translation endpoint
  async translate(request: TranslationRequest): Promise<TranslationResponse> {
    const response = await fetch(`${this.baseURL}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `Translation failed: ${response.statusText}`)
    }

    return response.json()
  }

  // Batch translation for multiple texts
  async translateBatch(requests: TranslationRequest[]): Promise<TranslationResponse[]> {
    const response = await fetch(`${this.baseURL}/translate/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ translations: requests })
    })

    if (!response.ok) {
      throw new Error(`Batch translation failed: ${response.statusText}`)
    }

    return response.json()
  }

  // Get supported language pairs
  async getSupportedLanguages(): Promise<{ 
    languages: Array<{ code: string; name: string }>
    pairs: Array<{ source: string; target: string }>
  }> {
    const response = await fetch(`${this.baseURL}/languages`)
    if (!response.ok) {
      throw new Error('Failed to fetch supported languages')
    }
    return response.json()
  }

  // Upload document for translation
  async translateDocument(file: File, targetLang: string): Promise<{
    task_id: string
    status: string
    estimated_time: number
  }> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('target_lang', targetLang)

    const response = await fetch(`${this.baseURL}/translate/document`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error(`Document translation failed: ${response.statusText}`)
    }

    return response.json()
  }

  // Get document translation status
  async getDocumentStatus(taskId: string): Promise<{
    task_id: string
    status: 'pending' | 'processing' | 'completed' | 'error'
    progress: number
    result_url?: string
    error?: string
  }> {
    const response = await fetch(`${this.baseURL}/translate/document/${taskId}/status`)
    if (!response.ok) {
      throw new Error('Failed to get document status')
    }
    return response.json()
  }

  // Get conversation context
  async getConversationContext(conversationId: string): Promise<ConversationContext> {
    const response = await fetch(`${this.baseURL}/conversation/${conversationId}`)
    if (!response.ok) {
      throw new Error('Failed to get conversation context')
    }
    return response.json()
  }

  // Update conversation context
  async updateConversationContext(
    conversationId: string, 
    context: Partial<ConversationContext>
  ): Promise<ConversationContext> {
    const response = await fetch(`${this.baseURL}/conversation/${conversationId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(context)
    })

    if (!response.ok) {
      throw new Error('Failed to update conversation context')
    }

    return response.json()
  }

  // Get translation history
  async getTranslationHistory(limit: number = 50): Promise<TranslationResponse[]> {
    const response = await fetch(`${this.baseURL}/history?limit=${limit}`)
    if (!response.ok) {
      throw new Error('Failed to get translation history')
    }
    return response.json()
  }

  // Provide feedback on translation quality
  async provideFeedback(translationId: string, feedback: {
    rating: number // 1-5
    corrections?: string
    comments?: string
  }): Promise<{ message: string }> {
    const response = await fetch(`${this.baseURL}/feedback/${translationId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedback)
    })

    if (!response.ok) {
      throw new Error('Failed to submit feedback')
    }

    return response.json()
  }

  // Get agent performance metrics
  async getAgentMetrics(): Promise<{
    agents: Array<{
      name: string
      success_rate: number
      avg_processing_time: number
      total_translations: number
      quality_score: number
    }>
    system_metrics: {
      total_translations: number
      avg_quality_score: number
      avg_response_time: number
      uptime: number
    }
  }> {
    const response = await fetch(`${this.baseURL}/metrics/agents`)
    if (!response.ok) {
      throw new Error('Failed to get agent metrics')
    }
    return response.json()
  }
}

// Singleton instance
export const translationAPI = new TranslationAPI()

// React Hook for Translation API
import { useState, useEffect, useCallback } from 'react'

export function useTranslationAPI() {
  const [isConnected, setIsConnected] = useState(false)
  const [agentActivities, setAgentActivities] = useState<AgentActivity[]>([])

  useEffect(() => {
    const socket = translationAPI.initializeWebSocket((activity) => {
      setAgentActivities(prev => [...prev, activity])
    })

    socket.on('connect', () => setIsConnected(true))
    socket.on('disconnect', () => setIsConnected(false))

    return () => {
      translationAPI.disconnect()
    }
  }, [])

  const translate = useCallback(async (request: TranslationRequest) => {
    setAgentActivities([]) // Clear previous activities
    return translationAPI.translate(request)
  }, [])

  const clearActivities = useCallback(() => {
    setAgentActivities([])
  }, [])

  return {
    translate,
    translateBatch: translationAPI.translateBatch.bind(translationAPI),
    translateDocument: translationAPI.translateDocument.bind(translationAPI),
    getDocumentStatus: translationAPI.getDocumentStatus.bind(translationAPI),
    getSupportedLanguages: translationAPI.getSupportedLanguages.bind(translationAPI),
    getTranslationHistory: translationAPI.getTranslationHistory.bind(translationAPI),
    provideFeedback: translationAPI.provideFeedback.bind(translationAPI),
    getAgentMetrics: translationAPI.getAgentMetrics.bind(translationAPI),
    isConnected,
    agentActivities,
    clearActivities
  }
}

// Utility functions
export const formatLanguageName = (code: string): string => {
  const languages: Record<string, string> = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'ru': 'Russian'
  }
  return languages[code] || code.toUpperCase()
}

export const getQualityColor = (score: number): string => {
  if (score >= 0.9) return 'text-green-600'
  if (score >= 0.8) return 'text-yellow-600' 
  if (score >= 0.7) return 'text-orange-600'
  return 'text-red-600'
}

export const getQualityLabel = (score: number): string => {
  if (score >= 0.9) return 'Excellent'
  if (score >= 0.8) return 'Good'
  if (score >= 0.7) return 'Fair'
  return 'Needs Improvement'
}