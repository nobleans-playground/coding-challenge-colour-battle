import argparse
import numpy as np
import matplotlib.pyplot as plt
from robots.bot_list import BotList
from world import World
import os, time, math, copy, sys
import threading, multiprocessing
import concurrent.futures
from datetime import datetime

# This is the function that will execute a single game
# and capture some information about it. It will terminate
# when the game is done.
# Note: This has to be in global scope
class Context:
    def __init__(self, game):
        self.game = game
        self.n_rounds = n_rounds
        self.bot_list = BotList
        self.progress = progress
        self.scores = [0] * len(BotList)
        self.time_min = [0.0] * len(BotList)
        self.time_avg = [0.0] * len(BotList)
        self.time_max = [0.0] * len(BotList)
        self.should_dump = args.dump
        self.dump_semaphore = dump_semaphore
        self.dump_filename = dump_filename
def game_runner(context : Context) -> Context:
    # We run the game in harsh mode, meaning we don't simply ignore
    # it when your bot crashes or returns an invalid move. Your bot
    # will just sit in the same place. Also includes some checks to 
    # ensure the bots aren't cheating.
    _world = World(harsh=True)
    for bot in context.bot_list:
        _world.add_bot(bot)
    _world.setup(context.n_rounds)
    
    context.progress[context.game] = 0
    
    # Run the game
    while not _world.step(measure_time=True):
        for index, bot in enumerate(_world.bots):
            context.time_min[index] = min(bot.measured_time, context.time_min[index])
            context.time_avg[index] += bot.measured_time / context.n_rounds
            context.time_max[index] = max(bot.measured_time, context.time_max[index])
        
        # Update the value used by the progress printer
        context.progress[context.game] = _world.current_round / context.n_rounds

    # The game is completed. Clean up
    # and capture some information to return
    context.progress.pop(context.game, None)

    max_score = _world.grid.size
    for bot_id, bot_score in _world.get_score().items():
        # Here we calculate the percentage
        context.scores[_world.colour_map[bot_id] - 1] = bot_score / max_score * 100

    if context.should_dump:
        # Dump the results into the csv file
        with context.dump_semaphore:            
            data = np.reshape(np.array(context.scores), (-1, len(BotList)))
            with open(context.dump_filename,'a') as f:
                np.savetxt(f, data, fmt='%3.5f', delimiter=',')

    # Return all results for this game
    return context

