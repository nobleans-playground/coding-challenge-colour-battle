import argparse
import numpy as np
from robots.bot_list import BotList
from world import World

parser = argparse.ArgumentParser(description='Nobleo Colour Run')
parser.add_argument('--rounds', type=int, default=1000,
                    help='number of rounds in a single game')
parser.add_argument('--games', type=int, default=100,
                    help='number of games to play')
args = parser.parse_args()

n_bots = len(BotList)
n_rounds = int(args.rounds)
n_games = int(args.games)
scores = np.zeros((n_bots, n_games))

world = World()
for bot in BotList:
    world.add_bot(bot)
world.setup(1) # Dry run to get max score
max_score_per_game = world.grid.size

for game in range(n_games):
    world.setup(n_rounds)
    while not world.step(): pass
    for bot_id, score in world.get_score().items():
        scores[world.colour_map[bot_id] - 1, game] = score


for bot_i in range(n_bots):
    score = scores[bot_i].sum()
    print(f"{BotList[bot_i]().get_name()}: {round(100*score/n_games/max_score_per_game)} %")