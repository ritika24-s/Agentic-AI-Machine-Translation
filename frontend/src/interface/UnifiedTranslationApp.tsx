type TabType = 'chat' | 'documents' | 'history' | 'analytics' | 'settings'

export interface Tab {
  id: TabType
  name: string
  icon: React.ReactNode
  description: string
  component: React.ReactNode
}