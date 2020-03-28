#!/usr/bin/env python2.7
#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import multiprocessing
import random
import sys

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(verbose=True):
    random.seed(64)

    NGEN = 40
    CXPB = 0.5
    MUTPB = 0.1
    verbose = True

    # Process Pool of 4 workers
    pool = multiprocessing.Pool(processes=4)
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    algo = algorithms.GenerationalAlgorithm(pop, toolbox, cxpb=CXPB, mutpb=MUTPB)
    for gen, state in enumerate(algo):
        hof.update(state.population)

        record = stats.compile(state.population)
        logbook.record(gen=gen, nevals=state.nevals, **record)
        if verbose:
            print(logbook.stream)

        if gen >= NGEN:
            break

    pool.close()
    return pop, stats, hof


if __name__ == "__main__":
    if sys.version_info < (2, 7):
        print("mpga_onemax example requires Python >= 2.7.")
        exit(1)

    main()