# We need this if here otherwise the multiprocessing.Manager() goes hay-wire
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nobleo Colour Run')
    parser.add_argument('--rounds', type=int, default=2000,
                        help='number of rounds in a single game')
    parser.add_argument('--games', type=int, default=200,
                        help='number of games to play')
    parser.add_argument('--threads', type=int, default=8,
                        help='number of games to run simultaniously')
    parser.add_argument('--graph', action='store_true',
                        help='Shows a histogram of the bots performance')
    parser.add_argument('--dump', action='store_true',
                        help='Dumps the results of the tournament in a csv')
    args = parser.parse_args()

    mgr = multiprocessing.Manager()

    n_bots = len(BotList)
    n_rounds = int(args.rounds)
    n_games = int(args.games)
    total_entries = n_rounds * n_games

    # This is all the metrics that we will collect from all the threads
    scores = np.zeros((n_bots, n_games))
    time_min = [0.0] * n_bots
    time_avg = [0.0] * n_bots
    time_max = [0.0] * n_bots

    # Setup writing to the csv dump
    dump_semaphore = mgr.Semaphore()
    now = datetime.now()
    dump_filename = f'dumps/{now.strftime("dump_%Y%m%d_%H%M%S")}.csv'
    if args.dump:
        if not os.path.exists('dumps'):
            os.makedirs('dumps')
        header = np.reshape(np.array([bot_type().get_name() for bot_type in BotList]), (-1, len(BotList)))
        np.savetxt(dump_filename, header, fmt='%s', delimiter=',')

    # This is a thread that will print the progress
    # of all the games currently in progress in
    # other threads. It will automatically terminate
    # once the last game is done
    progress = mgr.dict()
    def progress_printer():
        games_left = {game: True for game in range(n_games)}
        busy = False
        time_started = time.time()
        update_period = 1 # seconds

        total_rounds = n_games * n_rounds
        time_last = time_started
        average_bucket = 20
        average_rounds_per_update = 0
        last_rounds_left = total_rounds
        while busy or len(games_left) != 0:
            print("\033[H\033[J", end="") # Clear console

            progress_ = progress.copy()

            if len(progress_) == 0:
                busy = False
                print("Nothing in progress")
            else:
                busy = True
                for game in progress_.keys():
                    games_left.pop(game, None)

                # How much rounds are still left
                rounds_left = len(games_left) * n_rounds
                for game, completion in progress_.items():
                    rounds_left += math.floor((1-completion) * n_rounds)
                total_completion = (total_rounds-rounds_left)*100/total_rounds

                # Calculate some kind of estimated time left
                time_now = time.time()
                time_delta = time_now - time_last
                time_last = time_now

                rounds_completed = last_rounds_left - rounds_left
                if average_rounds_per_update == 0:
                    average_rounds_per_update = rounds_completed
                else:
                    average_rounds_per_update -= average_rounds_per_update / average_bucket
                    average_rounds_per_update += rounds_completed / average_bucket
                last_rounds_left = rounds_left
                rounds_per_second = round(average_rounds_per_update / time_delta)
                if rounds_per_second >= 1:
                    time_remaining = round(rounds_left / rounds_per_second)
                else:
                    time_remaining = math.inf

                # Print the information
                print(f"{'Game':>5} | Left: {len(games_left)} / {n_games} ({round(total_completion,1)}%) | Speed: {rounds_per_second} rounds/s | Est. Time Left: {time_remaining} seconds")
                for game, completion in progress_.items():
                    bar_length = 40
                    filledLength = math.ceil(completion * bar_length)
                    bar = '*' * filledLength + '-' * (bar_length - filledLength)
                    print(f'{game:>5} |{bar}| {round(completion * 100, 1)}%')
            time.sleep(update_period)
        print("\033[H\033[J", end="") # Clear console
        print(f"Tournament finished in {round(time.time() - time_started)} seconds")
    progress_printer_thread = threading.Thread(target=progress_printer, daemon=True)
    progress_printer_thread.start()

    # Here we will spawn the threads that will run all the games concurrently
    # It's quite cool that Python has something like this built in
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.threads) as executor:
        future_games = {
            executor.submit(game_runner, Context(game)): game 
            for game in range(n_games)
        }
        for future in concurrent.futures.as_completed(future_games):
            context = future.result()
            for index in range(n_bots):
                scores[index, context.game] = context.scores[index]
                time_min[index] = min(context.time_min[index], time_min[index])
                time_avg[index] += context.time_avg[index] / n_games
                time_max[index] = max(context.time_max[index], time_max[index])

    # Wait for progress printer thread to finish
    progress_printer_thread.join()

    print(f"Ran tournament of {n_games} games of {n_rounds} rounds each.")

    # We are done with the tournament. Now display some info
    # Create a dummy world to get bot names and such
    world = World()
    for bot in BotList:
        world.add_bot(bot)
    world.setup(n_rounds)
    total_scores = scores.sum(axis=1) / n_games
    def fmt(time):
        return f"{round(time * 1e6, 3)}"

    # Calculate the final scores and print 
    print("============================================================")
    print("The Final Scores")
    print("============================================================")
    sorted_indexes = list(range(n_bots))
    sorted_indexes.sort(reverse=True, key=lambda i: total_scores[i])
    print(f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score':<7}")
    for rank, i in enumerate(sorted_indexes):
        bot = world.bots[i]
        print(f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[i]):<15}{round(total_scores[i], 3):<7} %")

    print("\n\n")

    print("============================================================")
    print("Best Efficiency")
    print("============================================================")
    sorted_indexes = list(range(n_bots))
    sorted_indexes.sort(reverse=True, key=lambda i: total_scores[i]/time_avg[i])
    print(f"{'Rank':<5}{'Name':<30}{'Contributor':<20}{'Avg [us]':<15}{'Score [%]':<12}{'Efficiency [%/us]':<12}")
    for rank, i in enumerate(sorted_indexes):
        bot = world.bots[i]
        efficiency = total_scores[i] / (time_avg[i] * 1e6)
        print(f"{rank+1:<5}{bot.get_name():<30}{bot.get_contributor():<20}{fmt(time_avg[i]):<15}{round(total_scores[i], 3):<12}{round(efficiency, 3):<12}")

    if args.graph:
        fig = plt.figure()
        fig.set_figheight(8)
        fig.set_figwidth(15)
        for i, bot in enumerate(world.bots):
            y, x = np.histogram(scores[i], bins=math.ceil(scores.max()/2))
            linestyle = "." if i > 16 else "--" if i > 8 else "-"
            plt.plot(x[:-1], y, linestyle=linestyle, label=bot.get_name())
        
        plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
        plt.tight_layout()
        plt.subplots_adjust(left=0.045, bottom=0.08, top=0.95)

        plt.title("Histogram showing scores reached over games")
        plt.ylabel("Quantity")
        plt.xlabel("Score [%]")
        plt.show()
