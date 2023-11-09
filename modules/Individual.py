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
                operands = random.sample(Dataset.feature_names, 2)
            else:
                operands = [random.choice(Dataset.feature_names), '2']

            self.equation.append((operation, operands))

        # Evaluate the individual's equation using the training data
        #self.evaluate(Dataset.X_train.values)

    def evaluate(self, data):
        # The data parameter is expected to be a NumPy array where each row corresponds to an instance
        # and each column corresponds to a feature.

        results = np.zeros(data.shape[0])

        for operation, operands in self.equation:
            operation_func = OperationSet.OPERATIONS[operation]

            if operation in ['add', 'subtract']:
                operand_indices = [Dataset.feature_names.index(op) for op in operands]
                results += operation_func(data[:, operand_indices[0]], data[:, operand_indices[1]])
            else:
                operand_index = Dataset.feature_names.index(operands[0])
                # For 'multiply' and 'divide', the second operand is always 2
                results += operation_func(data[:, operand_index], 2)

        # Store the evaluation results
        self.value = results
        return results

    def __str__(self):
        equation_parts = []
        for operation, operands in self.equation:
            if operation in ['add', 'subtract']:
                equation_parts.append(f"({operands[0]} {operation} {operands[1]})")
            else:
                equation_parts.append(f"({operands[0]} {operation} 2)")

        return ' '.join(equation_parts)
