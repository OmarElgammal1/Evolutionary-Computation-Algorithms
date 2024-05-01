import random, time, pygame, sys
from pygame.locals import *
from Evolution import Evolution

from Environment import Environment, GameEngine
random.seed(42)
def main():

	pygame.display.set_caption('Tetris AI')

	rows = 3	
	cols = 3

	engine = GameEngine(rows, cols);
	evol = Evolution(engine, rows * cols, 0.01)
	evol.evolve(10, 300)
main()