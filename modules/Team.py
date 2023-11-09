import numpy as np

class Team:
    def __init__(self, individuals):
        self.individuals = individuals
        self.fitness = 0

    def evaluate_fitness(self, data, actual_labels):
        # Vectorize the evaluation of all individuals for all instances
        # This creates a 2D array where each row corresponds to an individual's evaluation for all instances
        evaluations = np.array([individual.evaluate(data) for individual in self.individuals])
        
        # Find the index of the best individual for each instance
        winning_indices = np.argmax(evaluations, axis=0)

        # Vectorize the comparison of predicted labels with actual labels
        predicted_labels = np.array([self.individuals[idx].population_label for idx in winning_indices])
        self.fitness = np.sum(predicted_labels == actual_labels)
