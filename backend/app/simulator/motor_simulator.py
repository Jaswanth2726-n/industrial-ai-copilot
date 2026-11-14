import random
from datetime import datetime, timezone


class MotorSimulator:
    """Generate synthetic motor telemetry for development and testing."""

    def __init__(self):
        self.mode = "normal"
        self.temperature = 65.0
        self.vibration = 2.0
        self.rpm = 1500.0
        self.current = 4.5

    def set_mode(self, mode: str) -> None:
        if mode not in {"normal", "fault"}:
            raise ValueError("Mode must be 'normal' or 'fault'")
        self.mode = mode

    def generate_reading(self) -> dict:
        if self.mode == "normal":
            self.temperature = random.uniform(63.0, 68.0)
            self.vibration = random.uniform(1.5, 2.5)
            self.rpm = random.uniform(1470.0, 1530.0)
            self.current = random.uniform(4.0, 5.0)
        else:
            self.temperature = random.uniform(82.0, 95.0)
            self.vibration = random.uniform(5.0, 8.0)
            self.rpm = random.uniform(1250.0, 1400.0)
            self.current = random.uniform(5.5, 7.0)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": self.mode,
            "temperature_c": round(self.temperature, 2),
            "vibration_mm_s": round(self.vibration, 2),
            "rpm": round(self.rpm, 2),
            "current_a": round(self.current, 2),
            "is_synthetic": True,
        }


if __name__ == "__main__":
    simulator = MotorSimulator()

    print("NORMAL MODE")
    print(simulator.generate_reading())

    print("\nFAULT MODE")
    simulator.set_mode("fault")
    print(simulator.generate_reading())
