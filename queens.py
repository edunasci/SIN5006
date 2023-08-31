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
    if len(fitness)<1000:
       dpi = 120
       figsize = (16,16)
    elif len(fitness)<10000:
       dpi = 120
       figsize = (32,32)
    else:
       dpi = 60
       figsize = (128,128)
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    plt.figure(figsize=figsize, dpi=dpi)
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
    if individualSize<10:
        print(f'ploting solution... (len(fitness)={len(fitness)})')
        queensPlotSolution( f'{individualSize} Queens Problem', fitness )
    print(f'Stopping queensBruteForce({individualSize})')
    return solution

def queensPopulationFitness( population ):
    populationFitness = np.zeros(len(population),dtype='i2')
    maxFitness = 0
    minFitness = queensMaxFitness(len(population[0]))
    sumFitness = 0

    for i in range(len(population)):
        populationFitness[i] = queensFitness(population[i])
        maxFitness = max(populationFitness[i],maxFitness)
        minFitness = min(populationFitness[i],minFitness)
        sumFitness += populationFitness[i]

    return populationFitness, maxFitness, minFitness, sumFitness

def queensSelection( population, populationFitness ):
    rouletteIndividual = random.randrange(sum(populationFitness))
    for i in range(population):
        if rouletteIndividual <= sum(populationFitness[:i]):
            return population[i]
        
def queensReplicate( population, populationFitness ):
    return queensSelection( population, populationFitness )
    
def queensMutation(  population, populationFitness ):
    individual = queensSelection( population, populationFitness )
    point1 = random.randrange(len(individual))
    point2 = random.randrange(len(individual))
    tempgene = individual[point1]
    individual[point1] = individual[point2]
    individual[point2] = tempgene
    return individual

def queensCrossover(  population, populationFitness ):
    individual1 = queensSelection( population, populationFitness )
    individual2 = queensSelection( population, populationFitness )
    
    return individual

def queensGeneticPlotStatistics( title, fitness ):
    if len(fitness)<1000:
       dpi = 120
       figsize = (16,16)
    elif len(fitness)<10000:
       dpi = 120
       figsize = (32,32)
    else:
       dpi = 60
       figsize = (128,128)
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    plt.figure(figsize=figsize, dpi=dpi)
    plt.title(title)
    plt.plot(fitness)
    plt.savefig(title.replace(' ','_'))
    plt.close('all')
    return

def queensGenetic( individualSize, populationSize, weight_parameters, stop_generations, stop_maxFitness, stop_sumFitness ):
    # weight_parameters = [ mutation_weight, replicate_weight, crossover_weight ]
    population = createPopulation( populationSize, individualSize)
    offsprings = []
    generation = 0
    statistics = {}
    statistics['generation'] = []
    statistics['maxFitness'] = []
    statistics['minFitness'] = []
    statistics['sumFitness'] = []
    while( generation < stop_generations ):
        populationFitness, maxFitness, minFitness, sumFitness = queensPopulationFitness( population )
        if( maxFitness >= stop_maxfitness):
            break;
        if( sumFitness >= stop_sumFitness):
            break;
        while (len(generation)<populationSize):
            rouletteOperation = random.randrange( sum(weight_parameters))
            if rouuletteOperation < weight_parameters[0]: #mutation
                offsprings += [queensMutation(population)]
            elif roletteOperation < weight_parameters[0]+weight_parameters[1]: #replicate
                offsprings += [queensReplicate(population)]
            # select operation
            # select individuals
            # perform operation
            # increment generation
            generation += 1
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

