from modules.Population import Population  # Assuming this will be implemented later
from modules.Dataset import Dataset

class PopulationList:
    def __init__(self):
        # Create a dictionary to hold populations, each keyed by its target label
        self.populations = {label: Population(label) for label in Dataset.target_labels}

    def remove_individuals(self, teams_to_remove):
        # Flatten the list of individuals to remove from each team
        individuals_to_remove = [ind for team in teams_to_remove for ind in team.individuals]

        # Remove these individuals from their respective populations
        for population in self.populations.values():
            population.remove_individuals(individuals_to_remove)

    def generate_children(self):
        # For each population, generate children to fill the gap left by removed individuals
        for population in self.populations.values():
            population.generate_children()

    # ... (any other existing methods you may have)
