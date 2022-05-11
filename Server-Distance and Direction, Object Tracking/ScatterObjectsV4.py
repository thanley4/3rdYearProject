import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(16, 9), dpi=120)

ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0.0, 1920), ax.set_xticks([])
ax.set_ylim(1080, 0.0), ax.set_yticks([])

num_objects_in_frame = 50

objects_in_frame = np.zeros(num_objects_in_frame, dtype=[('position', float, (2,)),
                                                         ('size', float),
                                                         ('in_frame', bool),
                                                         ('color', float, (4,))])

objects_in_frame['position'][:, 0] = -1000
objects_in_frame['position'][:, 1] = -1000
objects_in_frame['size'] = 10
objects_in_frame['in_frame'] = False

scatter_plot = ax.scatter(objects_in_frame['position'][:, 0], objects_in_frame['position'][:, 1],
                          s=objects_in_frame['size'], lw=0.5, edgecolors='red',
                          facecolors='none')


def update(i, x, y, s):

    # X - Position
    # objects_in_frame['position'][:, 0] = np.random.uniform(0, 1920, max_objects_in_frame)
    objects_in_frame['position'][i, 0] = x

    # Y - Position
    # objects_in_frame['position'][:, 1] = np.random.uniform(0, 1080, max_objects_in_frame)
    objects_in_frame['position'][i, 1] = y

    # Size - Diameter * Unknown
    objects_in_frame['size'][i] = s

    # Update Scatter Plot Positions
    scatter_plot.set_offsets(objects_in_frame['position'])

    # Update Scatter Plot Sizes
    scatter_plot.set_sizes(objects_in_frame['size'])


animation = FuncAnimation(fig, update, interval=33)
plt.show()