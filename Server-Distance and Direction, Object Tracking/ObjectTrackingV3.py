import math
import time

import numpy as np

max_acceleration_or_decceleration = 7  # m / s^2
num_total_matches = 0
num_total_objects = 0


def assign_objects(old_frame, num_objects_old, new_frame, num_objects_new, t):
    old_frame['match'] = False
    global num_total_matches
    global num_total_objects

    matches = np.zeros(num_objects_new * 1000, dtype=[('error', float,), ('old index', int), ('new index', int)])
    total_matches = 0

    num_total_objects = num_total_objects + num_objects_new

    for i in range(0, num_objects_old - 1):
        # print("Old Frame Velocity:", old_frame['velocity (t)'][i, 0], "i,", old_frame['velocity (t)'][i, 1], "j")
        max_error = round(t * math.sqrt((old_frame['velocity (t)'][i, 0] ** 2) + (
                old_frame['velocity (t)'][i, 1] ** 2)) + 0.5 * max_acceleration_or_decceleration * (
                                  t ** 2), 3) + (1.1111 * int(
            old_frame['velocity (t)'][i, 0] == 0 and old_frame['velocity (t)'][i, 1] == 0))
        print("Max Error: ", max_error)
        for j in range(0, num_objects_new - 1):
            error = round(
                math.sqrt((((old_frame['position (t+1)'][i, 0] - new_frame['position (t)'][j, 0]) / 20) ** 2) +
                          (((old_frame['position (t+1)'][i, 1] - new_frame['position (t)'][j, 1]) / 20) ** 2)), 3)
            # print("Error: ", error)
            # print(error <= max_error)
            # print(old_frame['id'][i])
            # print(new_frame['id'][j])

            if old_frame['id'][i] == new_frame['id'][j] and error <= max_error:
                print(
                    "Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! Match! ")
                print("Old Index:", i, ", New Index: ", j, "Old Position:", old_frame['position (t)'][i], ", New Position: ", new_frame['position (t)'][j],
                      "Expected Position:", old_frame['position (t+1)'][i])
                matches['error'][total_matches] = error
                print()
                matches['old index'][total_matches] = i
                matches['new index'][total_matches] = j
                print("Old Index:", matches['old index'][total_matches], ", New Index:", matches['new index'][total_matches])
                total_matches = total_matches + 1

    matches.sort(order='error')

    old_frame['velocity (t-2)'] = old_frame['velocity (t-1)']
    old_frame['position (t-1)'] = old_frame['position (t)']

    num_total_matches = num_total_matches + total_matches

    print("\n\nMatches ------------------\n")

    for i in range(0, total_matches):
        old_frame['position (t)'][matches['old index'][num_objects_new - 1 - i], 0] = new_frame['position (t)'][
            matches['new index'][num_objects_new - 1 - i], 0]
        old_frame['position (t)'][matches['old index'][num_objects_new - 1 - i], 1] = new_frame['position (t)'][
            matches['new index'][num_objects_new - 1 - i], 1]
        old_frame['size'][matches['old index'][num_objects_new - 1 - i]] = new_frame['size'][
            matches['new index'][num_objects_new - 1 - i]]
        old_frame['color'][num_objects_new - 1 - i] = [0, 1, 0]
        old_frame['match'][matches['old index'][num_objects_new - 1 - i]] = True
        new_frame['match'][matches['new index'][num_objects_new - 1 - i]] = True

        print("Old Index:", matches['old index'], ", New Index: ",
              matches['new index'],
              "\nOld Position:", old_frame['position (t)'][matches['old index'][num_objects_new - 1 - i]],
              ", New Position: ", new_frame['position (t)'][
                  matches['new index'][num_objects_new - 1 - i]],
              "Expected Position:", old_frame['position (t+1)'][matches['old index'][num_objects_new - 1 - i]])

    old_frame['velocity (t)'][:, 0] = (old_frame['position (t)'][:, 0] - old_frame['position (t-1)'][:, 0]) * 1.5
    old_frame['velocity (t)'][:, 1] = (old_frame['position (t)'][:, 1] - old_frame['position (t-1)'][:, 1]) * 1.5

    print("\n---------------------------------------\n\n")
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
                old_frame['id'] = 999
                old_frame['size'] = 10
            old_frame['position (t-1)'][i, 0] = -1000
            old_frame['position (t-1)'][i, 1] = -1000
            old_frame['position (t-2)'][i, 0] = -1000
            old_frame['position (t-2)'][i, 1] = -1000
            old_frame['velocity (t)'][i, 0] = 0
            old_frame['velocity (t)'][i, 1] = 0
            old_frame['velocity (t-1)'][i, 0] = 0
            old_frame['velocity (t-1)'][i, 1] = 0
            old_frame['velocity (t-2)'][i, 0] = 0
            old_frame['velocity (t-2)'][i, 1] = 0

    old_frame['position (t+1)'][:, 0] = old_frame['position (t)'][:, 0] + old_frame['velocity (t)'][:, 0] / 1.5
    old_frame['position (t+1)'][:, 1] = old_frame['position (t)'][:, 1] + old_frame['velocity (t)'][:, 1] / 1.5

    print(total_matches, "Matches from", num_objects_new, "Objects")
    print("Total Match %:", num_total_matches / num_total_objects * 100)

    for i in range(0, num_objects_old):
        print("Old Position:", old_frame['position (t-1)'][i], ", New Position: ", old_frame['position (t)'][i],
              "Next Position:", old_frame['position (t+1)'][i], ", Velocity: ", old_frame['velocity (t)'][i])
        # print("Old Frame Velocity:", old_frame['velocity (t)'][i, 0], "i,", old_frame['velocity (t)'][i, 1], "j")

    return old_frame
