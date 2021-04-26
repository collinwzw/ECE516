import math

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from matplotlib import animation

# constants
# Make sure CHUNK is divisible by wraps
CHUNK = 2400
WRAPS = 1
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second
COLS = 1
ROWS = 1
SATURATION_LVL = 32767  # Int16 max.
HALF_SATURATION = SATURATION_LVL // 2

TITLE = " "

# Create matplotlib figure and axes.
plt.style.use('dark_background')
fig, axes = plt.subplots(ROWS, COLS, figsize=(15, 7), subplot_kw=dict(polar=True))

# Init PyAudio Class.
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.linspace(0, 2 * math.pi, CHUNK // WRAPS, dtype=float)
x_wrapper = np.linspace(0, 2 * math.pi, CHUNK // WRAPS, dtype=float)
for index in range(WRAPS - 1):
    x = np.append(x, x_wrapper)

lines = []
axes.set_xticks([])
axes.set_yticks([])
axes.set_facecolor('k')
axes.set_title(TITLE, color='white')
axes.set_ylim(-1, SATURATION_LVL)
temp = axes.plot(x, np.random.rand(CHUNK), '-', color='white', linewidth=0.5)[0]
lines.append(temp)


def init():
    """
    Base frame for animation.FuncAnimation.

    Returns:
        list(np.array): Data to animate.
    """
    for line in lines:
        line.set_ydata([])
    return lines


def animate(frame_num):
    """
    Main animation method for animation.FuncAnimation.

    Args:
        frame_num (int): Frame number as it is called in animation.FuncAnimation.

    Returns:
        list(np.array): Data to animate.
    """
    # binary data
    data_raw = stream.read(CHUNK, exception_on_overflow=False)
    # create np array and offset by 128
    data = np.frombuffer(data_raw, dtype=np.int16).astype(np.int16)
    data_processed = np.add(data, HALF_SATURATION)

    lines[0].set_ydata(data_processed)
    return lines


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=1000, interval=10, blit=True)
plt.show()