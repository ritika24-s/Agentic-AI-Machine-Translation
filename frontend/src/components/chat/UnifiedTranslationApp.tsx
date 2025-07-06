'use client'

import React, { useState } from 'react'
import { MessageSquare, Upload, Settings, BarChart3, History, Languages, Bot } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

import { Tab } from '../../interface/UnifiedTranslationApp'
import ChatTranslationInterface from './ChatTranslationInterface'
import DocumentUploadSystem from './DocumentUploadSystem'



const TABS: Tab[] = [
  {
    id: 'chat',
    name: 'Chat Translation',
    icon: <MessageSquare className="h-5 w-5" />,
    description: 'Conversational translation interface',
    component: <ChatTranslationInterface />
  },
  {
    id: 'documents',
    name: 'Document Upload',
    icon: <Upload className="h-5 w-5" />,
    description: 'Upload and translate documents',
    component: <DocumentUploadSystem />
  },
  {
    id: 'history',
    name: 'Translation History',
    icon: <History className="h-5 w-5" />,
    description: 'View past translations',
    component: (
      <div className="h-full flex items-center justify-center bg-gray-50 rounded-lg">
        <div className="text-center">
          <History className="h-12 w-12 text-purple-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Translation History</h3>
          <p className="text-gray-600">View and manage your translation history</p>
        </div>
      </div>
    )
  },
  {
    id: 'analytics',
    name: 'Agent Analytics',
    icon: <BarChart3 className="h-5 w-5" />,
    description: 'Monitor agent performance',
    component: (
      <div className="h-full bg-white rounded-lg p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Agent Performance Dashboard</h2>
          <p className="text-gray-600">Real-time insights into your AI agent collaboration</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          {/* Agent Performance Cards */}
          {[
            { name: 'Intelligence Router', accuracy: 98.5, tasks: 1247, status: 'active' },
            { name: 'Context Manager', accuracy: 97.2, tasks: 1189, status: 'active' },
            { name: 'Translation Specialist', accuracy: 96.8, tasks: 1156, status: 'active' },
            { name: 'Quality Guardian', accuracy: 99.1, tasks: 1098, status: 'active' },
            { name: 'Results Synthesizer', accuracy: 97.9, tasks: 1203, status: 'active' }
          ].map((agent, index) => (
            <div key={agent.name} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-medium text-gray-900 text-sm">{agent.name}</h3>
                <div className={`w-2 h-2 rounded-full ${
                  agent.status === 'active' ? 'bg-green-500' : 'bg-gray-400'
                }`} />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-600">Accuracy</span>
                  <span className="font-medium text-green-600">{agent.accuracy}%</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-600">Tasks Completed</span>
                  <span className="font-medium">{agent.tasks.toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* System Metrics */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 mb-4">System Metrics</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Translations</span>
                <span className="font-medium">5,893</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Quality Score</span>
                <span className="font-medium text-green-600">97.5%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Response Time</span>
                <span className="font-medium">2.3s</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">System Uptime</span>
                <span className="font-medium text-green-600">99.9%</span>
              </div>
            </div>
          </div>
          
          {/* Recent Activity */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Recent Activity</h3>
            <div className="space-y-3">
              {[
                { time: '2 min ago', action: 'Document translated', lang: 'EN → ES' },
                { time: '5 min ago', action: 'Chat translation', lang: 'FR → EN' },
                { time: '8 min ago', action: 'Batch processing', lang: 'DE → IT' },
                { time: '12 min ago', action: 'Quality review', lang: 'JA → EN' }
              ].map((activity, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <div>
                    <span className="text-gray-900">{activity.action}</span>
                    <span className="text-gray-500 ml-2">({activity.lang})</span>
                  </div>
                  <span className="text-gray-500 text-xs">{activity.time}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'settings',
    name: 'Settings',
    icon: <Settings className="h-5 w-5" />,
    description: 'Configure translation preferences',
    component: (
      <div className="h-full bg-white rounded-lg p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Translation Settings</h2>
          <p className="text-gray-600">Configure your translation preferences and agent behavior</p>
        </div>
        
        <div className="space-y-6">
          {/* Language Preferences */}
          <div className="border-b border-gray-200 pb-6">
            <h3 className="font-medium text-gray-900 mb-4">Language Preferences</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Source Language
                </label>
                <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option>Auto-detect</option>
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Target Language
                </label>
                <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option>Spanish</option>
                  <option>English</option>
                  <option>French</option>
                  <option>German</option>
                </select>
              </div>
            </div>
          </div>
          
          {/* Quality Settings */}
          <div className="border-b border-gray-200 pb-6">
            <h3 className="font-medium text-gray-900 mb-4">Quality Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quality Threshold
                </label>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="70"
                    max="99"
                    defaultValue="85"
                    className="flex-1"
                  />
                  <span className="text-sm text-gray-600 w-12">85%</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Translations below this quality will be automatically retried
                </p>
              </div>
              
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="auto-retry"
                  defaultChecked
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="auto-retry" className="text-sm text-gray-700">
                  Automatically retry low-quality translations
                </label>
              </div>
              
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="human-review"
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="human-review" className="text-sm text-gray-700">
                  Request human review for critical documents
                </label>
              </div>
            </div>
          </div>
          
          {/* Agent Configuration */}
          <div className="border-b border-gray-200 pb-6">
            <h3 className="font-medium text-gray-900 mb-4">Agent Configuration</h3>
            <div className="space-y-3">
              {[
                { name: 'Intelligence Router', description: 'Analyzes text complexity and routing' },
                { name: 'Context Manager', description: 'Manages conversation context and consistency' },
                { name: 'Translation Specialist', description: 'Performs the actual translation' },
                { name: 'Quality Guardian', description: 'Reviews and validates translation quality' },
                { name: 'Results Synthesizer', description: 'Finalizes and optimizes results' }
              ].map((agent) => (
                <div key={agent.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">{agent.name}</h4>
                    <p className="text-xs text-gray-600">{agent.description}</p>
                  </div>
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    Configure
                  </button>
                </div>
              ))}
            </div>
          </div>
          
          {/* API Settings */}
          <div>
            <h3 className="font-medium text-gray-900 mb-4">API Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Rate Limit
                </label>
                <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option>100 requests/minute</option>
                  <option>500 requests/minute</option>
                  <option>1000 requests/minute</option>
                  <option>Unlimited</option>
                </select>
              </div>
              
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="cache-translations"
                  defaultChecked
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="cache-translations" className="text-sm text-gray-700">
                  Cache translations for faster repeated requests
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
]

export default function UnifiedTranslationApp() {
  const [activeTab, setActiveTab] = useState<TabType>('chat')
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const activeTabData = TABS.find(tab => tab.id === activeTab)

  return (
    <div className="h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <motion.div
        className={`bg-white border-r border-gray-200 flex flex-col ${
          sidebarCollapsed ? 'w-16' : 'w-64'
        }`}
        animate={{ width: sidebarCollapsed ? 64 : 256 }}
        transition={{ duration: 0.3 }}
      >
        {/* Logo/Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Languages className="h-5 w-5 text-white" />
            </div>
            {!sidebarCollapsed && (
              <div>
                <h1 className="font-semibold text-gray-900">AI Translator</h1>
                <p className="text-xs text-gray-600">Powered by agents</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <div className="space-y-2">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <div className="flex-shrink-0">
                  {tab.icon}
                </div>
                {!sidebarCollapsed && (
                  <div>
                    <div className="font-medium text-sm">{tab.name}</div>
                    <div className="text-xs text-gray-500">{tab.description}</div>
                  </div>
                )}
              </button>
            ))}
          </div>
        </nav>

        {/* Sidebar Toggle */}
        <div className="p-4 border-t border-gray-200">
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="w-full flex items-center justify-center p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <motion.div
              animate={{ rotate: sidebarCollapsed ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </motion.div>
          </button>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                {activeTabData?.name}
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                {activeTabData?.description}
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              {/* Status Indicator */}
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span>All agents active</span>
              </div>
              
              {/* Agent Count */}
              <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 rounded-lg text-sm">
                <Bot className="h-4 w-4 text-gray-600" />
                <span className="text-gray-700">5 agents online</span>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="h-full"
            >
              {activeTabData?.component}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}