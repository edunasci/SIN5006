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
    return((1+individualSize)*individualSize/2)

def queensFitness( individual ):
    fitness = queensMaxFitness( len(individual) )  # starts with maximum fitness
    for i in range(len(individual)):
        for j in range(1,len(individual)-i):
            print(f'i={i}, j={j}, startfitness={fitness}') if __printdebug__ else None
            # other queen on the same line, decrease fitness by 1
            fitness -= 1 if individual[i]==individual[i+j] else 0
            # other queen on the same ascendent diagnoal, decrease fitness by 1
            fitness -= 1 if individual[i]==(individual[i+j]+j) else 0
            # other queen on the same descendent diagnoal, decrease fitness by 1
            fitness -= 1 if individual[i]==(individual[i+j]-j) else 0
            print(f'i={i}, j={j}, stopfitness={fitness}\n') if __printdebug__ else None
    print(f'individual = {individual}, fitness = {fitness}') if __printdebug__ else None
    return fitness

    
def queensBruteForce( individualSize ):
    solution = []
    firstindividual = []
    maxFitness = queensMaxFitness( individualSize )
    for i in range(1, individualSize+1):
        firstindividual += [i]
    for individual in itertools.permutations(firstindividual,r=individualSize):
        if( queensFitness(individual) == maxFitness ):
            solution += [individual]
    return solution

def main():
    solutions={}
    # solve from n=1 to n=12 by brute force
    for n in range(1,13):
        print(f'{datetime.now().replace(microsecond=0)}')
        solutions[f'{n}_Queens'] = queensBruteForce(n)
        print(f'\n\n{n} Queens Solutions ({len(solutions[f"{n}_Queens"])} best solutions):')
        print(f'solutions[f\'{n}_Queens\'] = {solutions[f"{n}_Queens"]}')
    
    # write solution to a file
    with open('Solutions.csv','w') as f:
        json.dump(solutions,f,indent=4)

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\n\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')