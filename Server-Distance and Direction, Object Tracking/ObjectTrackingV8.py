import math
import time
from multiprocessing import Pool
import multiprocessing
from multiprocessing import Process


import numpy as np

max_acceleration_or_decceleration = 7  # m / s^2
num_total_matches = 0
num_total_objects = 0


def assign_objects(old_frame, num_objects_old, new_frame, num_objects_new, t, v):
    old_frame['match'] = False
    global num_total_matches
    global num_total_objects

    def find_match(portion, index):

        match = np.zeros(1, dtype=[('error', float,), ('old index', int), ('new index', int)])
        max_error = round(t * math.sqrt((portion['velocity (t)'][0] ** 2) + (
                portion['velocity (t)'][1] ** 2)) + 0.5 * max_acceleration_or_decceleration * (t ** 2), 3) + \
                    (2.2222 * int(portion['velocity (t)'][0] == 0 and portion['velocity (t)'][1] == 0))
        for j in range(0, num_objects_new):
            match['error'] = max_error + 1
            error = round(
                math.sqrt((((portion['position (t+1)'][0] - new_frame['position (t)'][j, 0]) / 20) ** 2) +
                          (((portion['position (t+1)'][1] - new_frame['position (t)'][j, 1]) / 20) ** 2)), 3)

            if portion['id'] == new_frame['id'][j] and error <= max_error:
                if error < match['error']:
                    match['error'] = error
                    match['old index'] = index
                    match['new index'] = j
        return match

    matches = np.zeros(100, dtype=[('error', float,), ('old index', int), ('new index', int)])
    total_matches = 0

    num_total_objects = num_total_objects + num_objects_new

    if num_objects_new != 0:
        for i in range(0, num_objects_old):
            matches[i] = find_match(old_frame[i], i)

        old_frame['velocity (t-2)'] = old_frame['velocity (t-1)']
        old_frame['velocity (t-1)'] = old_frame['velocity (t)']

        old_frame['position (t-6)'] = old_frame['position (t-5)']
        old_frame['position (t-5)'] = old_frame['position (t-4)']
        old_frame['position (t-4)'] = old_frame['position (t-3)']
        old_frame['position (t-3)'] = old_frame['position (t-2)']
        old_frame['position (t-2)'] = old_frame['position (t-1)']
        old_frame['position (t-1)'] = old_frame['position (t)']

        for i in range(0, num_objects_new):
            old_frame['position (t)'][matches['old index'][i]] = new_frame['position (t)'][matches['new index'][i]]
            old_frame['size'][matches['old index'][i]] = new_frame['size'][matches['new index'][i]]
            old_frame['color'][matches['old index'][i]] = [0, 1, 0]
            old_frame['match'][matches['old index'][i]] = True
            new_frame['match'][matches['new index'][i]] = True

        old_frame['velocity (t)'][:, 0] = (old_frame['position (t)'][:, 0] - old_frame['position (t-1)'][:, 0]) * 1.5
        old_frame['velocity (t)'][:, 1] = ((old_frame['position (t)'][:, 1] - old_frame['position (t-1)'][:, 1]) * 1.5) - v

        j = 0
        for i in range(0, num_objects_old):
            # If there isn't already a match in this position
            if not old_frame['match'][i]:
                # If there are still objects in the frame to be added
                if i < num_objects_new and j < num_objects_new:
                    # As long as the current frame is
                    while new_frame['match'][j] and j < num_objects_new - 1:
                        j = j + 1
                    old_frame['position (t)'][i] = new_frame['position (t)'][j]
                    old_frame['size'][i] = new_frame['size'][j]
                    old_frame['id'][i] = new_frame['id'][j]
                    # print("Old: ", old_frame['id'], " New: ", new_frame['id'])
                    j = j + 1
                else:
                    old_frame['position (t)'][i, 0] = -1000
                    old_frame['position (t)'][i, 1] = -1000
                    old_frame['id'][i] = 999
                    old_frame['size'][i] = 10
                old_frame['position (t-1)'][i, 0] = -1000
                old_frame['position (t-1)'][i, 1] = -1000
                old_frame['position (t-2)'][i, 0] = -1000
                old_frame['position (t-2)'][i, 1] = -1000
                old_frame['position (t-3)'][i, 0] = -1000
                old_frame['position (t-3)'][i, 1] = -1000
                old_frame['position (t-4)'][i, 0] = -1000
                old_frame['position (t-4)'][i, 1] = -1000
                old_frame['position (t-5)'][i, 0] = -1000
                old_frame['position (t-5)'][i, 1] = -1000
                old_frame['position (t-6)'][i, 0] = -1000
                old_frame['position (t-6)'][i, 1] = -1000
                old_frame['velocity (t)'][i, 0] = 0
                old_frame['velocity (t)'][i, 1] = 0
                old_frame['velocity (t-1)'][i, 0] = 0
                old_frame['velocity (t-1)'][i, 1] = 0
                old_frame['velocity (t-2)'][i, 0] = 0
                old_frame['velocity (t-2)'][i, 1] = 0

        old_frame['position (t+1)'][:, 0] = old_frame['position (t)'][:, 0] + old_frame['velocity (t)'][:, 0] / 1.5
        old_frame['position (t+1)'][:, 1] = old_frame['position (t)'][:, 1] + old_frame['velocity (t)'][:, 1] / 1.5

        # Check this is working
        for i in range(num_objects_new, num_objects_old):
            # print("Resetting Old Frame Object", i)
            old_frame['position (t+1)'][i, 0] = -1000
            old_frame['position (t+1)'][i, 1] = -1000
            old_frame['position (t)'][i, 0] = -1000
            old_frame['position (t)'][i, 1] = -1000
            old_frame['position (t-1)'][i, 0] = -1000
            old_frame['position (t-1)'][i, 1] = -1000
            old_frame['position (t-2)'][i, 0] = -1000
            old_frame['position (t-2)'][i, 1] = -1000
            old_frame['position (t-3)'][i, 0] = -1000
            old_frame['position (t-3)'][i, 1] = -1000
            old_frame['position (t-4)'][i, 0] = -1000
            old_frame['position (t-4)'][i, 1] = -1000
            old_frame['position (t-5)'][i, 0] = -1000
            old_frame['position (t-5)'][i, 1] = -1000
            old_frame['position (t-6)'][i, 0] = -1000
            old_frame['position (t-6)'][i, 1] = -1000
            old_frame['velocity (t)'][i, 0] = 0
            old_frame['velocity (t)'][i, 1] = 0
            old_frame['velocity (t-1)'][i, 0] = 0
            old_frame['velocity (t-1)'][i, 1] = 0
            old_frame['velocity (t-2)'][i, 0] = 0
            old_frame['velocity (t-2)'][i, 1] = 0
            old_frame['id'][i] = 999
            old_frame['size'][i] = 10
            old_frame['color'][i] = [1, 0, 0]
            old_frame['match'][i] = False

        # print(total_matches, "Matches from", num_objects_new, "Objects")
        # print("Total Match %:", num_total_matches / num_total_objects * 100)

    else:
        old_frame['position (t+1)'][:, 0] = -1000
        old_frame['position (t+1)'][:, 1] = -1000
        old_frame['position (t)'][:, 0] = -1000
        old_frame['position (t)'][:, 1] = -1000
        old_frame['position (t-1)'][:, 0] = -1000
        old_frame['position (t-1)'][:, 1] = -1000
        old_frame['position (t-2)'][:, 0] = -1000
        old_frame['position (t-2)'][:, 1] = -1000
        old_frame['position (t-3)'][:, 0] = -1000
        old_frame['position (t-3)'][:, 1] = -1000
        old_frame['position (t-4)'][:, 0] = -1000
        old_frame['position (t-4)'][:, 1] = -1000
        old_frame['position (t-5)'][:, 0] = -1000
        old_frame['position (t-5)'][:, 1] = -1000
        old_frame['position (t-6)'][:, 0] = -1000
        old_frame['position (t-6)'][:, 1] = -1000
        old_frame['velocity (t)'][:, 0] = 10
        old_frame['velocity (t)'][:, 1] = 10
        old_frame['velocity (t-1)'][:, 0] = 0
        old_frame['velocity (t-1)'][:, 1] = 0
        old_frame['velocity (t-2)'][:, 0] = 0
        old_frame['velocity (t-2)'][:, 1] = 0
        old_frame['id'] = 999
        old_frame['size'] = 10
        old_frame['color'] = [1, 0, 0]
        old_frame['match'] = False

    return old_frame, num_objects_new
