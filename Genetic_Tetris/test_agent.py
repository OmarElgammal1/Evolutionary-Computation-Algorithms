import random, time, pygame, sys, json
from pygame.locals import *
from Evolution import Evolution
from Environment import Environment, GameEngine
from Agent import Agent

random.seed(42)
def main():
	engine = GameEngine(3, max_cols=3, side_panel_width=150)

	#load the latest generation's best agent
	with open("generations.json") as f:
		gens = json.load(f)
	
	engine.environments[0].agent = Agent(gens[-1][0]['chromosome'])

	engine.run_envs(1000, False)
	print(engine.environments[0].turns)
main()