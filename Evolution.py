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


	# do your stuff on the population
	#use agent.fitness value to do your suff
	# Main training function. Goes through every step of evolution process.
    # Called every time after population evaluation by interacting with the environment.
	def nextGeneration(self,):
		self.generateRandomPopulation()


	def evolve(self, numGenerations, maxTurns):
		
		for currGen in range(numGenerations):
			self.engine.reset_envs()
			# assign each agent an environment
			for idx, agent in enumerate(self.population):
				self.engine.environments[idx].agent = agent
			self.engine.run_envs(maxTurns)

			for env in self.engine.environments:
				env.agent.fitness = env.score
			self.nextGeneration()