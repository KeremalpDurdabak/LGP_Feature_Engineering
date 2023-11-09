import random
from modules.Parameter import Parameter
from modules.Team import Team


class TeamList:
    def __init__(self, population_list):
        self.population_list = population_list
        self.teams = self.form_teams(population_list)

    def form_teams(self, population_list):
        teams = []
        for _ in range(Parameter.population_count):
            team_individuals = []
            # Iterate over the Population objects which are the values of the dictionary
            for population in population_list.populations.values():
                individual = random.choice(population.individuals)  # Select an individual without replacement
                team_individuals.append(individual)
            teams.append(Team(team_individuals))  # Create a Team object
        return teams

    def calculate_fitness(self, data, labels):
        for team in self.teams:
            team.evaluate_fitness(data, labels)

    def evolve(self, data, labels):
        # Calculate fitness for all teams
        self.calculate_fitness(data, labels)

        # Sort teams by fitness in descending order
        self.teams.sort(key=lambda team: team.fitness, reverse=True)

        # Determine the number of teams to remove
        num_teams_to_remove = int(len(self.teams) * Parameter.gap_percentage)

        # Identify the teams to remove
        teams_to_remove = self.teams[-num_teams_to_remove:]

        # Collect individuals to remove from their respective populations
        individuals_to_remove = {}
        for team in teams_to_remove:
            for individual in team.individuals:
                population_label = team.individual_to_population[individual]
                if population_label not in individuals_to_remove:
                    individuals_to_remove[population_label] = []
                individuals_to_remove[population_label].append(individual)

        # Remove the identified individuals from their populations
        self.population_list.remove_individuals(individuals_to_remove)

        # Generate new children to fill the gap
        self.population_list.generate_children()

        # Re-form teams with the updated populations
        self.teams = self.form_teams(self.population_list)