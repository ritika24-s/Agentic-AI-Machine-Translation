// Types for document upload and processing
export interface UploadedFile {
    id: string
    file: File
    name: string
    size: string
    type: string
    status: 'uploading' | 'queued' | 'translating' | 'completed' | 'error'
    progress: number
    uploadProgress: number
    translationProgress: number
    targetLang: string
    result?: {
        translated_url: string
        original_url: string
        translation_id: string
        quality_score: number
        processing_time: number
        page_count?: number
        word_count?: number
    }
    error?: string
    agent_activities?: AgentActivity[]
    estimated_time?: number
}

export interface AgentActivity {
    agent_name: string
    status: 'waiting' | 'active' | 'completed' | 'error'
    message: string
    timestamp: string
}