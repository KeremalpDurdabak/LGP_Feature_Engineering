import numpy as np
from sklearn.metrics import f1_score

class Team:
    def __init__(self, individuals):
        self.individuals = individuals
        self.fitness = 0
        self.individual_to_population = {ind: ind.population_label for ind in individuals}

    def evaluate_fitness(self, data, actual_labels):
        # Vectorize the evaluation of all individuals for all instances
        # This creates a 2D array where each row corresponds to an individual's evaluation for all instances
        evaluations = np.array([individual.evaluate(data) for individual in self.individuals])

        # Find the index of the best individual for each instance
        winning_indices = np.argmax(evaluations, axis=0)

        # Vectorize the comparison of predicted labels with actual labels
        population_labels = np.array([ind.population_label for ind in self.individuals])
        predicted_labels = population_labels[winning_indices]

        # Calculate the macro F1 score
        self.fitness = f1_score(actual_labels, predicted_labels, average='macro')

    # ... (any other existing methods you may have)
