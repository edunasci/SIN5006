#!/usr/bin/env python3
"""
queens.py - Solve n queens problem
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2023-08-27'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = ''
__status__      = 'Production'
__printdebug__  = False

from datetime import datetime
import random
import json
import itertools
import math
import numpy as np
import matplotlib.pyplot as plt

def createIndividual( individualSize ):
    individual=[]
    for i in range(1,individualSize+1):
        individual += [i]
        random.shuffle( individual )
    return individual

def createPopulation( populationSize, individualSize ):
    population = []
    for i in range(populationSize):
        population += [createIndividual(individualSize)]
    return population

def queensMaxFitness( individualSize ):
    return((1+individualSize)*individualSize/2*10+1)

def queensFitness( individual ):
    fitness = queensMaxFitness( len(individual) )  # starts with maximum fitness
    for i in range(len(individual)):
        for j in range(1,len(individual)-i):
            print(f'i={i}, j={j}, startfitness={fitness}') if __printdebug__ else None
            # other queen on the same line, decrease fitness by 1
            fitness -= 10 if individual[i]==individual[i+j] else 0
            # other queen on the same ascendent diagnoal, decrease fitness by 1
            fitness -= 10 if individual[i]==(individual[i+j]+j) else 0
            # other queen on the same descendent diagnoal, decrease fitness by 1
            fitness -= 10 if individual[i]==(individual[i+j]-j) else 0
            print(f'i={i}, j={j}, stopfitness={fitness}\n') if __printdebug__ else None
    print(f'individual = {individual}, fitness = {fitness}') if __printdebug__ else None
    return fitness

def queensPlotSolution( title, fitness ):
    dpi = 120
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    plt.figure(figsize=(6.4, 6.4), dpi=dpi)
    plt.title(title)
    plt.plot(fitness)
    plt.savefig(title.replace(' ','_'))
    plt.close('all')
    return

def queensBruteForce( individualSize ):
    solution = []
    firstindividual = []
    print(f'Starting queensBruteForce({individualSize})')
    maxFitness = queensMaxFitness( individualSize )
    for i in range(1, individualSize+1):
        firstindividual += [i]
    i=0
    print(f'initializing fitness..')
    fitness = np.zeros(math.factorial(individualSize),dtype='i2')
    print(f'starting permutations..')
    for individual in itertools.permutations(firstindividual,r=individualSize):
        fitness[i] = queensFitness(individual)
        if( fitness[i] == maxFitness ):
            solution += [individual]
        i += 1
    print(f'ploting solution..')
    queensPlotSolution( f'{individualSize} Queens Problem', fitness )
    print(f'Stopping queensBruteForce({individualSize})')
    return solution

def queensPopulationFitness( population ):
    ###
    return maxfitness, maxfitness, totalfitness

def queensReproduction( individual ):
    ###
    return individual

def queensMutation( individual ):
    ###
    return individual

def queensCrossover( individual1, individual2 ):
    ###
    return individual

def queensGenetic( individualSize, populationSize, weight_parameters, stop_generations, stop_maxfitness, stop_totalfitness ):
    # weight_parameters = [ mutation_weight, reproduction_weight, crossover_weight ]
    population = createPopulation( populationSize, individualSize)
    generationPopulation = []
    generation = 0
    while( generation < stop_generations ):
        maxfitness, maxfitness, totalfitness = queensPopulationFitness( population )
        if( maxfitness >= stop_maxfitness):
            break;
        if( totalfitness >= stop_totalfitness):
            break;
        while (len(generation)<populationSize):
            # select operation
            # select individuals
            # perform operation
            # increment generation
        population = generationPopulation[:populationSize]
    return population

def main():
    solutions={}
    # solve from n=1 to n=12 by brute force
    with open('solutions-nqueens.json','w') as f:
        f.write('\n')
    for n in range(1,13):
        startTime=datetime.now()
        solutions[f'{n}_Queens'] = queensBruteForce(n)
        finishTime=datetime.now()
        print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}, '
              + f'{n} Queens Solutions ({len(solutions[f"{n}_Queens"])} best solutions)')
        print(f'solutions[f\'{n}_Queens\'] = {solutions[f"{n}_Queens"]}')
        # write solution to a file
        with open('solutions-nqueens.json','a') as f:
            json.dump({f'{n}_Queens':solutions[f'{n}_Queens']},f)
            f.write('\n')

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')

