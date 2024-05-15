import random
N_GENES = 7
class Agent():
    def __init__(self, chromosome = None):
        self.fitness = 0
        if chromosome == None:
            self.chromosome = []
            for _ in range(N_GENES):
                self.chromosome.append(random.uniform(-1, 1))
        else:
            self.chromosome = chromosome

    def evaluateOptions(self, options):
        bestIndex = 0
        # print(len(options))
        for i in range(len(options)):
            if self.evaluateOption(options[i]) > self.evaluateOption(options[bestIndex]):
                bestIndex = i
        return bestIndex

    def evaluateOption(self, option):
        # print(len(option))
        value = 0
        for i in range(N_GENES):
            value += self.chromosome[i] * option[i]
        return value

    def crossover(self, other):
        parent1 = self.getChromosome()
        parent2 = other.getChromosome()
        cutoff = random.randint(0, N_GENES)
        offspring = parent1[:cutoff] + parent2[cutoff:]
        return Agent(offspring)

    def mutate(self, mutationRate):
        for i in range(N_GENES):
            if random.random() <= mutationRate:
                # self.chromosome[i] += random.uniform(-0.05, 0.05)
                self.chromosome[i] = random.uniform(-1, 1)

    def getChromosome(self):
        return self.chromosome

    def setChromosome(self, chromosome):
        self.chromosome = chromosome