from pathlib import Path

import numpy as np
import pandas as pd


def generate_dataset():
    rng = np.random.default_rng(42)

    normal_count = 2000
    fault_count = 600

    # Normal operating conditions
    normal = pd.DataFrame({
        "temperature_c": rng.normal(65, 2, normal_count),
        "vibration_mm_s": rng.normal(2.0, 0.25, normal_count),
        "rpm": rng.normal(1500, 20, normal_count),
        "current_a": rng.normal(4.5, 0.25, normal_count),
        "is_fault": 0,
        "fault_type": "normal",
    })

    # Simulated overheating faults
    overheating = pd.DataFrame({
        "temperature_c": rng.normal(88, 4, 150),
        "vibration_mm_s": rng.normal(2.2, 0.3, 150),
        "rpm": rng.normal(1480, 25, 150),
        "current_a": rng.normal(4.8, 0.3, 150),
        "is_fault": 1,
        "fault_type": "overheating",
    })

    # Simulated excessive vibration faults
    imbalance = pd.DataFrame({
        "temperature_c": rng.normal(68, 3, 150),
        "vibration_mm_s": rng.normal(6.5, 0.8, 150),
        "rpm": rng.normal(1480, 30, 150),
        "current_a": rng.normal(4.8, 0.4, 150),
        "is_fault": 1,
        "fault_type": "excessive_vibration",
    })

    # Simulated motor overload faults
    overload = pd.DataFrame({
        "temperature_c": rng.normal(82, 4, 150),
        "vibration_mm_s": rng.normal(3.5, 0.5, 150),
        "rpm": rng.normal(1400, 35, 150),
        "current_a": rng.normal(6.5, 0.5, 150),
        "is_fault": 1,
        "fault_type": "overload",
    })

    # Simulated speed-drop faults
    speed_drop = pd.DataFrame({
        "temperature_c": rng.normal(72, 3, 150),
        "vibration_mm_s": rng.normal(3.0, 0.5, 150),
        "rpm": rng.normal(1280, 35, 150),
        "current_a": rng.normal(5.2, 0.4, 150),
        "is_fault": 1,
        "fault_type": "speed_drop",
    })

    dataset = pd.concat(
        [normal, overheating, imbalance, overload, speed_drop],
        ignore_index=True,
    )

    dataset = dataset.sample(
        frac=1,
        random_state=42,
    ).reset_index(drop=True)

    output_path = (
        Path(__file__).resolve().parent
        / "data"
        / "synthetic_motor_data.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(output_path, index=False)

    print("Synthetic motor dataset generated successfully!")
    print(f"Total readings: {len(dataset)}")
    print(f"Normal readings: {(dataset['is_fault'] == 0).sum()}")
    print(f"Fault readings: {(dataset['is_fault'] == 1).sum()}")
    print("\nFault distribution:")
    print(dataset["fault_type"].value_counts())
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    generate_dataset()
