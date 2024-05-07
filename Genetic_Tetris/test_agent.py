import random, json
from pygame.locals import *
from Environment import  GameEngine
from Agent import Agent


random.seed(11)
def main():
	engine = GameEngine(2, max_cols=2, side_panel_width=0)
	#load the latest generation's best agent
	with open("generations.json") as f:
		gens = json.load(f)
	agents = [Agent(agen['chromosome']) for agen in gens[-1]]
	# print(len(agents))
	# for i in range(1):
	# 	random.seed(11)
	# 	engine.run_envs(2500, agents)
	# 	for i in range(16):
	# 		engine.environments[i].agent.fitness = engine.environments[i].total_removed_lines + 1500 * engine.environments[i].tetri - 50 * engine.environments[i].calc_initial_move_info(engine.environments[i].board)[0] + engine.environments[i].turns
	# 	engine.environments.sort(key = lambda x: x.agent.fitness, reverse = True)
	# 	for i in range(16):
	# 		print(i, 'th agent:')
	# 		print(f'\tScore:{engine.environments[i].score}')
	# 		print(f'\tTurns:{engine.environments[i].turns}')
	# 		print(f'\tLines:{engine.environments[i].total_removed_lines}')
	# 		print(f'\tFitness:{engine.environments[i].agent.fitness}')
	# 		print(f'\tChromosome:{engine.environments[i].agent.chromosome}')
		
	engine.run_envs(2500, [agents[0], agents[1]])
	# print(engine.environments[0].turns, engine.environments[0].score)
	# print(engine.environments[1].turns, engine.environments[1].score)
	# print(engine.environments[2].turns, engine.environments[2].score)

main()