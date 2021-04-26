import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_facecolor("black")
xdata, ydata = [], []
ln, = plt.plot([], [], 'go')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-5, 20)
    return ln,

def update(data):
    ln.set_data(2, data)
    return ln,

for i in range(0,20):

    ani = FuncAnimation(fig, update, frames=i,
                    init_func=init, blit=True)
plt.show()