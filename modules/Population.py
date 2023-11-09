from modules.Individual import Individual
from modules.Parameter import Parameter

class Population:
    def __init__(self, label):
        # Initialize individuals with the population label
        self.individuals = [Individual(label) for _ in range(Parameter.population_count)]


# Assuming the Individual class is defined elsewhere and handles its own initialization
