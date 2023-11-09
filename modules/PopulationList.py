from modules.Population import Population  # Assuming this will be implemented later
from modules.Dataset import Dataset

class PopulationList:
    def __init__(self):
        # Create a dictionary to hold populations, each keyed by its target label
        self.populations = {label: Population(label) for label in Dataset.target_labels}

