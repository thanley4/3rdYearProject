import math
import numpy as np

num_objects_in_frame = 10

frame_time = 1 / 30  # seconds
max_acceleration_or_decceleration = 7  # G

objects_in_frame = np.zeros(num_objects_in_frame, dtype=[('position (t)', float, (2,)),
                                                         ('velocity (t)', float, (2,)),
                                                         ('id', int),
                                                         ('size', float)])

objects_in_frame['position (t)'][:, 0] = np.random.uniform(0, 1920, num_objects_in_frame)
objects_in_frame['position (t)'][:, 1] = np.random.uniform(0, 1080, num_objects_in_frame)
objects_in_frame['velocity (t)'][:, 0] = np.random.uniform(-30, 30, num_objects_in_frame)
objects_in_frame['velocity (t)'][:, 1] = np.random.uniform(-30, 30, num_objects_in_frame)
objects_in_frame['id'] = np.random.uniform(0, 20, num_objects_in_frame)
objects_in_frame['size'] = 10

objects_in_new_frame = np.zeros(num_objects_in_frame, dtype=[('position (t)', float, (2,)),
                                                             ('id', int),
                                                             ('size', float)])

objects_in_new_frame['position (t)'][:, 0] = objects_in_frame['position (t)'][:, 0] + np.random.uniform(-15, 15, num_objects_in_frame)
objects_in_new_frame['position (t)'][:, 1] = objects_in_frame['position (t)'][:, 1] + np.random.uniform(-15, 15, num_objects_in_frame)
objects_in_new_frame['id'] = objects_in_frame['id']
objects_in_new_frame['size'] = 10

matches = np.zeros(num_objects_in_frame, dtype=[('error', float,), ('old index', int), ('new index', int)])

print("Old Frame: ")
print(objects_in_frame)
print("\nNew Frame: ")
print(objects_in_new_frame)

total_matches = 0

for i in range(0, num_objects_in_frame):
    x = []
    errors = []
    max_error = round(frame_time * math.sqrt((objects_in_frame['velocity (t)'][i, 0] ** 2) + (
            objects_in_frame['velocity (t)'][i, 1] ** 2)) + 0.5 * max_acceleration_or_decceleration * (
                        frame_time ** 2), 3)
    print("\nMax Error: ")
    print(max_error)
    num_matches = 0
    for j in range(0, num_objects_in_frame):
        # expected position minus this error

        error = round(math.sqrt((((objects_in_frame['position (t)'][i, 0] - objects_in_new_frame['position (t)'][j, 0] +
                            (objects_in_frame['velocity (t)'][i, 0] * frame_time)) / 20) ** 2) +
                          (((objects_in_frame['position (t)'][i, 1] - objects_in_new_frame['position (t)'][j, 1] +
                            (objects_in_frame['velocity (t)'][i, 1] * frame_time)) / 20) ** 2)), 3)

        errors.append(error)

        x.append(int(objects_in_frame['id'][i] == objects_in_new_frame['id'][j]) and int(error <= max_error))
        if x[j] == 1:
            matches['error'][total_matches] = error
            matches['old index'][total_matches] = i
            matches['new index'][total_matches] = j
            num_matches = num_matches + 1
            total_matches = total_matches + 1


    print(num_matches, "Match(es)")
    print("Errors: ")
    print(x)
    print(errors)
    x.clear()
    errors.clear()
    num_matches = 0

print("\nMatching Vectors")
print(matches)

matches.sort(order='error')

print("\nSorted Matching Vectors")
print(matches)

for i in range(0, total_matches):
    print("Object ", matches['old index'][num_objects_in_frame - 1 - i], " is now Object ", matches['new index'][num_objects_in_frame - 1 - i])
