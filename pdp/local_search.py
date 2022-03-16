import glob
import os
from math import ceil
from statistics import mean
from random import randrange, shuffle, uniform
import time
from operators.one_insert import one_insert
from operators.two_exchange import two_exchange
from operators.three_exchange import three_exchange
import progressbar

from utils import cost_function, feasibility_check, generate_s_0, load_problem


def local_search(s_0, prob, operator):
    best_s = [s_0, cost_function(s_0, prob)]

    bar = progressbar.ProgressBar(
        maxval=10000,
        widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
    )
    bar.start()

    for i in range(1, 10001):
        bar.update(i)
        # print("----------------------------------------")
        current = operator(best_s, prob)
        # print(current)
        curr_feasiblity, c = feasibility_check(current, prob)
        curr_cost = cost_function(current, prob)

        # print(curr_feasiblity, curr_cost)

        if curr_feasiblity and curr_cost < best_s[1]:
            best_s = [current, curr_cost]
        # time.sleep(0.5)
    bar.finish()
    return best_s


def main():
    # os.chdir(r"/home/elias/Projects/INF273/pdp/data")
    # problems = glob.glob("*.txt")
    # problems = ["./data/Call_7_Vehicle_3.txt"]
    problems = [
        "./data/Call_7_Vehicle_3.txt",
        "./data/Call_18_Vehicle_5.txt",
        "./data/Call_35_Vehicle_7.txt",
        "./data/Call_80_Vehicle_20.txt",
        "./data/Call_130_Vehicle_40.txt",
        "./data/Call_300_Vehicle_90.txt",
    ]
    print("---------------Local Search---------------")
    for file in problems:
        print("-------------------------------------------")
        print("Problem: ", file)

        prob = load_problem(file)

        s_0 = generate_s_0(prob["n_vehicles"], prob["n_calls"])
        cost_s0 = cost_function(s_0, prob)

        runs = []

        for iteration in range(1, 11):
            print("Iteration " + str(iteration))
            start_time = time.time()
            sol = local_search(s_0, prob, three_exchange)

            end_time = time.time()
            dur = end_time - start_time
            sol.append(dur)
            runs.append(sol)

        runs.sort(key=lambda x: x[1])
        avg_obj = mean([obj[1] for obj in runs])
        best = runs[0]
        improvement = 100 * (cost_s0 - best[1]) / best[1]
        print("")
        print("Avg objective: ", avg_obj)
        print("Best solution: ", best[0])
        print("Best objective: ", best[1])
        print("Improvement : ", improvement, "%")
        print("Running time : ", best[2])


main()
