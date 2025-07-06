'use client'

import React, { useState, useRef, useCallback } from 'react'
import { 
  Upload, FileText, File, Image, Download, X, CheckCircle, 
  AlertCircle, Clock, Loader2, Eye, Trash2, Globe, Settings 
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { UploadedFile, AgentActivity } from '../../interface/document'


const SUPPORTED_FORMATS = {
  'application/pdf': { name: 'PDF', icon: '📄', color: 'text-red-600' },
  'application/msword': { name: 'DOC', icon: '📝', color: 'text-blue-600' },
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { name: 'DOCX', icon: '📝', color: 'text-blue-600' },
  'text/plain': { name: 'TXT', icon: '📄', color: 'text-gray-600' },
  'application/vnd.ms-powerpoint': { name: 'PPT', icon: '📊', color: 'text-orange-600' },
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': { name: 'PPTX', icon: '📊', color: 'text-orange-600' },
  'text/csv': { name: 'CSV', icon: '📈', color: 'text-green-600' },
  'application/vnd.ms-excel': { name: 'XLS', icon: '📈', color: 'text-green-600' },
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': { name: 'XLSX', icon: '📈', color: 'text-green-600' }
}

const LANGUAGE_OPTIONS = [
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
  { code: 'ko', name: 'Korean', flag: '🇰🇷' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' }
]

const AGENTS = [
  { name: 'Intelligence Router', icon: '🧠', color: 'bg-blue-500' },
  { name: 'Context Manager', icon: '🧠', color: 'bg-purple-500' },
  { name: 'Translation Specialist', icon: '🌍', color: 'bg-green-500' },
  { name: 'Quality Guardian', icon: '✅', color: 'bg-orange-500' },
  { name: 'Results Synthesizer', icon: '📝', color: 'bg-pink-500' }
]

export default function DocumentUploadSystem() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [defaultTargetLang, setDefaultTargetLang] = useState('es')
  const [isDragOver, setIsDragOver] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (type: string) => {
    return SUPPORTED_FORMATS[type as keyof typeof SUPPORTED_FORMATS]?.icon || '📄'
  }

  const getFileColor = (type: string) => {
    return SUPPORTED_FORMATS[type as keyof typeof SUPPORTED_FORMATS]?.color || 'text-gray-600'
  }

  const simulateAgentActivities = (fileId: string) => {
    let activities: AgentActivity[] = []
    
    AGENTS.forEach((agent, index) => {
      setTimeout(() => {
        const activity: AgentActivity = {
          agent_name: agent.name,
          status: 'active',
          message: `Processing document with ${agent.name}...`,
          timestamp: new Date().toISOString()
        }
        activities.push(activity)
        
        setFiles(prev => prev.map(f => 
          f.id === fileId 
            ? { ...f, agent_activities: [...activities] }
            : f
        ))
        
        // Mark as completed
        setTimeout(() => {
          activity.status = 'completed'
          setFiles(prev => prev.map(f => 
            f.id === fileId 
              ? { ...f, agent_activities: [...activities] }
              : f
          ))
        }, 1200)
      }, index * 800)
    })
  }

  const simulateFileProcessing = async (uploadedFile: UploadedFile) => {
    const fileId = uploadedFile.id

    // Start agent activities
    simulateAgentActivities(fileId)

    // Upload progress
    for (let progress = 0; progress <= 100; progress += 10) {
      await new Promise(resolve => setTimeout(resolve, 100))
      setFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, uploadProgress: progress, progress: progress * 0.3 }
          : f
      ))
    }

    // Set to translating
    setFiles(prev => prev.map(f => 
      f.id === fileId 
        ? { 
            ...f, 
            status: 'translating',
            estimated_time: Math.floor(Math.random() * 120) + 30 // 30-150 seconds
          }
        : f
    ))

    // Translation progress
    for (let progress = 0; progress <= 100; progress += 5) {
      await new Promise(resolve => setTimeout(resolve, 150))
      setFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { 
              ...f, 
              translationProgress: progress,
              progress: 30 + (progress * 0.7)
            }
          : f
      ))
    }

    // Complete the translation
    setFiles(prev => prev.map(f => 
      f.id === fileId 
        ? { 
            ...f, 
            status: 'completed',
            progress: 100,
            result: {
              translated_url: '#',
              original_url: '#',
              translation_id: `trans_${Date.now()}`,
              quality_score: 0.92 + Math.random() * 0.07,
              processing_time: 45 + Math.random() * 60,
              page_count: Math.floor(Math.random() * 50) + 1,
              word_count: Math.floor(Math.random() * 5000) + 500
            }
          }
        : f
    ))
  }

  const handleFileUpload = useCallback((selectedFiles: FileList | null) => {
    if (!selectedFiles) return

    Array.from(selectedFiles).forEach(file => {
      if (!Object.keys(SUPPORTED_FORMATS).includes(file.type)) {
        alert(`Unsupported file type: ${file.type}`)
        return
      }

      const uploadedFile: UploadedFile = {
        id: `${Date.now()}_${Math.random()}`,
        file,
        name: file.name,
        size: formatFileSize(file.size),
        type: file.type,
        status: 'uploading',
        progress: 0,
        uploadProgress: 0,
        translationProgress: 0,
        targetLang: defaultTargetLang
      }

      setFiles(prev => [...prev, uploadedFile])
      simulateFileProcessing(uploadedFile)
    })
  }, [defaultTargetLang])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    handleFileUpload(e.dataTransfer.files)
  }, [handleFileUpload])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const retryTranslation = (fileId: string) => {
    const file = files.find(f => f.id === fileId)
    if (file) {
      const updatedFile = {
        ...file,
        status: 'uploading' as const,
        progress: 0,
        uploadProgress: 0,
        translationProgress: 0,
        error: undefined
      }
      setFiles(prev => prev.map(f => f.id === fileId ? updatedFile : f))
      simulateFileProcessing(updatedFile)
    }
  }

  const downloadFile = (url: string, filename: string) => {
    // In a real app, this would download the actual file
    console.log(`Downloading: ${filename} from ${url}`)
    alert(`Download started: ${filename}`)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
      case 'queued':
      case 'translating':
        return <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-600" />
      default:
        return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusText = (file: UploadedFile) => {
    switch (file.status) {
      case 'uploading':
        return 'Uploading...'
      case 'queued':
        return 'Queued for translation'
      case 'translating':
        return `Translating... ${file.estimated_time ? `(~${file.estimated_time}s remaining)` : ''}`
      case 'completed':
        return 'Translation completed'
      case 'error':
        return file.error || 'Translation failed'
      default:
        return 'Unknown status'
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Upload className="h-6 w-6 text-blue-600" />
            Document Translation
          </h1>
          <p className="text-gray-600 mt-1">Upload documents for AI-powered translation</p>
        </div>
        
        <div className="flex items-center gap-3">
          <select
            value={defaultTargetLang}
            onChange={(e) => setDefaultTargetLang(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {LANGUAGE_OPTIONS.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Settings className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Upload Area */}
      <motion.div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
          isDragOver 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400 bg-white'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
      >
        <div className="flex flex-col items-center gap-4">
          <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
            isDragOver ? 'bg-blue-100' : 'bg-gray-100'
          }`}>
            <Upload className={`h-8 w-8 ${isDragOver ? 'text-blue-600' : 'text-gray-400'}`} />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {isDragOver ? 'Drop files here' : 'Upload documents'}
            </h3>
            <p className="text-gray-600 mt-1">
              Drag and drop files or{' '}
              <button
                onClick={() => fileInputRef.current?.click()}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                browse to upload
              </button>
            </p>
          </div>
          
          <div className="flex flex-wrap gap-2 text-xs text-gray-500">
            {Object.values(SUPPORTED_FORMATS).map((format, index) => (
              <span key={index} className="px-2 py-1 bg-gray-100 rounded">
                {format.name}
              </span>
            ))}
          </div>
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={Object.keys(SUPPORTED_FORMATS).join(',')}
          onChange={(e) => handleFileUpload(e.target.files)}
          className="hidden"
        />
      </motion.div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">
            Files ({files.length})
          </h2>
          
          <div className="space-y-3">
            <AnimatePresence>
              {files.map((file) => (
                <motion.div
                  key={file.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm"
                >
                  <div className="flex items-start gap-4">
                    {/* File Icon */}
                    <div className={`text-2xl ${getFileColor(file.type)}`}>
                      {getFileIcon(file.type)}
                    </div>
                    
                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-gray-900 truncate">
                          {file.name}
                        </h3>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(file.status)}
                          <button
                            onClick={() => removeFile(file.id)}
                            className="text-gray-400 hover:text-gray-600 p-1"
                          >
                            <X className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                        <span>{file.size}</span>
                        <span>→ {LANGUAGE_OPTIONS.find(l => l.code === file.targetLang)?.name}</span>
                        <span>{getStatusText(file)}</span>
                      </div>
                      
                      {/* Progress Bar */}
                      {(file.status === 'uploading' || file.status === 'translating') && (
                        <div className="mt-3">
                          <div className="flex justify-between text-xs text-gray-600 mb-1">
                            <span>
                              {file.status === 'uploading' ? 'Upload' : 'Translation'} Progress
                            </span>
                            <span>{Math.round(file.progress)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <motion.div
                              className="bg-blue-600 h-2 rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${file.progress}%` }}
                              transition={{ duration: 0.3 }}
                            />
                          </div>
                        </div>
                      )}
                      
                      {/* Agent Activities */}
                      {file.agent_activities && file.agent_activities.length > 0 && (
                        <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                          <div className="text-xs font-medium text-gray-700 mb-2">
                            Agent Activity:
                          </div>
                          <div className="space-y-1">
                            {AGENTS.map(agent => {
                              const activity = file.agent_activities?.find(a => a.agent_name === agent.name)
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
                      )}
                      
                      {/* Translation Results */}
                      {file.status === 'completed' && file.result && (
                        <div className="mt-3 p-3 bg-green-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-green-800">
                              Translation Complete
                            </span>
                            <span className="text-xs text-green-600">
                              Quality: {Math.round(file.result.quality_score * 100)}%
                            </span>
                          </div>
                          
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs text-green-700 mb-3">
                            <div>Pages: {file.result.page_count}</div>
                            <div>Words: {file.result.word_count?.toLocaleString()}</div>
                            <div>Time: {Math.round(file.result.processing_time)}s</div>
                            <div>ID: {file.result.translation_id.slice(-6)}</div>
                          </div>
                          
                          <div className="flex gap-2">
                            <button
                              onClick={() => downloadFile(file.result!.translated_url, `translated_${file.name}`)}
                              className="flex items-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded text-xs hover:bg-green-700 transition-colors"
                            >
                              <Download className="h-3 w-3" />
                              Download Translation
                            </button>
                            <button
                              onClick={() => downloadFile(file.result!.original_url, file.name)}
                              className="flex items-center gap-1 px-3 py-1.5 bg-gray-600 text-white rounded text-xs hover:bg-gray-700 transition-colors"
                            >
                              <Eye className="h-3 w-3" />
                              View Original
                            </button>
                          </div>
                        </div>
                      )}
                      
                      {/* Error State */}
                      {file.status === 'error' && (
                        <div className="mt-3 p-3 bg-red-50 rounded-lg">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-red-800">
                              Translation Failed
                            </span>
                            <button
                              onClick={() => retryTranslation(file.id)}
                              className="text-xs text-red-600 hover:text-red-700 font-medium"
                            >
                              Retry
                            </button>
                          </div>
                          {file.error && (
                            <p className="text-xs text-red-600 mt-1">{file.error}</p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      )}
      
      {/* Empty State */}
      {files.length === 0 && (
        <div className="text-center py-12">
          <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No documents uploaded</h3>
          <p className="text-gray-600">
            Upload your first document to get started with AI translation
          </p>
        </div>
      )}
    </div>
  )
}