import matplotlib.pyplot as plt
import numpy as np

# aircraft characateristics
groundspeed = 20  # m/s
pressure = 101300.0  # pascals
tempK = 15 + 273.15  # Kelvin

# ArduPilot parameters
L1_damp = 0.75
L1_period = 17
WP_radius = 140  # meters

# other values that don't change in L1
dist_min = 0
# equivalent airspeed to true airspeed ratio
eas2tas = (1.225 / (pressure / (287.26 * tempK))) ** 0.5
L1_dist = max(0.3183099 * L1_damp * L1_period * groundspeed, dist_min)


def turn_distance(wp_radius, turn_angle):
    distance_90 = min(wp_radius * eas2tas ** 2, L1_dist)
    if turn_angle >= 90:
        return distance_90
    return distance_90 * turn_angle / 90.0


turn_angle_plot = np.linspace(0, 100, 300)
distance_result = np.zeros_like(turn_angle_plot)
L1_dist_plot = np.ones_like(turn_angle_plot) * L1_dist
wp_radius_plot = np.ones_like(turn_angle_plot) * WP_radius
for i in range(len(turn_angle_plot)):
    distance_result[i] = turn_distance(WP_radius, turn_angle_plot[i])
plt.plot(turn_angle_plot, distance_result, label="Actual distance")
plt.plot(turn_angle_plot, L1_dist_plot, label="L1 distance")
plt.plot(turn_angle_plot, wp_radius_plot, label="WP_RADIUS")
plt.legend()
plt.xlabel("Waypoint angle [deg]")
plt.ylabel("Disantance from current waypoint where the turn will start [m]")
plt.title("NAVL1_DAMPING = {}, NAVL1_PERIOD = {}, WP_RADIUS = {}".format(L1_damp, L1_period, WP_radius))
plt.show()
