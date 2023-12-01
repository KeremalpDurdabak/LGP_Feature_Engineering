from modules.Dataset import Dataset
from modules.Parameter import Parameter
from modules.PopulationList import PopulationList
from modules.TeamList import TeamList

def main():
    # Load the dataset
    Dataset.load_dataset('weekr4.2.csv', 'stratified', 400)

    populationList = PopulationList()
    print('Forming Teams...')
    teamList = TeamList(populationList)

    # Proceed with genetic operations
    for generation in range(1, Parameter.generations + 1):
        print(f'Generation: {generation}')
        teamList.evolve(Dataset.X_train.values,Dataset.y_train.values)
        # Display.generationReport()

    # Display.overallReport()

if __name__ == '__main__':
    main()
