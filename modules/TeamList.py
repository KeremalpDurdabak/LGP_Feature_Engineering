# TeamList.py

import random
from modules.Parameter import Parameter
from modules.Team import Team

class TeamList:
    def __init__(self, population_list):
        self.population_list = population_list
        self.teams = self.form_teams(Parameter.population_count)

    def form_teams(self, num_teams, new_individuals_only=False):
        teams = []
        for _ in range(num_teams):
            team_individuals = []
            for population in self.population_list.populations.values():
                if new_individuals_only:
                    eligible_individuals = [ind for ind in population.individuals if ind.is_new]
                else:
                    eligible_individuals = population.individuals
                individual = random.choice(eligible_individuals)
                team_individuals.append(individual)
            teams.append(Team(team_individuals))
        return teams

    def evolve(self, data, labels):
        # Calculate fitness for all teams
        for team in self.teams:
            team.evaluate_fitness(data, labels)

        # Sort teams by fitness in descending order
        self.teams.sort(key=lambda team: team.fitness, reverse=True)

        # Determine the number of teams to remove
        num_teams_to_remove = int(len(self.teams) * Parameter.gap_percentage)

        # Remove the worst-performing teams
        self.teams = self.teams[:-num_teams_to_remove]

        # Generate new children to fill the gap
        self.population_list.generate_children()

        # Form new teams with the new children
        new_teams = self.form_teams(num_teams_to_remove, new_individuals_only=True)

        # Add the new teams to the team list
        self.teams.extend(new_teams)

        # Calculate fitness for new teams only
        for team in new_teams:
            team.evaluate_fitness(data, labels)

        # Sort teams again after evaluating new teams
        self.teams.sort(key=lambda team: team.fitness, reverse=True)