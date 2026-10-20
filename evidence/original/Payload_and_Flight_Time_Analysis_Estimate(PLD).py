import matplotlib.pyplot as plt
import numpy as np

# Constants
max_thrust_total = 3400  # grams
drone_weight_base = 1100  # base drone weight without extra payload
base_flight_time = 7  # minutes (real-world flight time estimate with 1100g)

# Payloads from 0 to 1000g
payload_weights = np.arange(0, 1001, 100)
total_weights = drone_weight_base + payload_weights

# Throttle needed to lift off (as % of total available thrust)
throttle_percent = (total_weights / max_thrust_total) * 100

# Realistic flight time estimation using exponential decay model
def estimate_flight_time(base_weight, payload, base_time):
    total_weight = base_weight + payload
    factor = (base_weight / total_weight) ** 1.3
    return base_time * factor

realistic_flight_times = [estimate_flight_time(drone_weight_base, pw, base_flight_time) for pw in payload_weights]

# Plotting
plt.figure(figsize=(10, 6))

# Throttle vs Payload
plt.subplot(2, 1, 1)
plt.plot(payload_weights, throttle_percent, marker='o', color='teal')
plt.title("Throttle % and Flight Time vs Payload")
plt.ylabel("Throttle % for Liftoff")
plt.grid(True)
plt.axhline(100, color='red', linestyle='--', label="Max Thrust Limit")
plt.legend()

# Flight Time vs Payload
plt.subplot(2, 1, 2)
plt.plot(payload_weights, realistic_flight_times, marker='o', color='orange')
plt.xlabel("Payload (grams)")
plt.ylabel("Estimated Flight Time (min)")
plt.grid(True)

plt.tight_layout()
plt.show()
#AUTHOR:- ABHINAV PATRO