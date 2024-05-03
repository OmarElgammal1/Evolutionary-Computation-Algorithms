import random, time, pygame, sys
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


	def generateRandomPopulation(self):
		self.population = []
		for i in range(self.populationSize):
			self.population.append(Agent())


	def nextGeneration(self,):
		# sort the population by fitness
		self.population.sort(key = lambda x: x.fitness, reverse = True)
		for i in range(len(self.population)):
			print(f"Agent {i}: {self.population[i].fitness}")
		newPopulation = self.population[:2]
		agent1, agent2 = self.population[0], self.population[1]
		# create the rest of the population
		for i in range(self.populationSize - 2):
			# agent1, agent2 = random.choices(self.population, k = 2)
			# mutation
			newAgent = agent1.crossover(agent2)
			newAgent.mutate(self.mutationRate)
			newPopulation.append(newAgent)
		# set the new population
		self.population = newPopulation


	def evolve(self, numGenerations, maxTurns):
		
		for currGen in range(numGenerations):
			self.engine.reset_envs()
			# assign each agent an environment
			for idx, agent in enumerate(self.population):
				self.engine.environments[idx].agent = agent
			self.engine.side_panel_data = {'gen':f"{currGen}/{numGenerations}", 'mxTurns':maxTurns}
			self.engine.run_envs(maxTurns)

			for env in self.engine.environments:
				env.agent.fitness = env.score
			self.nextGeneration()