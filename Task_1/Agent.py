import random
N_GENES = 4
class Agent():
    def __init__(self, chromosome = None):
        if chromosome == None:
            self.chromosome = []
            for _ in range(N_GENES):
                self.chromosome.append(random.uniform(-1, 1))
        else:
            self.chromosome = chromosome

    def evaluateOptions(self, options):
        bestIndex = 0
        for i in range(len(options)):
            if self.evaluateOption(options[i]) > self.evaluateOption(options[bestIndex]):
                bestIndex = i
        return bestIndex

    def evaluateOption(self, option):
        value = 0
        for i in range(N_GENES):
            value += self.chromosome[i] * option[i]
        return value

    # GENERATES 7 OTHER AGENTS WITH MUTATED VALUES TO ITSELF AND RETURNS THEM
    def mutate(self):
        mutatedChromosome = []
        for j in range(N_GENES):
            mutatedChromosome.append(self.chromosome[j] + random.uniform(-0.05, 0.05))
        return mutatedChromosome

    def getChromosome(self):
        return self.chromosome

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def normalization(self):
        print("Normalizing chromosome")