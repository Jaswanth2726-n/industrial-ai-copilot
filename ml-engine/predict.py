from pathlib import Path

import joblib
import pandas as pd


FEATURES = [
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "current_a",
]

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "isolation_forest.joblib"
)


def predict_anomaly(
    temperature_c: float,
    vibration_mm_s: float,
    rpm: float,
    current_a: float,
) -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    sensor_data = pd.DataFrame(
        [[temperature_c, vibration_mm_s, rpm, current_a]],
        columns=FEATURES,
    )

    prediction = model.predict(sensor_data)[0]
    score = model.decision_function(sensor_data)[0]

    is_anomaly = prediction == -1

    return {
        "prediction": "anomaly" if is_anomaly else "normal",
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": round(float(score), 5),
        "sensor_values": {
            "temperature_c": temperature_c,
            "vibration_mm_s": vibration_mm_s,
            "rpm": rpm,
            "current_a": current_a,
        },
    }


if __name__ == "__main__":
    print("Normal operating example:")
    print(predict_anomaly(65.0, 2.0, 1500.0, 4.5))

    print("\nSimulated fault example:")
    print(predict_anomaly(90.0, 7.0, 1300.0, 6.5))
