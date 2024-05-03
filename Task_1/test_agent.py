import random, time, pygame, sys, json
from pygame.locals import *
from Evolution import Evolution
from Environment import Environment, GameEngine
from Agent import Agent

random.seed(42)
def main():
	engine = GameEngine(1, max_cols=1, side_panel_width=150)

	#load the latest generation's best agent
	with open("generations.json") as f:
		gens = json.load(f)
	
	engine.environments[0].agent = Agent(gens[-1][0]['chromosome'])

	engine.run_envs(1000)
	print(engine.environments[0].turns)
main()