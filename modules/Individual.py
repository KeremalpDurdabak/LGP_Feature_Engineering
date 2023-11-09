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
        self.value = None  # This will store the evaluation results

        for _ in range(Parameter.operation_count):
            operation, func = OperationSet.get_random_operation()
            if operation in ['add', 'subtract']:
                operands = random.sample(range(Dataset.feature_count), 2)
            else:
                operands = [random.choice(range(Dataset.feature_count)), 2]

            self.equation.append((operation, operands))

    def evaluate(self, data):
        # The data parameter is expected to be a NumPy array where each row corresponds to an instance
        # and each column corresponds to a feature.

        results = np.zeros(data.shape[0])

        for operation, operands in self.equation:
            operation_func = OperationSet.OPERATIONS[operation]
            if operation in ['add', 'subtract']:
                results += operation_func(data[:, operands[0]], data[:, operands[1]])
            else:
                # For 'multiply' and 'divide', the second operand is always 2
                results += operation_func(data[:, operands[0]], 2)

        # Store the evaluation results
        self.value = results
        return results

    def __str__(self):
        equation_parts = []
        for operation, operands in self.equation:
            if operation in ['add', 'subtract']:
                equation_parts.append(f"(F{operands[0]} {operation} F{operands[1]})")
            else:
                equation_parts.append(f"(F{operands[0]} {operation} 2)")

        return ' '.join(equation_parts)

    def with_equation(self, equation):
        # Create a new Individual with the given equation
        new_individual = Individual(self.population_label)
        new_individual.equation = copy.deepcopy(equation)  # Ensure a deep copy
        return new_individual