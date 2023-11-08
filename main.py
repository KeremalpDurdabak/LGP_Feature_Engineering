from modules.Dataset import Dataset
from modules.Parameter import Parameter
from modules.PopulationList import PopulationList


def main():
    dataset = Dataset('weekr4.2.csv')
    popList = PopulationList(dataset)

    for generation in range(1, Parameter.generations + 1):
        popList.generateNextGen()
        #Display.generationReport()

    #Display.overallReport()


if __name__ == '__main__':
    main()