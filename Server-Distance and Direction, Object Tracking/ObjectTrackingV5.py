import math
import time

import numpy as np

from multiprocessing import Pool

max_acceleration_or_decceleration = 7  # m / s^2
num_total_matches = 0
num_total_objects = 0

old_frame_global = np.ndarray
num_objects_old_global = 0
new_frame_global = np.ndarray
num_objects_new_global = 0
t_global = 0

match_error = []
match_old_index = []
match_new_index = []


def check_error(old, index):
    total_matches = 0
    matches = np.zeros(100, dtype=[('error', float,), ('old index', int), ('new index', int)])

    max_error = round(t_global * math.sqrt((old['velocity (t)'][0] ** 2) + (
                old['velocity (t)'][1] ** 2)) + 0.5 * max_acceleration_or_decceleration * (t_global ** 2), 3)

    for j in range(0, num_objects_new_global):
        error = round(
            math.sqrt((((old['position (t+1)'][0] - new_frame_global['position (t)'][0]) / 20) ** 2) +
                      (((old['position (t+1)'][1] - new_frame_global['position (t)'][1]) / 20) ** 2)), 3)

        if old['id'] == new_frame_global['id'][j] and error <= max_error:
            match_error.append(error)
            match_old_index.append(index)
            match_new_index.append(j)
            #
            # matches['error'][total_matches] = error
            # matches['old index'][total_matches] = index
            # matches['new index'][total_matches] = j
            # total_matches = total_matches + 1


