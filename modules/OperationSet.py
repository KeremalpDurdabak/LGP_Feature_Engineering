import operator
import random

class OperationSet:
    operations = {
        'add': (operator.add, '+'),
        'subtract': (operator.sub, '-'),
        'multiply': (operator.mul, '*'),
        'divide': (lambda x, y: x / y if y != 0 else 1, '/')
    }

    @staticmethod
    def add_operation(name, function, symbol):
        OperationSet.operations[name] = (function, symbol)

    @staticmethod
    def remove_operation(name):
        if name in OperationSet.operations:
            del OperationSet.operations[name]

    @staticmethod
    def get_random_operation():
        return random.choice(list(OperationSet.operations.values()))

    @staticmethod
    def execute(operation, *args):
        try:
            return operation[0](*args)
        except Exception as e:
            raise ValueError(f"Error executing operation with args {args}: {e}")

    @staticmethod
    def get_operation_symbol(operation):
        for name, (func, symbol) in OperationSet.operations.items():
            if func == operation[0]:
                return symbol
        raise ValueError("Operation not found")
