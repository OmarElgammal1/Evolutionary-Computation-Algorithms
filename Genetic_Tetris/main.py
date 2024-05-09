import random
from pygame.locals import *
from Evolution import Evolution
from Environment import GameEngine

random.seed(42)
def main():
	population_size = 16
	engine = GameEngine(population_size, max_cols=4, side_panel_width=150)
	evol = Evolution(engine, population_size, 0.2)
	evol.evolve(30, 1000)
main()