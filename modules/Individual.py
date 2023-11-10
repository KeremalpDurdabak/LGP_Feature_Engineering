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
        # The data parameter is expected to be a NumPy array where each row corresponds to an instance
        # and each column corresponds to a feature.

        # Only evaluate if the individual has not been evaluated or if it's new
        if not self.evaluated or self.is_new:
            results = np.zeros(data.shape[0])

            for operation, operands in self.equation:
                operation_func = OperationSet.OPERATIONS[operation]
                if operation in ['add', 'subtract']:
                    results += operation_func(data[:, operands[0]], data[:, operands[1]])
                else:
                    # For 'multiply' and 'divide', the second operand is always 2
                    results += operation_func(data[:, operands[0]], 2)

            # Store the evaluation result
            self.result = results
            # Mark as evaluated
            self.evaluated = True
            self.is_new = False  # Reset the new flag after evaluation

        return self.result

    def with_equation(self, equation):
        # Create a new Individual with the given equation
        new_individual = copy.deepcopy(self)  # Deep copy of the current individual
        new_individual.equation = equation
        new_individual.evaluated = False  # New equation, needs to be evaluated
        new_individual.is_new = True  # Mark as new
        return new_individual


    def __str__(self):
        # Start with an empty list to hold parts of the equation
        equation_parts = []

        # Track the last operation to handle order of operations
        last_operation = None

        for operation, operands in self.equation:
            # For add and subtract, we'll group with parentheses
            if operation in ['add', 'subtract']:
                # If the last operation was multiply or divide, we need to enclose the previous part in parentheses
                if last_operation in ['multiply', 'divide']:
                    equation_parts[-1] = f"({equation_parts[-1]})"
                # Append the current operation with its operands
                equation_parts.append(f"F{operands[0]} {'+' if operation == 'add' else '-'} F{operands[1]}")
            else:
                # For multiply and divide, just append the operation
                equation_parts.append(f"F{operands[0]} {'*' if operation == 'multiply' else '/'} 2")

            # Update the last operation
            last_operation = operation

        # Combine the parts into one string with proper order of operations
        return ' '.join(equation_parts)