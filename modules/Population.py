# Assuming Individual.py is in the same directory as Population.py
from modules.Individual import Individual
from modules.Parameter import Parameter

class Population:
    def __init__(self, label, dataset):
        self.label = label
        self.dataset  = dataset
        self.individuals = [Individual(dataset) for _ in range(Parameter.population_count)]
        print('1')