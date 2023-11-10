import copy
import random
import numpy as np
from modules.Dataset import Dataset
from modules.OperationSet import OperationSet
from modules.Parameter import Parameter

class Individual:
    def __init__(self, population_label):
        self.population_label = population_label
        self.equation = []
        self.result = None  # This will store the evaluation result of the equation
        self.evaluated = False  # Flag to check if the individual's equation has been evaluated
        self.is_new = True  # Flag to indicate if the individual is new and needs evaluation

        # Initialize the individual with a random equation
        for _ in range(Parameter.operation_count):
            operation, func = OperationSet.get_random_operation()
            if operation in ['add', 'subtract']:
                operands = random.sample(range(Dataset.feature_count), 2)
            else:
                operands = [random.choice(range(Dataset.feature_count)), 2]
            self.equation.append((operation, operands))

    def evaluate(self, data):
        if not self.evaluated or self.is_new:
            results = np.zeros(data.shape[0])

            for operation, operands in self.equation:
                operation_func = OperationSet.OPERATIONS[operation]
                if operation in ['add', 'subtract']:
                    results += operation_func(data[:, operands[0]], data[:, operands[1]])
                else:
                    results += operation_func(data[:, operands[0]], 2)

            self.result = results
            self.evaluated = True
            self.is_new = False

        return self.result

    def with_equation(self, equation):
        # Optimized method to create a new Individual with the given equation
        new_individual = Individual(self.population_label)
        new_individual.equation = copy.deepcopy(equation)
        new_individual.evaluated = False
        new_individual.is_new = True
        return new_individual

    def __str__(self):
        # Optimized string representation
        equation_parts = [self.format_operation(operation, operands) for operation, operands in self.equation]
        return ' '.join(equation_parts)

    def format_operation(self, operation, operands):
        # Helper method to format an operation
        if operation in ['add', 'subtract']:
            return f"F{operands[0]} {'+' if operation == 'add' else '-'} F{operands[1]}"
        else:
            return f"F{operands[0]} {'*' if operation == 'multiply' else '/'} 2"