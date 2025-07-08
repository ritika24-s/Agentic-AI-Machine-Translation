import { AgentActivity, QualityMetrics } from "./chat"

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

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