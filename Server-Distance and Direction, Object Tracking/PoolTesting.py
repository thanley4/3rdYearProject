from multiprocessing import Pool
import time


def function(i, f):
    for j in range(1, 100000000):
        k = j * j / i
        l = k * k / j
        m = l * l / k
    print("F: ", f)
    print("I: ", i)
    return i


if __name__ == '__main__':
    start = time.process_time_ns()
    list_of_i = [1, 2, 3, 4, 5, 6]
    list_of_f = [3, 3, 3, 3, 3, 3]

    number_of_processes = 6

    with Pool(number_of_processes) as p:
        results = p.starmap(function, zip(list_of_i, list_of_f))
        print(results)

    print("Time Taken: ", (time.process_time_ns() - start) / 10000)
