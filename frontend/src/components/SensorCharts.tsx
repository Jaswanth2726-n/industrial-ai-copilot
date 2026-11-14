import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

interface SensorChartPoint {
  time: string
  temperature: number
  vibration: number
}

interface SensorChartsProps {
  data: SensorChartPoint[]
}

function SensorCharts({ data }: SensorChartsProps) {
  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 mt-8">
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
        <h3 className="text-lg font-semibold mb-1">Temperature Trend</h3>
        <p className="text-sm text-slate-400 mb-5">
          Live synthetic temperature readings (°C)
        </p>

        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="time" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <Tooltip contentStyle={{
              backgroundColor: '#0f172a',
              border: '1px solid #334155',
              color: '#fff',
            }} />
            <Line
              type="monotone"
              dataKey="temperature"
              stroke="#fb923c"
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
        <h3 className="text-lg font-semibold mb-1">Vibration Trend</h3>
        <p className="text-sm text-slate-400 mb-5">
          Live synthetic vibration readings (mm/s)
        </p>

        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="time" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <Tooltip contentStyle={{
              backgroundColor: '#0f172a',
              border: '1px solid #334155',
              color: '#fff',
            }} />
            <Line
              type="monotone"
              dataKey="vibration"
              stroke="#22d3ee"
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default SensorCharts
