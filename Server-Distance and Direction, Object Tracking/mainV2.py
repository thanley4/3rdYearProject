import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Fixing random state for reproducibility
np.random.seed(19680801)

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(16, 9), dpi=120)
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0.0, 1920), ax.set_xticks([])
ax.set_ylim(1080, 0.0), ax.set_yticks([])

# Create rain data
num_objects_in_frame = 10

objects_in_frame = np.zeros(num_objects_in_frame, dtype=[('position', float, (2,)),
                                                        ('y', int),
                                                        ('size', int),
                                                        ('colour', int, (3,))])

# Initialize the raindrops in random positions and with
# random growth rates.
objects_in_frame['position'][:, 0] = np.random.uniform(0, 1920, num_objects_in_frame)
objects_in_frame['position'][:, 1] = np.random.uniform(0, 1080, num_objects_in_frame)
objects_in_frame['size'] = np.random.uniform(0, 25, num_objects_in_frame)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scatter_plot = ax.scatter(objects_in_frame['position'][:, 0], objects_in_frame['position'][:, 1],
                          objects_in_frame['size'])


def update(frame_number):
    objects_in_frame['position'][:, 0] = np.random.uniform(0, 1920, num_objects_in_frame)
    objects_in_frame['position'][:, 1] = np.random.uniform(0, 1080, num_objects_in_frame)
    objects_in_frame['size'] = np.random.uniform(0, 25, num_objects_in_frame)

    scatter_plot.set_offsets(objects_in_frame['position'])
    scatter_plot.set_sizes(objects_in_frame['size'])


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()