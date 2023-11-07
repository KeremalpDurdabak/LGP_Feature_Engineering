from dataclasses import dataclass


@dataclass
class Parameter:
    # Number of Individuals in the Population
    population_count = 100

    # Max Instruction (Row) per each Individual
    max_instruction = 32

    # Max number per each decode instruction (Source Select, Target Index, Source Index)
    # (Max number for the 'operator_select' is dynamically assumed by the OperatorSet class)
    source_select = 2
    target_index = 4
    source_index = 4 # 9 for tictactoe, 4 for iris, 8 for shuttle, 5 for thyroid
    operator_select = 4

    # Number of Registers to use
    register_count = 4

    # Percentage of worst fit Individuals to replace
    gap_percentage = 0.3

    # Generation Count
    generations = 1000

    # Probability of a Mutation
    mutation_prob = 0.3