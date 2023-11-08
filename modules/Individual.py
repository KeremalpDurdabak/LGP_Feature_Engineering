import random
from modules.Parameter import Parameter
from modules.OperationSet import OperationSet

class Individual:
    def __init__(self, dataset):
        self.operation_size = random.randint(1, Parameter.max_operation)
        self.operations = [OperationSet.get_random_operation() for _ in range(self.operation_size)]
        # Adjust the number of features needed based on the number of operations
        num_features_needed = self.operation_size + 1
        self.features = random.sample(dataset.feature_names, num_features_needed)
        self.equation = self.create_equation()

    def create_equation(self):
        # Start with the first feature
        equation = self.features[0]
        for i in range(self.operation_size):
            operation = self.operations[i][1]  # Get the symbol of the operation
            next_feature = self.features[i + 1]
            
            # Check if we need to add parentheses
            # We add parentheses if the current operation is * or / and the next operation is + or -
            # or if the current operation is + or - and the previous operation was * or /
            if i > 0 and (operation in ['*', '/'] and self.operations[i - 1][1] in ['+', '-']):
                equation = f"({equation})"
            
            if operation in ['+', '-'] and i + 1 < self.operation_size and self.operations[i + 1][1] in ['*', '/']:
                next_feature = f"({next_feature} {self.operations[i + 1][1]} {self.features[i + 2]})"
                i += 1  # Skip the next feature as it's already used in the parentheses
            
            equation += f" {operation} {next_feature}"
        
        return equation