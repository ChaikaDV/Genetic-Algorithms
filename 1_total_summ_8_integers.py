### This algorithm written as an example of how
### genetic algorithm could\shoud work
###
### Here it solves a little problem of maximizing value of genes
### Summ of value for chromosome should be equal to its length
### Values for genes are 1 or 0 (just integers)

from random import randint


class GeneticAlgorithm:
    """
    Genetic algorithms are commonly used to generate
    high-quality solutions to optimization and search problems

    :param gene_number       is a number of genes
    :param chromosome_number is a number of chomosomes
    :param value_needed      is a value closer to which result should be
    :param limit             is optional value, sets limit of iterations (executed loop will be for loop), if limit is not set
                             it automatically sets limit as infinity (executed loop will be while loop)

    Pseudocode:
    START
        Generate the initial population
        Compute fitness
        REPEAT
            Selection
            Crossover
            Mutation
            Compute fitness
        UNTIL population has converged
    STOP

    """

    def __init__(self, gene_number, chromosome_number, mutation_chance, limit):
        l = self.initialize_population(gene_number, chromosome_number)
        print('Start : ')
        for i, chromosome in enumerate(l):
            print(f'#{i} {chromosome} summ : {sum(chromosome)}')

        l, probabilities = self.fitness(l)
        for i_to_limit in range(limit):
            _l = self.crossover(l)
            _l = self.mutation(_l, mutation_chance)
            _l, probabilities = self.fitness(_l)
            l = _l
        print('Result : ')
        for i, chromosome in enumerate(l):
            print(f'#{i} {chromosome} summ : {sum(chromosome)}')

    def initialize_population(self, gene_number, chromosome_number):
        """
        Initializing population to work with
        :return: list with population (Chomosomes and genes)
        """
        l = []
        for chromosome in range(chromosome_number):
            l.append([])
            for gene in range(gene_number):
                l[-1].append(randint(0, 1))
        return l

    def fitness(self, l):
        """
        It is vitally important function, which defines are parameters
        fit or not for the solution
        :param l: list with  population
        :return: probability that individual will be selected for further reproduction
        """

        values = {}
        for i, chromosome in enumerate(l):
            _summ = sum(chromosome)
            values[i] = _summ
            number_of_chromosome = len(chromosome)

        # define how close solutions to required result and get possibilities
        _values = []
        for i in values:
            _values.append((values[i], i)) # sum : index
        probabilities = []
        total_summ = 0
        for _s, i in _values:
            total_summ = total_summ + _s
        for s, i in _values:
            probabilities.append((round(s/total_summ, 4), i))
        probabilities.sort(key=lambda tup: tup[0])

        probabilities = probabilities[len(probabilities)-number_of_chromosome:] # choose the best from all population

        _l = []
        for percentage, index in probabilities:
            _l.append(l[index])

        return _l, probabilities

    def crossover(self, l):
        """
        Get all off-springs  (population size = a(i) ... a(i+1) )
        Here we use 'One Point Crossover'

        :return: new l
        """
        _l = []
        for i, chromosome_i in enumerate(l):
            for j in range(i + 1, len(l)):
                parent_1 = l[i]
                parent_2 = l[j]
                new_parent_1_left = l[i][:len(l[i])//2]
                new_parent_1_right = l[j][len(l[i])//2:]
                new_parent_2_left = l[j][:len(l[j])//2]
                new_parent_2_right = l[i][len(l[j])//2:]
                new_parent_1 = []
                new_parent_1.extend(new_parent_1_left)
                new_parent_1.extend(new_parent_1_right)
                new_parent_2 = []
                new_parent_2.extend(new_parent_2_left)
                new_parent_2.extend(new_parent_2_right)
                _l.append(new_parent_1)
                _l.append(new_parent_2)

        return _l

    def mutation(self, _l, mutation_chance):
        """
        For some chromosomes add mutation
        :return: list with mutated chromosomes
        """

        mutation_chance = mutation_chance*100
        for i, chromosome in enumerate(_l):
            if randint(0, 100) <= mutation_chance:
                # mutate
                _l[i][randint(0, len(chromosome)) - 1] = randint(0, 1)

        return _l

import time
start = time.perf_counter()
GeneticAlgorithm(gene_number=5, chromosome_number=8, mutation_chance=0.01, limit=100)
print(f'finished in {round(time.perf_counter() - start)} sec')

