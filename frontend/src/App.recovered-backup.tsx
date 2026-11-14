import { useEffect, useState } from 'react'
import {
  Activity,
  AlertTriangle,
  Bot,
  Factory,
  Gauge,
  LayoutDashboard,
  Settings,
  Thermometer,
  Zap,
} from 'lucide-react'

import SensorCharts from './components/SensorCharts'
import {
  getSensorReading,
  setSimulationMode,
  type SensorReading,
} from './services/api'

function App() {
  const [reading, setReading] = useState<SensorReading | null>(null)
  const [history, setHistory] = useState<
    { time: string; temperature: number; vibration: number }[]
  >([])
  const [connection, setConnection] = useState<'online' | 'offline'>('offline')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchReading = async () => {
    try {
      const data = await getSensorReading()
      setReading(data)
      setConnection('online')
      setError('')

      setHistory((previous) => [
        ...previous,
        {
          time: new Date(data.timestamp).toLocaleTimeString(),
          temperature: data.temperature_c,
          vibration: data.vibration_mm_s,
        },
      ].slice(-20))
    } catch {
      setConnection('offline')
      setError('Cannot connect to the backend. Check that FastAPI is running.')
    }
  }

  useEffect(() => {
    fetchReading()
    const interval = window.setInterval(fetchReading, 2000)

    return () => window.clearInterval(interval)
  }, [])

  const changeMode = async (mode: 'normal' | 'fault') => {
    setLoading(true)
    try {
      await setSimulationMode(mode)
      await fetchReading()
    } catch {
      setError('Could not change simulation mode.')
    } finally {
      setLoading(false)
    }
  }

  const cards = [
    {
      title: 'Temperature',
      value: reading ? `${reading.temperature_c} °C` : '--',
      icon: Thermometer,
      color: 'text-orange-400',
      description: 'Motor temperature',
    },
    {
      title: 'Vibration',
      value: reading ? `${reading.vibration_mm_s} mm/s` : '--',
      icon: Activity,
      color: 'text-cyan-400',
      description: 'Vibration level',
    },
    {
      title: 'Motor Speed',
      value: reading ? `${reading.rpm} RPM` : '--',
      icon: Gauge,
      color: 'text-violet-400',
      description: 'Rotational speed',
    },
    {
      title: 'Current',
      value: reading ? `${reading.current_a} A` : '--',
      icon: Zap,
      color: 'text-emerald-400',
      description: 'Electrical current',
    },
  ]

  const isFault = reading?.mode === 'fault'

  return (
    <div className="min-h-screen bg-slate-950 text-white flex">
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6 hidden md:block">
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
            <Gauge size={20} />
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

      <main className="flex-1 min-w-0">
        <header className="min-h-20 border-b border-slate-800 px-5 md:px-8 py-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-2xl font-semibold">Dashboard</h2>
            <p className="text-sm text-slate-400">
              Industrial Predictive Maintenance System
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className={`h-2 w-2 rounded-full ${
              connection === 'online' ? 'bg-emerald-400' : 'bg-red-400'
            }`} />
            <span className={connection === 'online' ? 'text-emerald-400' : 'text-red-400'}>
              {connection === 'online' ? 'Backend Online' : 'Backend Offline'}
            </span>
          </div>
        </header>

        <section className="p-5 md:p-8">
          <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
            <div>
              <h3 className="text-xl font-semibold">Machine Overview</h3>
              <p className="text-sm text-slate-400">
                Live synthetic motor telemetry
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => changeMode('normal')}
                disabled={loading}
                className="rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 px-4 py-2 text-sm font-medium"
              >
                Normal Mode
              </button>
              <button
                onClick={() => changeMode('fault')}
                disabled={loading}
                className="rounded-lg bg-red-600 hover:bg-red-500 disabled:opacity-50 px-4 py-2 text-sm font-medium"
              >
                Fault Mode
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-5 rounded-lg border border-red-800 bg-red-950/40 p-4 text-red-300 text-sm">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
            {cards.map((card) => {
              const Icon = card.icon
              return (
                <div
                  key={card.title}
                  className="rounded-xl border border-slate-800 bg-slate-900 p-5"
                >
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-slate-400">{card.title}</p>
                    <Icon className={card.color} size={23} />
                  </div>
                  <p className="text-2xl font-bold">{card.value}</p>
                  <p className="text-xs text-slate-500 mt-2">{card.description}</p>
                </div>
              )
            })}
          </div>

          <div className={`mt-6 rounded-xl border p-4 flex items-center gap-3 ${
            isFault
              ? 'border-red-800 bg-red-950/30 text-red-300'
              : 'border-emerald-800 bg-emerald-950/20 text-emerald-300'
          }`}>
            {isFault
              ? <AlertTriangle size={22} />
              : <Activity size={22} />}
            <div>
              <p className="font-semibold">
                {reading ? `Simulation Mode: ${reading.mode.toUpperCase()}` : 'Waiting for telemetry'}
              </p>
              <p className="text-xs opacity-80">
                {isFault
                  ? 'Synthetic fault scenario is active.'
                  : 'Synthetic normal scenario is active.'}
              </p>
            </div>
            <span className="ml-auto text-xs border border-current rounded-full px-3 py-1">
              SYNTHETIC DATA
            </span>
          </div>

          <SensorCharts data={history} />
        </section>
      </main>
    </div>
  )
}

export default App
