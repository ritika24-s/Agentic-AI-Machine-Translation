// Types
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
  
export interface QualityMetrics {
    accuracy_score: number
    fluency_score: number
    adequacy_score: number
    overall_quality: number
}
  
export interface AgentActivity {
    agent_name: string
    status: 'waiting' | 'active' | 'completed' | 'error'
    message: string
    timestamp: string
}