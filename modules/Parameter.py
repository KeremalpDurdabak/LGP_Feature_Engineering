from dataclasses import dataclass


@dataclass
class Parameter:
    # Number of Individuals in the Population
    population_count = 100

    # Max Instruction (Row) per each Individual
    operation_count = 10

    # Percentage of worst fit Individuals to replace
    gap_percentage = 0.5

    # Generation Count
    generations = 1000

    # Probability of a Mutation
    mutation_prob = 0.3