def assign_objects(old_frame, num_objects_old, new_frame, num_objects_new, t):
    old_frame['match'] = False
    global num_total_matches
    global num_total_objects

    global old_frame_global
    global num_objects_old_global
    global new_frame_global
    global num_objects_new_global
    global t_global

    old_frame_global = old_frame
    num_objects_old_global = num_objects_old
    new_frame_global = new_frame
    num_objects_new_global = num_objects_new
    t_global = t

    matches = np.zeros(100, dtype=[('error', float,), ('old index', int), ('new index', int)])
    total_matches = 0

    num_total_objects = num_total_objects + num_objects_new

    if num_objects_new != 0:
        number_of_processes = num_objects_new
        array_of_indexes = range(num_objects_old_global)

        with Pool(number_of_processes) as pool:
            pool.starmap(check_error, zip(old_frame_global, array_of_indexes))
        print(match_error)
        print(match_old_index)
        print(match_new_index)

    return old_frame

        # for i in range(0, num_objects_old):
        #     # print("Old Frame Velocity:", old_frame['velocity (t)'][i, 0], "i,", old_frame['velocity (t)'][i, 1], "j")
        #     max_error = round(t * math.sqrt((old_frame['velocity (t)'][i, 0] ** 2) + (old_frame['velocity (t)'][i, 1] ** 2)) + 0.5 * max_acceleration_or_decceleration * (t ** 2), 3) + (1.1111 * int(old_frame['velocity (t)'][i, 0] == 0 and old_frame['velocity (t)'][i, 1] == 0))
        #     for j in range(0, num_objects_new):
        #         error = round(
        #             math.sqrt((((old_frame['position (t+1)'][i, 0] - new_frame['position (t)'][j, 0]) / 20) ** 2) +
        #                       (((old_frame['position (t+1)'][i, 1] - new_frame['position (t)'][j, 1]) / 20) ** 2)), 3)
        #
        #         if old_frame['id'][i] == new_frame['id'][j] and error <= max_error:
        #             matches['error'][total_matches] = error
        #             matches['old index'][total_matches] = i
        #             matches['new index'][total_matches] = j
        #             total_matches = total_matches + 1

        # matches.sort(order='error')

    #     old_frame['velocity (t-2)'] = old_frame['velocity (t-1)']
    #     old_frame['velocity (t-1)'] = old_frame['velocity (t)']
    #
    #     old_frame['position (t-1)'] = old_frame['position (t)']
    #     old_frame['position (t-2)'] = old_frame['position (t-1)']
    #     old_frame['position (t-3)'] = old_frame['position (t-2)']
    #     old_frame['position (t-4)'] = old_frame['position (t-3)']
    #     old_frame['position (t-5)'] = old_frame['position (t-4)']
    #     old_frame['position (t-6)'] = old_frame['position (t-5)']
    #
    #     num_total_matches = num_total_matches + total_matches
    #
    #     # Sorted puts max error at bottom of 100 long vector
    #     #
    #
    #     for i in range(99, 99 - total_matches, -1):
    #         old_frame['position (t)'][matches['old index'][i]] = new_frame['position (t)'][matches['new index'][i]]
    #         old_frame['size'][matches['old index'][i]] = new_frame['size'][matches['new index'][i]]
    #         old_frame['color'][matches['old index'][i]] = [0, 1, 0]
    #         old_frame['match'][matches['old index'][i]] = True
    #         new_frame['match'][matches['new index'][i]] = True
    #
    #         print("Old Index:", matches['old index'][i], ", New Index: ", matches['new index'][i],
    #               "\nOld Position:", old_frame['position (t)'][matches['old index'][i]],
    #               ", New Position: ", new_frame['position (t)'][matches['new index'][i]],
    #               "Expected Position:", old_frame['position (t+1)'][matches['old index'][i]])
    #
    #     old_frame['velocity (t)'][:, 0] = (old_frame['position (t)'][:, 0] - old_frame['position (t-1)'][:, 0]) * 1.5
    #     old_frame['velocity (t)'][:, 1] = (old_frame['position (t)'][:, 1] - old_frame['position (t-1)'][:, 1]) * 1.5
    #
    #     j = 0
    #     for i in range(0, num_objects_old):
    #         # If there isn't already a match in this position
    #         if not old_frame['match'][i]:
    #             # If there are still objects in the frame to be added
    #             if i < num_objects_new and j < num_objects_new:
    #                 # As long as the current frame is
    #                 while new_frame['match'][j] and j < num_objects_new - 1:
    #                     j = j + 1
    #                 old_frame['position (t)'][i] = new_frame['position (t)'][j]
    #                 old_frame['size'][i] = new_frame['size'][j]
    #                 old_frame['id'][i] = new_frame['id'][j]
    #                 # print("Old: ", old_frame['id'], " New: ", new_frame['id'])
    #                 j = j + 1
    #             else:
    #                 old_frame['position (t)'][i, 0] = -1000
    #                 old_frame['position (t)'][i, 1] = -1000
    #                 old_frame['id'][i] = 999
    #                 old_frame['size'][i] = 10
    #             old_frame['position (t-1)'][i, 0] = -1000
    #             old_frame['position (t-1)'][i, 1] = -1000
    #             old_frame['position (t-2)'][i, 0] = -1000
    #             old_frame['position (t-2)'][i, 1] = -1000
    #             old_frame['position (t-3)'][i, 0] = -1000
    #             old_frame['position (t-3)'][i, 1] = -1000
    #             old_frame['position (t-4)'][i, 0] = -1000
    #             old_frame['position (t-4)'][i, 1] = -1000
    #             old_frame['position (t-5)'][i, 0] = -1000
    #             old_frame['position (t-5)'][i, 1] = -1000
    #             old_frame['position (t-6)'][i, 0] = -1000
    #             old_frame['position (t-6)'][i, 1] = -1000
    #             old_frame['velocity (t)'][i, 0] = 0
    #             old_frame['velocity (t)'][i, 1] = 0
    #             old_frame['velocity (t-1)'][i, 0] = 0
    #             old_frame['velocity (t-1)'][i, 1] = 0
    #             old_frame['velocity (t-2)'][i, 0] = 0
    #             old_frame['velocity (t-2)'][i, 1] = 0
    #
    #     old_frame['position (t+1)'][:, 0] = old_frame['position (t)'][:, 0] + old_frame['velocity (t)'][:, 0] / 1.5
    #     old_frame['position (t+1)'][:, 1] = old_frame['position (t)'][:, 1] + old_frame['velocity (t)'][:, 1] / 1.5
    #
    #     print(total_matches, "Matches from", num_objects_new, "Objects")
    #     print("Total Match %:", num_total_matches / num_total_objects * 100)
    #
    # else:
    #     old_frame['position (t+1)'][:, 0] = -1000
    #     old_frame['position (t+1)'][:, 1] = -1000
    #     old_frame['position (t)'][:, 0] = -1000
    #     old_frame['position (t)'][:, 1] = -1000
    #     old_frame['position (t-1)'][:, 0] = -1000
    #     old_frame['position (t-1)'][:, 1] = -1000
    #     old_frame['position (t-2)'][:, 0] = -1000
    #     old_frame['position (t-2)'][:, 1] = -1000
    #     old_frame['position (t-3)'][:, 0] = -1000
    #     old_frame['position (t-3)'][:, 1] = -1000
    #     old_frame['position (t-4)'][:, 0] = -1000
    #     old_frame['position (t-4)'][:, 1] = -1000
    #     old_frame['position (t-5)'][:, 0] = -1000
    #     old_frame['position (t-5)'][:, 1] = -1000
    #     old_frame['position (t-6)'][:, 0] = -1000
    #     old_frame['position (t-6)'][:, 1] = -1000
    #     old_frame['velocity (t)'][:, 0] = 10
    #     old_frame['velocity (t)'][:, 1] = 10
    #     old_frame['velocity (t-1)'][:, 0] = 0
    #     old_frame['velocity (t-1)'][:, 1] = 0
    #     old_frame['velocity (t-2)'][:, 0] = 0
    #     old_frame['velocity (t-2)'][:, 1] = 0
    #     old_frame['id'] = 999
    #     old_frame['size'] = 10
    #     old_frame['color'] = [1, 0, 0]
    #     old_frame['match'] = False
    #
    # return old_frame, num_objects_new
