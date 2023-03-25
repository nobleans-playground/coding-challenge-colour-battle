import argparse
import numpy as np
import matplotlib.pyplot as plt
from robots.bot_list import BotList
from world import World
import time, math
import concurrent.futures
import copy

# TODO bot.id is not deterministic between worlds and thus not a suitable key


def run_games(game_nr, bots, n_rounds):
    world = World(harsh=True)
    for bot in bots:
        world.add_bot(bot)
    world.setup(n_rounds)

    running_time = {bot.id: 0 for bot in world.bots}
    start = time.time()
    while not world.step(measure_time=True):
        for bot in world.bots:
            running_time[bot.id] += bot.measured_time
    duration = time.time() - start

    id_to_names = {bot.id: bot.get_name() for bot in world.bots}
    scores = {
        id_to_names[id]: score
        for id, score in world.get_score().items()
    }
    running_time = {id_to_names[id]: time for id, time in running_time.items()}

    return (game_nr, duration, scores, running_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nobleo Colour Run')
    parser.add_argument('--rounds',
                        type=int,
                        default=1000,
                        help='number of rounds in a single game')
    parser.add_argument('--games',
                        type=int,
                        default=50,
                        help='number of games to play')
    parser.add_argument('--graph',
                        action='store_true',
                        help='Shows a histogram of the bots performance')
    args = parser.parse_args()

    n_bots = len(BotList)
    n_rounds = int(args.rounds)
    n_games = int(args.games)

    print(f"Running tournament of {n_games} games of {n_rounds} rounds each.")

    # Setup the world
    world = World(harsh=True)
    for bot in BotList:
        world.add_bot(bot)
    world.setup(1)  # Dry run to get max score
    max_score_per_game = world.grid.size

    scores = {bot.get_name(): [0] * n_games for bot in world.bots}
    time_min = {bot.get_name(): 0.0 for bot in world.bots}
    time_avg = {bot.get_name(): 0.0 for bot in world.bots}
    time_max = {bot.get_name(): 0.0 for bot in world.bots}

    # Run the game
    # Print iterations progress
    def printProgressBar(iteration,
                         total,
                         prefix='Progress',
                         suffix='',
                         decimals=1,
                         length=40,
                         fill='*',
                         printEnd="\r"):
        # https://stackoverflow.com/a/34325723
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    DEBUG_START = time.monotonic()

    executor = concurrent.futures.ProcessPoolExecutor()

    not_done = [
        executor.submit(run_games, i, copy.deepcopy(BotList), n_rounds)
        for i in range(n_games)
    ]
    done = []

    time_per_game_len = 30
    time_per_game_avg = 0  # Approx. moving average

    while len(not_done):
        finished, not_done = concurrent.futures.wait(not_done, timeout=0.1)

        for f in finished:
            if not f.done():
                print("WTF?!!")
            if f.exception() is not None:
                print("EXCEPTION?! {}".format(str(f.exception())))
            game_result = f.result()
            game_nr = game_result[0]
            game_duration = game_result[1]
            game_score = game_result[2]
            game_bot_times = game_result[3]

            if time_per_game_avg != 0:
                time_per_game_avg += (-time_per_game_avg / time_per_game_len
                                      ) + (game_duration / time_per_game_len)
            else:
                time_per_game_avg = game_duration

            for bot_id, score in game_score.items():
                scores[bot_id][game_nr] = score

            for bot_id, running_time in game_bot_times.items():
                time_min[bot_id] = min(running_time, time_min[bot_id])
                time_avg[bot_id] += running_time / (n_games * n_rounds)
                time_max[bot_id] = max(running_time, time_max[bot_id])

        done += finished

        n_done = len(done)

        printProgressBar(
            n_done,
            n_games,
            suffix=
            f"| Est. Time left: {round((n_games - n_done) * time_per_game_avg, 2)} seconds"
        )

    # Post process scores
    for bot, bot_scores in scores.items():
        bot_scores[:] = [
            score * 100 / max_score_per_game for score in bot_scores
        ]
    total_scores = {
        bot: sum(bot_scores) / n_games
        for bot, bot_scores in scores.items()
    }

    def fmt(time):
        return f"{round(time * 1e6, 3)}"

    # Calculate the final scores and print
    print("============================================================")
    print("The Final Scores")
    print("============================================================")
    total_scores = dict(
        sorted(total_scores.items(), reverse=True, key=lambda i: i[1]))
    print(
        f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score':<7}"
    )
    for rank, bot_id in enumerate(total_scores):
        bot = next(filter(lambda b: b.get_name() == bot_id, world.bots))
        print(
            f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[bot_id]):<15}{round(total_scores[bot_id], 3):<7} %"
        )

    print("\n\n")

    print("============================================================")
    print("Best Efficiency")
    print("============================================================")
    sorted_indexes = list(total_scores.keys())
    sorted_indexes.sort(reverse=True,
                        key=lambda i: total_scores[i] / time_avg[i])
    print(
        f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score [%]':<12}{'Efficiency [%/us]':<12}"
    )
    for rank, bot_id in enumerate(sorted_indexes):
        bot = next(filter(lambda b: b.get_name() == bot_id, world.bots))
        efficiency = total_scores[bot_id] / (time_avg[bot_id] * 1e6)
        print(
            f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[bot_id]):<15}{round(total_scores[bot_id], 3):<12}{round(efficiency, 3):<12}"
        )

    DEBUG_DURATION = time.monotonic() - DEBUG_START
    print("Took {} seconds".format(DEBUG_DURATION))

    # if args.graph:
    #     fig = plt.figure()
    #     fig.set_figheight(8)
    #     fig.set_figwidth(15)
    #     for i, bot in enumerate(world.bots):
    #         y, x = np.histogram(scores[i], bins=math.ceil(scores.max() / 2))
    #         linestyle = "." if i > 16 else "--" if i > 8 else "-"
    #         plt.plot(x[:-1], y, linestyle=linestyle, label=bot.get_name())

    #     plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
    #     plt.tight_layout()
    #     plt.subplots_adjust(left=0.045, bottom=0.08, top=0.95)

    #     plt.title("Histogram showing scores reached over games")
    #     plt.ylabel("Quantity")
    #     plt.xlabel("Score [%]")
    #     plt.show()
