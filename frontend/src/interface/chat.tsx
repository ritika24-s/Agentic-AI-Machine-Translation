// Types for chat messages
export interface ChatMessage {
    id: string
    type: 'user' | 'assistant' | 'system'
    content: string
    translation?: string
    metadata?: {
      source_lang: string
      target_lang: string
      confidence_score: number
      quality_metrics: QualityMetrics
      agent_activities: AgentActivity[]
      processing_time: number
    }
    timestamp: Date
    isDocument?: boolean
    documentName?: string
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
    style_preferences: Record<string, string>
  }