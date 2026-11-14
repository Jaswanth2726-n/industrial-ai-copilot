
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from threading import Lock

import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.simulator.motor_simulator import MotorSimulator
from predict import predict_anomaly


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("industrial-ai-copilot")

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial-ai-copilot/demo-esp32-7f3a/motor/sensors"

simulator = MotorSimulator()

latest_esp32_reading = None
reading_lock = Lock()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logger.error("MQTT connection failed: %s", reason_code)
        return

    logger.info("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC, qos=1)
    logger.info("Subscribed to topic: %s", MQTT_TOPIC)


def on_message(client, userdata, message):
    global latest_esp32_reading

    try:
        payload = json.loads(message.payload.decode("utf-8"))

        reading = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": payload["mode"],
            "temperature_c": float(payload["temperature_c"]),
            "vibration_mm_s": float(payload["vibration_mm_s"]),
            "rpm": float(payload["rpm"]),
            "current_a": float(payload["current_a"]),
            "is_synthetic": True,
            "source": "wokwi_esp32",
        }

        if reading["mode"] not in {"normal", "fault"}:
            raise ValueError("Invalid motor mode")

        with reading_lock:
            latest_esp32_reading = reading

        logger.info("ESP32 sensor reading received: %s", reading)

    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as error:
        logger.warning("Invalid MQTT sensor message: %s", error)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="industrial-ai-copilot-backend",
    )

    client.on_connect = on_connect
    client.on_message = on_message

    app.state.mqtt_client = client

    try:
        client.connect_async(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        logger.info("MQTT subscriber started")
    except Exception:
        logger.exception("Could not start MQTT subscriber")

    yield

    client.loop_stop()
    client.disconnect()
    logger.info("MQTT subscriber stopped")


app = FastAPI(
    title="Industrial Predictive Maintenance API",
    description="Backend API for motor telemetry and ML anomaly detection.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModeRequest(BaseModel):
    mode: str


def get_latest_reading():
    with reading_lock:
        if latest_esp32_reading is not None:
            return dict(latest_esp32_reading)

    reading = simulator.generate_reading()
    reading["source"] = "python_simulator"
    return reading


@app.get("/")
def root():
    return {
        "message": "Industrial AI Copilot API is running",
        "synthetic_data": True,
        "ml_enabled": True,
        "mqtt_enabled": True,
    }


@app.get("/api/sensor/readings")
def get_sensor_reading():
    return get_latest_reading()


@app.post("/api/sensor/mode")
def set_simulation_mode(request: ModeRequest):
    try:
        simulator.set_mode(request.mode)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "message": f"Simulator mode changed to {request.mode}",
        "mode": simulator.mode,
    }


@app.get("/api/ml/prediction")
def get_ml_prediction():
    reading = get_latest_reading()

    try:
        prediction = predict_anomaly(
            temperature_c=reading["temperature_c"],
            vibration_mm_s=reading["vibration_mm_s"],
            rpm=reading["rpm"],
            current_a=reading["current_a"],
        )
    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {
        "timestamp": reading["timestamp"],
        "mode": reading["mode"],
        "is_synthetic": True,
        "source": reading["source"],
        "sensor_reading": reading,
        "ml_prediction": prediction,
    }
