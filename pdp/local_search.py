import glob
import os
from math import ceil
from statistics import mean
from utils import *
from random import randrange, shuffle
import time


def local_search(s_0, prob, operator, n_iterations=10000):
    best_s = [s_0, cost_function(s_0, prob)]

    for i in range(1, n_iterations + 1):
        curr_sol = operator(best_s[0])
        curr_feasiblity, c = feasibility_check(curr_sol, prob)
        curr_cost = cost_function(curr_sol, prob)
        if curr_feasiblity and curr_cost < best_s[1]:
            best_s = [curr_sol, curr_cost]
    return best_s


def reinsert():
    return


def exchange_2():
    return


def exchange_3():
    return


def main():
    # os.chdir(r"/home/elias/Projects/INF273/pdp_py/data")
    # problems = glob.glob("*.txt")
    problems = [
        "./data/Call_7_Vehicle_3.txt",
        "./data/Call_18_Vehicle_5.txt",
        "./data/Call_35_Vehicle_7.txt",
    ]

    for file in problems:
        print("-------------------------------------------")
        print("Problem: ", file)

        prob = load_problem(file)

        s_0 = generate_s_0(prob["n_vehicles"], prob["n_calls"])
        cost_s0 = cost_function(s_0, prob)

        runs = []

        for test_ in range(1, 11):
            start_time = time.time()
            sol = local_search(s_0, prob)

            end_time = time.time()
            dur = end_time - start_time
            sol.append(dur)
            runs.append(sol)

        runs.sort(key=lambda x: x[1])
        avg_obj = mean([obj[1] for obj in runs])
        best = runs[0]
        improvement = 100 * (cost_s0 - best[1]) / best[1]

        print("Avg objective: ", avg_obj)
        print("Best objective: ", best[1])
        print("Improvement : ", improvement, "%")
        print("Running time : ", best[2])


main()
