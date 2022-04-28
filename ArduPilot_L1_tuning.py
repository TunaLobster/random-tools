import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

# aircraft characateristics
groundspeed = 28  # m/s
pressure = 101300.0  # pascals
tempK = 15 + 273.15  # Kelvin

# ArduPilot parameters
L1_damp = 0.85
L1_period = 25
WP_radius = 200  # meters

dist_min = 0
L1_dist = max(0.3183099 * L1_damp * L1_period * groundspeed, dist_min)


def f(turn_angle, groundspeed, pressure, tempK, L1_damp, L1_period, wp_radius):
    # equivalent airspeed to true airspeed ratio
    eas2tas = (1.225 / (pressure / (287.26 * tempK))) ** 0.5
    L1_dist = get_L1_dist(groundspeed, L1_damp, L1_period,)
    return np.array([turn_distance(i, wp_radius, eas2tas, L1_dist) for i in turn_angle])


def get_L1_dist(groundspeed, L1_damp, L1_period):
    return max(0.3183099 * L1_damp * L1_period * groundspeed, dist_min)


def f_L1_dist(x, groundspeed, L1_damp, L1_period):
    return np.ones_like(x) * get_L1_dist(groundspeed, L1_damp, L1_period)


def f_wp_radius(x):
    return np.ones_like(x) * WP_radius


def turn_distance(turn_angle, wp_radius, eas2tas, L1_dist):
    distance_90 = min(wp_radius * eas2tas ** 2, L1_dist)
    if turn_angle >= 90:
        return distance_90
    return distance_90 * turn_angle / 90.0


turn_angle_plot = np.linspace(0, 100, 300)

fig, ax = plt.subplots()
line, = plt.plot(turn_angle_plot, f(turn_angle_plot, groundspeed, pressure, tempK, L1_damp, L1_period, WP_radius), label="Start turn distance")
l1_dist_line, = plt.plot(turn_angle_plot, f_L1_dist(turn_angle_plot, groundspeed, L1_damp, L1_period), label="L1_dist {:.2f} m".format(L1_dist))
wp_radius_line, = plt.plot(turn_angle_plot, f_wp_radius(turn_angle_plot), label="WP_RADIUS {:.2f} m".format(WP_radius))
# ax.hlines(WP_radius, min(turn_angle_plot), max(turn_angle_plot), label="WP_RADIUS")

# make room for slider
plt.subplots_adjust(bottom=0.25)

# Make a horizontal slider to control the groundspeed.
axgroundspeed = plt.axes([0.25, 0.1, 0.65, 0.03])
groundspeed_slider = Slider(
    ax=axgroundspeed,
    label="Groundspeed [m/s]",
    valmin=20,
    valmax=100,
    valinit=groundspeed,
)

# The function to be called anytime a slider's value changes


def update(val):
    line.set_ydata(f(turn_angle_plot, groundspeed_slider.val, pressure, tempK, L1_damp, L1_period, WP_radius))
    ax.set_title("Groundspeed = {:.2f} m/s,\nNAVL1_DAMPING = {}, NAVL1_PERIOD = {}".format(groundspeed_slider.val, L1_damp, L1_period, WP_radius))
    l1_dist_line.set_ydata(f_L1_dist(turn_angle_plot, groundspeed_slider.val, L1_damp, L1_period,))
    l1_dist_line.set(label = "L1_dist {:.2f} m".format(get_L1_dist(groundspeed_slider.val, L1_damp, L1_period)))
    wp_radius_line.set_ydata(f_wp_radius(turn_angle_plot))
    ax.set_ylim(auto=True)
    ax.set_autoscale_on(True)
    ax.autoscale_view()
    ax.legend(loc="lower right")
    fig.canvas.draw_idle()


# register the update function with each slider
groundspeed_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    groundspeed_slider.reset()


button.on_clicked(reset)

ax.set_title("Groundspeed = {:.2f} m/s,\nNAVL1_DAMPING = {}, NAVL1_PERIOD = {}".format(groundspeed, L1_damp, L1_period, WP_radius))
ax.legend(loc="lower right")
ax.set_xlabel("Bearing change after completeing next waypoint [deg]")
ax.set_ylabel("Disantance from current waypoint\nwhere the turn will start [m]")
plt.show()
