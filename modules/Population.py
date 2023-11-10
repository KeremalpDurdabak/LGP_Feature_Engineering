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
        num_children = int(Parameter.population_count * Parameter.gap_percentage)

        # Generate new children (this method needs to handle crossover and mutation)
        children = self.crossover_and_mutate(num_children)
        for child in children:
            child.is_new = True  # Mark the child as new
        self.individuals.extend(children)

    def crossover_and_mutate(self, num_children):
        children = []
        while len(children) < num_children:
            # Ensure there are enough parents for crossover
            if len(self.individuals) < 2:
                raise Exception("Not enough parents for crossover")
            parents = random.sample(self.individuals, 2)

            # 50% chance to perform either single-point or double-point crossover
            if random.random() < 0.5:
                child1, child2 = self.single_point_crossover(parents[0], parents[1])
            else:
                child1, child2 = self.double_point_crossover(parents[0], parents[1])

            # Mutate both children
            self.mutate(child1)
            self.mutate(child2)

            # Add the children to the list
            children.extend([child1, child2])

        # Trim the list if it exceeds the desired number of children
        return children[:num_children]

    def single_point_crossover(self, parent1, parent2):
        # Choose a crossover point
        crossover_point = random.randint(1, len(parent1.equation) - 1)

        # Create the first child
        child1_equation = []
        child1_equation.extend(parent1.equation[:crossover_point])
        child1_equation.extend(parent2.equation[crossover_point:])
        child1 = Individual(self.label).with_equation(child1_equation)

        # Create the second child with reversed roles
        child2_equation = []
        child2_equation.extend(parent2.equation[:crossover_point])
        child2_equation.extend(parent1.equation[crossover_point:])
        child2 = Individual(self.label).with_equation(child2_equation)

        return child1, child2


    def double_point_crossover(self, parent1, parent2):
        # Choose two crossover points
        crossover_points = sorted(random.sample(range(1, len(parent1.equation)), 2))

        # Create the first child
        child1_equation = []
        child1_equation.extend(parent1.equation[:crossover_points[0]])
        child1_equation.extend(parent2.equation[crossover_points[0]:crossover_points[1]])
        child1_equation.extend(parent1.equation[crossover_points[1]:])
        child1 = Individual(self.label).with_equation(child1_equation)

        # Create the second child with reversed roles
        child2_equation = []
        child2_equation.extend(parent2.equation[:crossover_points[0]])
        child2_equation.extend(parent1.equation[crossover_points[0]:crossover_points[1]])
        child2_equation.extend(parent2.equation[crossover_points[1]:])
        child2 = Individual(self.label).with_equation(child2_equation)

        return child1, child2


    def mutate(self, individual):
        for i in range(len(individual.equation)):
            if random.random() < Parameter.mutation_prob:
                # Decide whether to mutate the operation or an operand
                if random.random() < 0.5:
                    # Mutate operation
                    operation, _ = OperationSet.get_random_operation()
                    individual.equation[i] = (operation, individual.equation[i][1])
                else:
                    # Mutate operands
                    if individual.equation[i][0] in ['add', 'subtract']:
                        operands = random.sample(range(Dataset.feature_count), 2)
                    else:
                        operands = [random.choice(range(Dataset.feature_count)), 2]
                    individual.equation[i] = (individual.equation[i][0], operands)
                # After mutation, the individual needs to be re-evaluated
                individual.evaluated = False