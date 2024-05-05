import random, time, pygame, sys, json
from pygame.locals import *
from Evolution import Evolution
from Environment import Environment, GameEngine
from Agent import Agent

random.seed(12)

def main():
	engine = GameEngine(4, max_cols=3, side_panel_width=150)

	#load the latest generation's best agent
	with open("generations.json") as f:
		gens = json.load(f)
	
	agent1 = Agent(gens[-1][0]['chromosome'])
	agent2 = Agent(gens[-2][0]['chromosome'])
	agent3 = Agent(gens[-3][0]['chromosome'])
	agent4= Agent(gens[-4][0]['chromosome'])
	print(f"agent1: {agent1.getChromosome()}")
	print(f"agent2: {agent2.getChromosome()}")
	print(f"agent3: {agent3.getChromosome()}")
	print(f"agent4: {agent3.getChromosome()}")
	engine.run_envs(2000, [agent2, agent1, agent3, agent4])
	print(engine.environments[0].turns)
main()