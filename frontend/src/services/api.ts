import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000,
})

export interface SensorReading {
  timestamp: string
  mode: 'normal' | 'fault'
  temperature_c: number
  vibration_mm_s: number
  rpm: number
  current_a: number
  is_synthetic: boolean
}

export interface ModeResponse {
  message: string
  mode: 'normal' | 'fault'
}
export interface MlPredictionResponse {
  timestamp: string
  mode: 'normal' | 'fault'
  is_synthetic: boolean
  sensor_reading: SensorReading
  ml_prediction: {
    prediction: 'normal' | 'anomaly'
    is_anomaly: boolean
    anomaly_score: number
    sensor_values: {
      temperature_c: number
      vibration_mm_s: number
      rpm: number
      current_a: number
    }
  }
}

export const getMlPrediction = async (): Promise<MlPredictionResponse> => {
  const response = await api.get<MlPredictionResponse>('/api/ml/prediction')
  return response.data
}

export const getSensorReading = async (): Promise<SensorReading> => {
  const response = await api.get<SensorReading>('/api/sensor/readings')
  return response.data
}

export const setSimulationMode = async (
  mode: 'normal' | 'fault',
): Promise<ModeResponse> => {
  const response = await api.post<ModeResponse>('/api/sensor/mode', { mode })
  return response.data
}

export default api
