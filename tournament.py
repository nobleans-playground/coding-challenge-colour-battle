import argparse
import numpy as np
from robots.bot_list import BotList
from world import World
import time

parser = argparse.ArgumentParser(description='Nobleo Colour Run')
parser.add_argument('--rounds', type=int, default=1000,
                    help='number of rounds in a single game')
parser.add_argument('--games', type=int, default=1,
                    help='number of games to play')
args = parser.parse_args()

n_bots = len(BotList)
n_rounds = int(args.rounds)
n_games = int(args.games)
scores = np.zeros((n_bots, n_games))

total_entries = n_rounds * n_games
time_min = [0.0] * n_bots
time_avg = [0.0] * n_bots
time_max = [0.0] * n_bots

print(f"Running tournament of {n_games} games of {n_rounds} rounds each.")

# Setup the world
world = World(harsh=True)
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
    while not world.step(measure_time=True):
        for index, bot in enumerate(world.bots):
            time_min[index] = min(bot.measured_time, time_min[index])
            time_avg[index] += bot.measured_time / total_entries
            time_max[index] = max(bot.measured_time, time_max[index])
    duration = time.time() - start
    if time_per_game_avg != 0:
        time_per_game_avg += (- time_per_game_avg / time_per_game_len) + (duration / time_per_game_len)
    else:
        time_per_game_avg = duration
    for bot_id, score in world.get_score().items():
        scores[world.colour_map[bot_id] - 1, game] = score

def fmt(time):
    return f"{round(time * 1e6, 3)}"

# Calculate the final scores and print 
print("============================================================")
print("The Final Scores")
print("============================================================")
final_scores = scores.sum(axis=1)
sorted_indexes = list(range(n_bots))
sorted_indexes.sort(reverse=True, key=lambda i: final_scores[i])
print(f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score':<7}")
for rank, i in enumerate(sorted_indexes):
    bot = world.bots[i]
    print(f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[i]):<15}{round(100*final_scores[i]/n_games/max_score_per_game, 3):<7} %")

print("\n\n")

print("============================================================")
print("Best Efficiency")
print("============================================================")
final_scores = scores.sum(axis=1)
sorted_indexes = list(range(n_bots))
sorted_indexes.sort(reverse=True, key=lambda i: final_scores[i]/time_avg[i])
print(f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score [%]':<12}{'Efficiency [%/us]':<12}")
for rank, i in enumerate(sorted_indexes):
    bot = world.bots[i]
    score = 100*final_scores[i]/n_games/max_score_per_game
    efficiency = score / (time_avg[i] * 1e6)
    print(f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[i]):<15}{round(score, 3):<12}{round(efficiency, 3):<12}")
