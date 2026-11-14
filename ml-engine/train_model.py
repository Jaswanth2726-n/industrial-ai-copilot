from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split


FEATURES = [
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "current_a",
]


def train_model():
    project_dir = Path(__file__).resolve().parent

    data_path = project_dir / "data" / "synthetic_motor_data.csv"
    model_path = project_dir / "models" / "isolation_forest.joblib"

    dataset = pd.read_csv(data_path)

    normal_data = dataset[dataset["is_fault"] == 0][FEATURES]
    fault_data = dataset[dataset["is_fault"] == 1]

    X_normal_train, X_normal_test = train_test_split(
        normal_data,
        test_size=0.2,
        random_state=42,
    )

    _, X_fault_test = train_test_split(
        fault_data[FEATURES],
        test_size=0.2,
        random_state=42,
    )

    X_train = X_normal_train

    X_test = pd.concat(
        [X_normal_test, X_fault_test],
        ignore_index=True,
    )

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
    )

    model.fit(X_train)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print("Isolation Forest training completed!")
    print(f"Normal training samples: {len(X_train)}")
    print(f"Normal test samples: {len(X_normal_test)}")
    print(f"Fault test samples: {len(X_fault_test)}")
    print(f"Total test samples: {len(X_test)}")
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    train_model()
