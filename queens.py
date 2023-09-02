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

    return populationFitness, maxFitness, minFitness, sumFitness/len(population)

def queensSelection( population, populationFitness ):
    rouletteIndividual = random.randrange(sum(populationFitness))
    for i in range(len(population)):
        print(F'i={i} ({rouletteIndividual} <= {sum(populationFitness[:i])}') if __printdebug__ else None
        if rouletteIndividual <= sum(populationFitness[:i]):
            return population[i]
    return population[-1]
        
def queensOverlap( population, populationFitness ):
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
    individualSize = len(individual1)

    offspring1 = [0]*individualSize
    offspring2 = [0]*individualSize
    point1 = random.randrange(individualSize)

    for i in range(point1, point1+int(individualSize/2)):
        offspring1[i%individualSize] = individual1[i%individualSize]
        offspring2[i%individualSize] = individual2[i%individualSize]
    j=0
    k=0
    for i in range(individualSize):
        if offspring1[i] == 0:
            while(individual2[j] in offspring1):
                j +=1
            offspring1[i]=individual2[j]
            while(individual1[k] in offspring2):
                k +=1
            offspring2[i]=individual1[k]
    return offspring1, offspring2

def queensGeneticPlotStatistics( filename, parameters, statistics ):
    dpi = 120
    figsize = (16,16)
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    #plt.figure(figsize=figsize, dpi=dpi)
    plt.title(parameters)
    ax.plot(statistics[0])
    ax.plot(statistics[1])
    ax.plot(statistics[2])
    plt.legend( labels=['maxFitness', 'minFitness', 'sumFitness'] )
    plt.savefig(filename)
    plt.show() if __printdebug__ else None
    plt.close('all')
    return

def queensGenetic( individualSize, populationSize, weight_parameters, stop_generations, stop_maxFitness, stop_avgFitness ):
    # weight_parameters = [ mutation_weight, overlap_weight, crossover_weight ]
    print(f'queensGenetic( {individualSize}, {populationSize}, [ mutation_weight, overlap_weight, crossover_weight ] = {weight_parameters}, {stop_generations}, {stop_maxFitness}, {stop_avgFitness} )')
    population = createPopulation( populationSize, individualSize)
    statistics = [[],[],[]]
    generation = 0
    while( generation < stop_generations ):
        offsprings = []
        populationFitness, maxFitness, minFitness, avgFitness = queensPopulationFitness( population )
        statistics[0] += [maxFitness]
        statistics[1] += [minFitness] 
        statistics[2] += [avgFitness]
        # print(f'individualSize = {individualSize}, populationSize = {len(population)}, generation = {generation:4d}, maxFitness={maxFitness}, minFitness={minFitness}, avgFitness={avgFitness}')
        if( maxFitness >= stop_maxFitness):
            break;
        if( avgFitness >= stop_avgFitness):
            break;
        while (len(offsprings)<populationSize):
            rouletteOperation = random.randrange( sum(weight_parameters))
            # print(f'{len(offsprings)}, rouletteOperation = {rouletteOperation}, weight_parameters = {weight_parameters} ')
            if rouletteOperation < weight_parameters[0]: #mutation
                print(f'mutation') if __printdebug__ else None
                individual = queensMutation(population,populationFitness)
                if not individual in offsprings:
                    offsprings += [individual]
            elif rouletteOperation < weight_parameters[0]+weight_parameters[1]: #overlap
                print(f'overlap') if __printdebug__ else None
                individual = queensOverlap(population,populationFitness)
                if not individual in offsprings: 
                    offsprings += [individual]
            else: # crossover
                print(f'crossover') if __printdebug__ else None
                offspring1, offspring2 = queensCrossover(population,populationFitness)
                if not (offspring1 in offsprings or offspring2 in offsprings): 
                    offsprings += [offspring1]+[offspring2]
            #
        population = offsprings[:populationSize]
        generation += 1
    print(f'{individualSize} Queens Genetic, generations={generation}, maxFitness={maxFitness}, minFitness={minFitness}, avgFitness={avgFitness}')
    queensGeneticPlotStatistics(f'{individualSize}_Queens_Genetic', 
                                f'generations={generation}, ' +
                                f'individualSize={individualSize}, populationSize={populationSize}, \n'+
                                f'weight_parameters ([mutation_weight,overlap_weight,crossover_weight])={weight_parameters}, stop_generations={stop_generations}, '+
                                f'stop_maxFitness={stop_maxFitness}, stop_avgFitness={stop_avgFitness}', 
                                statistics)
    #print(f'maxFitness={maxFitness}, minFitness={minFitness}, avgFitness={avgFitness}')
    print(f'populationFitness={populationFitness}')
    print(f'statistics[0]={statistics[0]}')
    print(f'statistics[1]={statistics[1]}')
    print(f'statistics[2]={statistics[2]}')
    return population

def main_bruteforce():
    solutions={}
    # solve from n=1 to n=12 by brute force
    filename = 'solutions-nqueens-bruteforce.json'
    with open(filename,'w') as f:
        f.write('\n')
    for n in range(1,13):
        startTime=datetime.now()
        solutions[f'{n}_Queens'] = queensBruteForce(n)
        finishTime=datetime.now()
        print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}, '
              + f'{n} Queens Solutions ({len(solutions[f"{n}_Queens"])} best solutions)')
        print(f'solutions[f\'{n}_Queens\'] = {solutions[f"{n}_Queens"]}')
        # write solution to a file
        with open(filename,'a') as f:
            json.dump({f'{n}_Queens':solutions[f'{n}_Queens']},f)
            f.write('\n')

def main_genetics():
    solutions={}
    # solve from n=5 to n=12 by brute force
    filename = 'solutions-nqueens-genetics.json'
    with open(filename,'w') as f:
        f.write('\n')
    for n in range(13,20):
        startTime=datetime.now()
        solutions[f'{n}_Queens'] = queensGenetic( n, 100, [2,2,96], 200, queensMaxFitness(n), 10000 )
        finishTime=datetime.now()
        print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}, ' +
               f'{n} Queens Solutions ({len(solutions[f"{n}_Queens"])} best solutions)')
        print(f'solutions[f\'{n}_Queens\'] = {solutions[f"{n}_Queens"]}')
        # write solution to a file
        with open(filename,'a') as f:
            json.dump({f'{n}_Queens':solutions[f'{n}_Queens']},f)
            f.write('\n')

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main_genetics()
    # track execution time
    finishTime=datetime.now()
    print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')

