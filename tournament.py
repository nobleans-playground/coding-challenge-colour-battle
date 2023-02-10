import argparse
import numpy as np
from robots.bot_list import BotList
from world import World
import time

parser = argparse.ArgumentParser(description='Nobleo Colour Run')
parser.add_argument('--rounds', type=int, default=1000,
                    help='number of rounds in a single game')
parser.add_argument('--games', type=int, default=1000,
                    help='number of games to play')
args = parser.parse_args()

n_bots = len(BotList)
n_rounds = int(args.rounds)
n_games = int(args.games)
scores = np.zeros((n_bots, n_games))

# Setup the world
world = World()
for bot in BotList:
    world.add_bot(bot)
world.setup(1) # Dry run to get max score
max_score_per_game = world.grid.size

# Run the game
# Print iterations progress
def printProgressBar (iteration, total, prefix='Progress', suffix='', decimals=1, length=40, fill='*', printEnd = "\r"):
    # https://stackoverflow.com/a/34325723
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
time_per_game_len = 30
time_per_game_avg = 0   # Approx. moving average
for game in range(n_games):
    world.setup(n_rounds)
    printProgressBar(game + 1, n_games, suffix = f"| Est. Time left: {round((n_games - game) * time_per_game_avg, 2)} seconds")
    start = time.time()
    while not world.step(): pass
    duration = time.time() - start
    if time_per_game_avg != 0:
        time_per_game_avg += (- time_per_game_avg / time_per_game_len) + (duration / time_per_game_len)
    else:
        time_per_game_avg = duration
    for bot_id, score in world.get_score().items():
        scores[world.colour_map[bot_id] - 1, game] = score

# Calculate the final scores and print 
unsorted_scores = scores.sum(axis=1)
packed_scores = [ ]
for bot_i in range(n_bots):
    packed_scores += [(
        BotList[bot_i]().get_name(),
        BotList[bot_i]().get_contributor(),
        unsorted_scores[bot_i]
    )]
packed_scores.sort(reverse=True, key=lambda e: e[2])
print("============================================================")
print("The Final Scores")
print("============================================================")
for i, score in enumerate(packed_scores):    
    print(f"{i+1:<3}: {score[0]:<30} {score[1]:<20} {round(100*score[2]/n_games/max_score_per_game)} %")