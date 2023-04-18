import numpy as np
import matplotlib.pyplot as plt
import scipy
import math

# Thanks Lewie for running the simulation!
filename = "dumps/dump_20230417_153744.csv"

# Read headers
bot_names = None
with open(filename) as f:
    name_line = f.readline()
    bot_names = name_line.strip().split(",")
n_bots = len(bot_names)

# Read the data, ignoring the first row where the names are
scores = np.genfromtxt(filename, delimiter=',')[1:,:]
assert(n_bots == scores.shape[1])
n_games = scores.shape[0]
average_scores = np.average(scores, axis=0)
print(f"Found {n_games} games played by {n_bots} bots")

print("============================================================")
print("The Final Scores")
print("============================================================")
sorted_indexes = list(range(n_bots))
sorted_indexes.sort(reverse=True, key=lambda i: average_scores[i])
print(f"{'Rank':<5}{'Name':<30}{'Score':<7}")
for rank, i in enumerate(sorted_indexes):
    print(f"{rank+1:<5}{bot_names[i]:<30}{round(average_scores[i], 3):<7} %")

print("============================================================")
print("Standard deviation")
print("============================================================")
deviation = scores.std(axis=0) # Lower is better
sorted_indexes = list(range(n_bots))
sorted_indexes.sort(reverse=False, key=lambda i: deviation[i])
print(f"{'Rank':<5}{'Name':<30}{'Std (σ)':<7}")
for rank, i in enumerate(sorted_indexes):
    print(f"{rank+1:<5}{bot_names[i]:<30}{round(deviation[i], 5):<7} %")

print("============================================================")
print("Highest Single Point")
print("============================================================")
highscore = scores.max(axis=0) # Lower is better
sorted_indexes = list(range(n_bots))
sorted_indexes.sort(reverse=True, key=lambda i: highscore[i])
print(f"{'Rank':<5}{'Name':<30}{'Score':<7}")
for rank, i in enumerate(sorted_indexes):
    print(f"{rank+1:<5}{bot_names[i]:<30}{round(highscore[i], 5):<7} %")





fig = plt.figure()
fig.set_figheight(8)
fig.set_figwidth(15)
for i in range(n_bots):
    # if i != 12: continue

    y, x = np.histogram(scores[:,i], bins=math.ceil(scores.max()))
    x = [x[i] + (x[i+1]-x[i])/2 for i in range(len(x) - 1)]
    linestyle = "dotted" if i > 16 else "--" if i > 8 else "-"

    plt.plot(x, y, linestyle=linestyle, label=bot_names[i])


plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
plt.tight_layout()
plt.subplots_adjust(left=0.045, bottom=0.08, top=0.95)
plt.grid()
plt.title("Histogram showing scores reached over games")
plt.ylabel("Quantity")
plt.xlabel("Score [%]")
plt.xlim(0, 15)
plt.ylim(0, 10000)
plt.show()