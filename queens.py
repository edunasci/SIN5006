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
    return(int((1+individualSize)*individualSize/2*10+1))

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
    fitness = np.zeros(math.factorial(individualSize),'i2')
    print(f'starting permutations..')
    for individual in itertools.permutations(firstindividual,r=individualSize):
        fitness[i] = queensFitness(individual)
        if( fitness[i] == maxFitness ):
            solution += [individual]
        i += 1
    if individualSize<10:
        print(f'ploting solution... (len(fitness)={len(fitness)})')
        queensPlotSolution( f'img/{individualSize} Queens Problem', fitness )
    print(f'Stopping queensBruteForce({individualSize})')
    return solution

def queensPopulationFitness( population ):
    populationFitness = np.zeros(len(population),'i2')
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
        if rouletteIndividual < sum(populationFitness[:i]):
            return population[i]
    return population[-1]
        
def queensOverlap( population, populationFitness ):
    return queensSelection( population, populationFitness )
    
def queensMutation(  population, populationFitness ):
    # chapter 32 - Mutation Operators (Back et al, Evolationary Computation 1: Basic Algorithms and Operators)
    # 32.3.3 Insert, swap, and scramble operators
    # SWAP 
    individual = queensSelection( population, populationFitness )
    individualSize = len(individual)
    offspring = individual[:]
    point1 = random.randrange(individualSize)
    point2 = random.randrange(individualSize)
    while point2 == point1:
        point2 = random.randrange(individualSize)
    offspring[point1]=individual[point2]
    offspring[point2]=individual[point1]
    return offspring

def queensCrossover(  population, populationFitness ):
    # chapter 33 -Recombination - (Back et al, Evolationary Computation 1: Basic Algorithms and Operators)
    # 33.3 Permutations 
    # Davis’s order crossover
    individual1 = queensSelection( population, populationFitness )
    individual2 = queensSelection( population, populationFitness )
    individualSize = len(individual1)
    point1 = random.randrange(individualSize)
    point2 = random.randrange(individualSize)
    while point2 == point1:
        point2 = random.randrange(individualSize)
    point1,point2 = min(point1,point2),max(point1,point2)+1
    offspring = [0]*individualSize
    offspring[point1:point2] = individual1[point1:point2]
    for i in range(individualSize):
        if not individual2[i] in offspring:
            offspring[point2%individualSize] = individual2[i]
            point2 += 1
    return offspring

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
    plt.legend( labels=['maxFitness', 'minFitness', 'avgFitness'] )
    plt.savefig(filename)
    plt.show() if __printdebug__ else None
    plt.close('all')
    return

def queensGeneticPlotChessboard( filename, title, individual ):
    dpi = 120
    figsize = (8,8)
    black_queen = '\u265b'
    n=len(individual)
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    #plt.figure(figsize=figsize, dpi=dpi)
    plt.title(title)
    #create chessboard
    board = []
    for i in range(n):
        line=[]
        for j in range(n):
            line += [([((i+j)%2)*63+128]*3)]
        board += [line]
    ax.set_axis_off()
    ax.imshow(board,origin='lower',extent=(0,n,0,n))
    for i in range(n):
        ax.text(i+0.5,(individual[i]-0.5),black_queen,
                ha='center',va='center',color='black',
                fontweight='bold', fontfamily='monospace',fontsize=20)
    plt.savefig(filename)
    plt.show() if __printdebug__ else None
    plt.close('all')
    return

