from modules.Population import Population


class PopulationList:
    def __init__(self, dataset):
        self.populations = []
        self.create_populations(dataset)

    def create_populations(self, dataset):
        # Create a population for each unique target label
        for label in dataset.target_labels:
            # Assume Population class takes a target label and population count as initialization parameters
            population = Population(label, dataset)
            self.populations.append(population)