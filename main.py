import random, time, pygame, sys
from pygame.locals import *
from Evolution import Evolution

from Environment import Environment, GameEngine
random.seed(42)
def main():

	pygame.display.set_caption('Tetris AI')

	population_size = 12;

	engine = GameEngine(population_size, max_cols=5);
	print(engine.rows)
	evol = Evolution(engine, population_size, 0.01)
	evol.evolve(10, 300)
main()