def queensGenetic( individualSize, populationSize, weight_parameters, stop_generations, stop_maxFitness, stop_avgFitness ):
    # weight_parameters = [ mutation_weight, overlap_weight, crossover_weight, elitism_weight ]
    print(f'queensGenetic( {individualSize}, {populationSize}, [ mutation_weight, overlap_weight, crossover_weight, elitism_weight ] = {weight_parameters}, {stop_generations}, {stop_maxFitness}, {stop_avgFitness} )')
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
            rouletteOperation = random.randrange( sum(weight_parameters[0:2]) )
            # print(f'{len(offsprings)}, rouletteOperation = {rouletteOperation}, weight_parameters = {weight_parameters} ')
            if rouletteOperation < weight_parameters[0]: #mutation
                print(f'mutation') if __printdebug__ else None
                individual = queensMutation(population,populationFitness)
            elif rouletteOperation < weight_parameters[0]+weight_parameters[1]: #overlap
                print(f'overlap') if __printdebug__ else None
                individual = queensOverlap(population,populationFitness)
            else: # crossover
                print(f'crossover') if __printdebug__ else None
                individual = queensCrossover(population,populationFitness)
            if not individual in offsprings:  # add individual, if not repeated offspring
                offsprings += [individual]
            #
        offsprings = offsprings[:populationSize]
        # apply elitism
        elite =[]
        i = 0
        while len(elite) < weight_parameters[3] and len(elite)<populationSize:
            if populationFitness[i] == max(populationFitness):
               #print(f'generation = {generation:4d}, max(populationFitness) = {max(populationFitness)}, population[{i:3d}]={population[i]} ')
               print(f'generation = {generation:4d}, population[{i:3d}]={population[i]} = {generation:4d}, fitness({population[i]} = {populationFitness[i]}, max(populationFitness)={max(populationFitness)}') if __printdebug__ else None
               populationFitness[i] = 0
               elite += [population[i]]
            i += 1
            i = i%populationSize
        offspringsFitness, maxOffspringsFitness, minOffpringsFitness, avgOffspringsFitness = queensPopulationFitness( offsprings )
        i = 0
        elitetmp = elite
        while len(elite) > 0:
            if elite[-1] in offsprings:
                elite = elite[:-1] # do not duplicate
                continue
            if offspringsFitness[i] == min(offspringsFitness):
                offspringsFitness[i] = queensFitness(elite[-1])
                offsprings[i]= elite[-1]
                elite = elite[:-1]
            i += 1
            i = i%populationSize
        offspringsFitness, maxOffspringsFitness, minOffpringsFitness, avgOffspringsFitness = queensPopulationFitness( offsprings )
        if maxOffspringsFitness < maxFitness:
            print(f'Error maxOffspringsFitness({maxOffspringsFitness}) < maxFitness({maxFitness})')
            exit(-1)
        population = offsprings
        generation += 1
    print(f'{individualSize} Queens Genetic, generations={generation}, maxFitness={maxFitness}, minFitness={minFitness}, avgFitness={avgFitness}')
    queensGeneticPlotStatistics(f'img/{individualSize}_Queens_Genetic', 
                                f'generations={generation}, ' +
                                f'individualSize={individualSize}, populationSize={populationSize}, \n'+
                                f'weight_parameters ([mutation_weight,overlap_weight,crossover_weight,elitism_weight])={weight_parameters}, stop_generations={stop_generations}, '+
                                f'stop_maxFitness={stop_maxFitness}, stop_avgFitness={stop_avgFitness}', 
                                statistics)
    individual = population[list(populationFitness).index(max(populationFitness))]
    queensGeneticPlotChessboard( f'img/{individualSize}_Queens_Genetic_Chessboard', 
                                f'{individualSize} Queens - Solution ={individual}\n'+
                                f'Fitness = {max(populationFitness)} of {queensMaxFitness(individualSize)}', 
                                individual)
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
    filename = 'solutions-nqueens-genetics.json'
    with open(filename,'w') as f:
        f.write('\n')
    # solve from n=5 to n=50 by Genetic Algorithm
    for n in range(5,51):
        startTime=datetime.now()
        # weight_parameters = [ mutation_weight, overlap_weight, crossover_weight, elitism_weight ]
        solutions[f'{n}_Queens'] = queensGenetic( n, 100, [1,0,99,5], 2000, queensMaxFitness(n), 32000 )
        finishTime=datetime.now()
        print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}, ' +
               f'{n} Queens Solutions')
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

### Queens Genetics 2000:
### Start: 2023-09-02 15:28:43, Finish:2023-09-02 15:46:24, Running Time: 0:17:41.784603
