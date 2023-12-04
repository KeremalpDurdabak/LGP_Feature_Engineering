import matplotlib.pyplot as plt

class Display:
    @staticmethod
    def generationReport(team):
        print(f"Highest Fitness Team: {team.fitness}")
        for individual in team.individuals:
            # Assuming individual.population_label indicates the target label the individual is predicting
            print(f"Prediction for class '{individual.population_label}': {individual}")


    @staticmethod
    def overallReport(fitness_over_generations):
        plt.plot(fitness_over_generations)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness Score')
        plt.title('Fitness Score Over Generations')
        plt.savefig('fitness_over_generations.png')
        plt.show()
