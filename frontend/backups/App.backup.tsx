
import SensorCharts from './components/SensorCharts'

import {
  Thermometer,
  Gauge,
  AlertTriangle,
  Activity,
  BarChart3,
  Bot,
  Factory,
  LayoutDashboard,
  Settings,
} from 'lucide-react'

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex">

      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6">
        <div className="flex items-center gap-3 mb-10">
          <Factory className="text-cyan-400" size={30} />
          <h1 className="text-xl font-bold">Industrial AI</h1>
        </div>

        <nav className="space-y-3">
          <div className="flex items-center gap-3 rounded-lg bg-cyan-500/10 text-cyan-400 p-3">
            <LayoutDashboard size={20} />
            <span>Overview</span>
          </div>

          <div className="flex items-center gap-3 p-3 text-slate-400">
            <Activity size={20} />
            <span>Machines</span>
          </div>

          <div className="flex items-center gap-3 p-3 text-slate-400">
            <BarChart3 size={20} />
            <span>Analytics</span>
          </div>

          <div className="flex items-center gap-3 p-3 text-slate-400">
            <Bot size={20} />
            <span>AI Copilot</span>
          </div>

          <div className="flex items-center gap-3 p-3 text-slate-400">
            <Settings size={20} />
            <span>Settings</span>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1">

        {/* Header */}
        <header className="h-20 border-b border-slate-800 px-8 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Dashboard</h2>
            <p className="text-sm text-slate-400">
              Industrial Predictive Maintenance System
            </p>
          </div>

          <div className="flex items-center gap-2 text-emerald-400">
            <span className="h-2 w-2 rounded-full bg-emerald-400"></span>
            System Online
          </div>
        </header>

        {/* Dashboard Area */}
        <section className="p-8">
          <h3 className="text-xl font-semibold mb-2">
            Welcome to Industrial AI Copilot
          </h3>

          <p className="text-slate-400">
            Your machine monitoring workspace is ready.
          </p>

          <SensorCharts />
        </section>

      </main>
    </div>
  )
}

export default App

