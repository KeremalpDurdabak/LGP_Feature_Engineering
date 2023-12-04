from modules.Dataset import Dataset
from modules.Parameter import Parameter
from modules.PopulationList import PopulationList
from modules.TeamList import TeamList
from modules.Display import Display

def main():
    Dataset.load_dataset('weekr4.2.csv')#, 'stratified', 400)
    populationList = PopulationList()

    print('Forming Teams...')
    teamList = TeamList(populationList)

    best_fitness_scores = []

    for generation in range(1, Parameter.generations + 1):
        print(f'Generation: {generation}')
        teamList.evolve(Dataset.X_train.values, Dataset.y_train.values)
        
        best_team = teamList.teams[0]
        best_fitness_scores.append(best_team.fitness)
        Display.generationReport(best_team)

    Display.overallReport(best_fitness_scores)

    # Write the best fitness scores to a text file
    with open('week_best_fitness_scores.txt', 'w') as file:
        for score in best_fitness_scores:
            file.write(f"{score}\n")

if __name__ == '__main__':
    main()
