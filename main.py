from modules.Dataset import Dataset
from modules.Parameter import Parameter
from modules.PopulationList import PopulationList
from modules.TeamList import TeamList

def main():
    # Load the dataset
    Dataset.load_dataset('weekr4.2.csv')#, 'stratified', 200)

    populationList = PopulationList()
    teams = TeamList(populationList)
    print('1')

    # Proceed with genetic operations
    for generation in range(1, Parameter.generations + 1):
        teams.evolve(Dataset.X_train.values,Dataset.y_train.values)
        print('1')
        # Display.generationReport()

    # Display.overallReport()

if __name__ == '__main__':
    main()
