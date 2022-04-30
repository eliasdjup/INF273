import numpy as np
import random
from statistics import mean
import time
import progressbar
import math
from pdp.operators.dummy_to_best import dummy_to_best
from pdp.operators.two_exchange_capacity import two_exhange_capacity
from pdp.operators.route_shuffle import route_shuffle

from pdp.utils import cost_function, feasibility_check, generate_s_0, load_problem


def simulated_annealing(s_0, instance, operators):
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
        operator = roulette_wheel(operators)
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
    a = (t_f / t_0) ** (1 / 9900)  # Division by zero error

    t = t_0

    for i in range(101, 10001):
        bar.update(i)
        operator = roulette_wheel(operators)
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


def roulette_wheel(operators):
    selection = random.uniform(0, 1)

    p1 = 0.2
    p2 = 0.4
    p3 = 0.4

    if selection < p1:
        return operators[0]
    elif selection < p1 + p2:
        return operators[1]
    else:
        return operators[2]


def main():
    # problems = ["./data/Call_7_Vehicle_3.txt"]
    problems = [
        "./pdp/data/Call_7_Vehicle_3.txt",
        "./pdp/data/Call_18_Vehicle_5.txt",
        "./pdp/data/Call_35_Vehicle_7.txt",
        "./pdp/data/Call_80_Vehicle_20.txt",
        "./pdp/data/Call_130_Vehicle_40.txt",
        "./pdp/data/Call_300_Vehicle_90.txt",
    ]

    operators = [two_exhange_capacity, dummy_to_best, route_shuffle]

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
            sol = simulated_annealing(s_0, prob, operators)

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
