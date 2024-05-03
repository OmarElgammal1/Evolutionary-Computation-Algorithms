import random, math
N_GENES = 7
class Agent():
    def __init__(self, chromosome = None):
        if chromosome == None:
            self.chromosome = []
            for _ in range(N_GENES):
                self.chromosome.append(random.uniform(-1, 1))
        else:
            self.chromosome = chromosome
        self.normalizeChromosome()
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

    def crossover(self, other):
        parent1 = self.getChromosome()
        parent2 = other.getChromosome()
        cutoff = random.randint(0, N_GENES)
        offspring = parent1[:cutoff] + parent2[cutoff:]
        return Agent(offspring)

    def mutate(self, mutationRate):
        if random.random() >= mutationRate: return
        for j in range(N_GENES):
            if random.random() >= mutationRate:
                continue
            self.chromosome[j] += random.uniform(-0.1, 0.1)
            # self.chromosome[j] *= random.uniform(0.99, 1.01)
        self.normalizeChromosome()
    def getChromosome(self):
        return self.chromosome

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def normalizeChromosome(self):
        mod = 0
        for gene in self.chromosome:
            mod += gene * gene
        mod = math.sqrt(mod)
        for i in range(len(self.chromosome)):
            self.chromosome[i] /= mod
        