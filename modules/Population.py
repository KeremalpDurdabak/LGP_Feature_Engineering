from modules.Dataset import Dataset
from modules.Individual import Individual
from modules.OperationSet import OperationSet
from modules.Parameter import Parameter
import random
import numpy as np

class Population:
    def __init__(self, label):
        # Initialize individuals with the population label
        self.label = label
        self.individuals = [Individual(label) for _ in range(Parameter.population_count)]

    def add_individual(self, individual):
        # Mark the individual as new and add to the population
        individual.is_new = True
        self.individuals.append(individual)

    def remove_individuals(self, individuals_to_remove):
        # Remove the specified individuals from the population
        self.individuals = [ind for ind in self.individuals if ind not in individuals_to_remove]

    def generate_children(self):
        # Calculate the number of children to generate
        num_children = Parameter.population_count - len(self.individuals)

        # Generate new children (this method needs to handle crossover and mutation)
        children = self.crossover_and_mutate(num_children)
        for child in children:
            child.is_new = True  # Mark the child as new
        self.individuals.extend(children)

    def crossover_and_mutate(self, num_children):
        children = []
        for _ in range(num_children):
            # Select two parents randomly from the top performers
            parents = random.sample(self.individuals[:int((1 - Parameter.gap_percentage) * len(self.individuals))], 2)
            child = self.crossover(parents[0], parents[1])
            self.mutate(child)
            children.append(child)
        return children

    def crossover(self, parent1, parent2):
        # Perform a single point crossover between two parents
        child_equation = []
        crossover_point = random.randint(1, len(parent1.equation) - 1)
        child_equation.extend(parent1.equation[:crossover_point])
        child_equation.extend(parent2.equation[crossover_point:])
        return Individual(self.label).with_equation(child_equation)

    def mutate(self, individual):
        # Randomly mutate an individual's equation
        for i in range(len(individual.equation)):
            if random.random() < Parameter.mutation_prob:
                # Mutate operation
                operation, _ = OperationSet.get_random_operation()
                individual.equation[i] = (operation, individual.equation[i][1])
                # Mutate operands
                if operation in ['add', 'subtract']:
                    operands = random.sample(range(Dataset.feature_count), 2)
                else:
                    operands = [random.choice(range(Dataset.feature_count)), 2]
                individual.equation[i] = (individual.equation[i][0], operands)

        # After mutation, the individual needs to be re-evaluated
        individual.evaluated = False
