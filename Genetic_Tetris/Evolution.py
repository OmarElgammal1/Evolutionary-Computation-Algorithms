import random, json
from pygame.locals import *
from Agent import Agent
from Environment import Environment, GameEngine
class Evolution:
	def __init__(self, gameEngine, populationSize, mutationRate) -> None:
		self.engine : GameEngine = gameEngine
		self.populationSize = populationSize
		self.mutationRate = mutationRate
		self.population = []
		self.generateRandomPopulation()
		self.generation_logs = []

	def generateRandomPopulation(self):
		self.population = []
		for i in range(self.populationSize):
			self.population.append(Agent())


	def nextGeneration(self,):
		# sort the population by fitness
		self.population.sort(key = lambda x: x.fitness, reverse = True)
		newPopulation = []
		agent1, agent2 = self.population[0], self.population[1]
		# create the rest of the population
		for i in range(self.populationSize):
			# agent1, agent2 = random.choices(self.population, k = 2)
			# mutation
			newAgent = agent1.crossover(agent2)
			newAgent.mutate(self.mutationRate)
			newPopulation.append(newAgent)
		# set the new population
		self.population = newPopulation


	def evolve(self, numGenerations, maxTurns):
		
		for currGen in range(numGenerations):
			for idx, agent in enumerate(self.population):
				print(f"agent {idx} : {agent.chromosome}")
			self.engine.side_panel_data = {'gen':f"{currGen}/{numGenerations}", 'mxTurns':maxTurns}
			self.engine.run_envs(maxTurns, self.population, True)

			for env in self.engine.environments:
				env.agent.fitness = env.total_removed_lines + 1500 * env.tetri - 50 * env.calc_initial_move_info(env.board)[0]
			self.generation_logs.append(
				sorted(
					[{'chromosome': agent.chromosome, 'fitness': agent.fitness}
	  					for agent in self.population], key=lambda x: x['fitness'], reverse=True))
			self.save_generation_log()
			self.nextGeneration()

	def save_generation_log(self):
		with open("generations.json", 'w') as file:
			json.dump(self.generation_logs, file, indent=4)


