from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split


FEATURES = [
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "current_a",
]


def evaluate_model():
    project_dir = Path(__file__).resolve().parent

    data_path = project_dir / "data" / "synthetic_motor_data.csv"
    model_path = project_dir / "models" / "isolation_forest.joblib"

    dataset = pd.read_csv(data_path)

    normal_data = dataset[dataset["is_fault"] == 0][FEATURES]
    fault_data = dataset[dataset["is_fault"] == 1]

    _, X_normal_test = train_test_split(
        normal_data,
        test_size=0.2,
        random_state=42,
    )

    fault_indices = fault_data.index

    _, fault_test_indices = train_test_split(
        fault_indices,
        test_size=0.2,
        random_state=42,
    )

    fault_test = dataset.loc[fault_test_indices]

    X_test = pd.concat(
        [X_normal_test, fault_test[FEATURES]],
        ignore_index=True,
    )

    y_true = pd.Series(
        [0] * len(X_normal_test) + [1] * len(fault_test)
    )

    model = joblib.load(model_path)

    # Isolation Forest returns 1 for normal and -1 for anomalies.
    raw_predictions = model.predict(X_test)

    y_pred = (raw_predictions == -1).astype(int)

    print("=" * 55)
    print("ISOLATION FOREST - MODEL EVALUATION")
    print("=" * 55)

    print(f"\nTest samples: {len(X_test)}")
    print(f"Actual normal samples: {(y_true == 0).sum()}")
    print(f"Actual fault samples: {(y_true == 1).sum()}")

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=["Normal", "Anomaly"],
            zero_division=0,
        )
    )

    print("Summary Metrics:")
    print(f"Precision: {precision_score(y_true, y_pred):.3f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.3f}")
    print(f"F1-score:  {f1_score(y_true, y_pred):.3f}")

    print("\nFault Category Detection:")
    for fault_type in sorted(fault_test["fault_type"].unique()):
        category_data = fault_test[
            fault_test["fault_type"] == fault_type
        ]

        category_predictions = model.predict(category_data[FEATURES])
        detected = (category_predictions == -1).sum()

        print(
            f"{fault_type}: {detected}/{len(category_data)} "
            f"detected as anomalies"
        )

    print("\nNote: These metrics measure performance on synthetic scenarios.")
    print("They do not establish real-world industrial performance.")


if __name__ == "__main__":
    evaluate_model()
