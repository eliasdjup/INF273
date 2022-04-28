import numpy as np
import random
from statistics import mean
import time
from operators.one_insert import one_insert
from operators.two_exchange import two_exchange
from operators.three_exchange import three_exchange
import progressbar
import math

from utils import cost_function, feasibility_check, generate_s_0, load_problem


def simulated_annealing(s_0, instance, operator):
    best_s = [s_0, cost_function(s_0, instance)]
    incumbent = [s_0, cost_function(s_0, instance)]
    t_f = 0.1

    delta_w = []

    bar = progressbar.ProgressBar(
        maxval=10000,
        widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
    )
    bar.start()

    for w in range(1, 101):
        bar.update(w)
        new_s = operator(incumbent, instance)
        new_s_feasiblity, c = feasibility_check(new_s, instance)

        if new_s_feasiblity:
            new_s_cost = cost_function(new_s, instance)
            delta_e = new_s_cost - incumbent[1]
            if delta_e < 0.8:
                incumbent = [new_s, new_s_cost]
                if incumbent[1] < best_s[1]:
                    best_s = incumbent

            else:
                if random.uniform(0, 1) < 0.8:
                    incumbent = [new_s, new_s_cost]
                delta_w.append(delta_e)

    delta_avg = 0 if len(delta_w) == 0 else mean(delta_w)
    t_0 = -delta_avg / (np.log(0.8))
    a = (t_f / t_0) ** (1 / 9900)

    t = t_0

    for i in range(101, 10001):
        bar.update(i)
        new_s = operator(incumbent, instance)
        new_s_feasiblity, c = feasibility_check(new_s, instance)

        if new_s_feasiblity:
            new_s_cost = cost_function(new_s, instance)
            delta_e = new_s_cost - incumbent[1]

            if delta_e < 0:
                incumbent = [new_s, new_s_cost]
                if incumbent[1] < best_s[1]:
                    best_s = incumbent

            elif random.uniform(0, 1) < math.e ** (-delta_e / t):
                incumbent = [new_s, new_s_cost]

        t = a * t
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
    print("---------------Simulated Annealing---------------")
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
            sol = simulated_annealing(s_0, prob, three_exchange)

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
