import random, time, pygame, sys, json
from pygame.locals import *
from Evolution import Evolution
from Environment import Environment, GameEngine
from Agent import Agent

random.seed(12)

def main():
	engine = GameEngine(16, max_cols=4, side_panel_width=150)

	#load the latest generation's best agent
	with open("generations.json") as f:
		gens = json.load(f)
	agents = [Agent(agen['chromosome']) for agen in gens[-1]]
	engine.run_envs(2000, agents)
	print(engine.environments[0].turns)
main()