import glob
import os
from math import ceil
from statistics import mean
from random import randrange, shuffle, uniform
import time
from operators.one_reinsert import one_reinsert

from utils import cost_function, feasibility_check, generate_s_0, load_problem


def local_search(s_0, prob, operator):
    best_s = [s_0, cost_function(s_0, prob)]

    for i in range(1, 10000):
        current = operator(best_s, prob)
        print(current)
        curr_feasiblity, c = feasibility_check(current, prob)
        curr_cost = cost_function(current, prob)

        print(curr_feasiblity, curr_cost)

        if curr_feasiblity and curr_cost < best_s[1]:
            best_s = [current, curr_cost]
    return best_s


def main():
    # os.chdir(r"/home/elias/Projects/INF273/pdp_py/data")
    # problems = glob.glob("*.txt")
    problems = ["./data/Call_7_Vehicle_3.txt"]
    print("---------------Local Search---------------")
    for file in problems:
        print("-------------------------------------------")
        print("Problem: ", file)

        prob = load_problem(file)

        s_0 = generate_s_0(prob["n_vehicles"], prob["n_calls"])
        cost_s0 = cost_function(s_0, prob)

        runs = []

        for test_ in range(1, 11):
            start_time = time.time()
            sol = local_search(s_0, prob, one_reinsert)

            end_time = time.time()
            dur = end_time - start_time
            sol.append(dur)
            runs.append(sol)

        runs.sort(key=lambda x: x[1])
        avg_obj = mean([obj[1] for obj in runs])
        best = runs[0]
        improvement = 100 * (cost_s0 - best[1]) / best[1]

        print("Avg objective: ", avg_obj)
        print("Best solution: ", best[0])
        print("Best objective: ", best[1])
        print("Improvement : ", improvement, "%")
        print("Running time : ", best[2])


main()
