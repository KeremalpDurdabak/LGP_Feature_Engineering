import numpy as np


class Team:
    def __init__(self, individuals):
        self.individuals = individuals
        self.fitness = 0

    def evaluate_fitness(self, data, actual_labels):
        for instance, actual_label in zip(data, actual_labels):
            # Ensure instance is a 2D array for evaluation
            instance = np.atleast_2d(instance)
            predictions = [individual.evaluate(instance) for individual in self.individuals]
            winning_individual_index = np.argmax(predictions)
            winning_individual = self.individuals[winning_individual_index]
            predicted_label = winning_individual.population_label  # Ensure this attribute is set correctly

            if predicted_label == actual_label:
                self.fitness += 1
