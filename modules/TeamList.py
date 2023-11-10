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
                eligible_individuals = [ind for ind in population.individuals if ind.is_new] if new_individuals_only else population.individuals
                if not eligible_individuals:
                    raise Exception(f"No eligible individuals in population {population.label}")
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

        # Print the fitness scores of all teams for debugging
        #print("Fitness scores:", [team.fitness for team in self.teams])

        # Print the best performing team's fitness and individuals' details
        best_team = self.teams[0]
        print(f"Best Team's Fitness: {best_team.fitness}")
        for individual in best_team.individuals:
            print(f"Population Label: {individual.population_label}, Equation: {individual}")


        # Preserve the best performing teams
        best_teams = self.teams[:int((1 - Parameter.gap_percentage) * len(self.teams))]

        # Determine the number of teams to remove
        num_teams_to_remove = int(len(self.teams) * Parameter.gap_percentage)

        # Remove the worst-performing teams
        self.teams = self.teams[:-num_teams_to_remove]

        # Generate new children to fill the gap
        self.population_list.generate_children()

        # Form new teams with the new children
        new_teams = self.form_teams(num_teams_to_remove, new_individuals_only=True)

        # Calculate fitness for new teams only
        for team in new_teams:
            team.evaluate_fitness(data, labels)

        # Combine best performing teams with new teams
        self.teams = best_teams + new_teams

        # Sort teams again after evaluating new teams
        self.teams.sort(key=lambda team: team.fitness, reverse=True)
