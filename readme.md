# King of the Hill: Colour Run!

The goal is the fill as much as possible of the canvas with your bot's colour. You determine in which direction your bot should move. *Be weary of other bots who might want to paint over your hard work!*

[View the already submitted bots battle online here!](https://heinwessels.github.io/test/)

You will write your bot's logic in a Python class. In each iteration of the game a specific function in your bot will be called (with relevant information as arguments), and your bot will need to decide in which direction to turn.

Here you can see two example bots. Do you have what it takes to out-paint _Rambo the Rando?!_
- [Rambo the Rando](https://github.com/heinwessels/test/blob/master/robots/rambo_the_rando.py)
- [Short Sighted Steve](https://github.com/heinwessels/test/blob/master/robots/short_sighted_steve.py)

## Some Concepts

### The Grid

This is the square canvas on which your bot will paint. It's a 2D grid of integers, where the integer contains the `id` of the bot who's colour is painted there, or `0` if it's unpainted. The size of the grid will be scaled with the amount of bots in on the grid, with the following equation:

``` Python
cells_per_bot = 8 * 8    # The amount of space every bot will have on average
grid_side_length = math.ceil(math.sqrt(cells_per_bot * number_of_bots))
grid = np.zeros(grid_side_length, grid_side_length, dtype=np.int16)
```

### Your Bot

Your bot will move around on the grid (or canvas). Each round you can choose if it will go `UP`, `DOWN`, `LEFT`, `RIGHT` or `STAY` where it is currently. After every move it will attempt to paint the tile beneath it, but if it's successfull depends on its randomly assigned `id` (starting at `1`). The following equation is used:

``` Python
def determine_new_tile_colour(self, floor_colour, bot_colour):
        if floor_colour == 0: return bot_colour # Bot always paints a white floor tile
        return [floor_colour, 0, bot_colour][abs(bot_colour - floor_colour) % 3]
```

The goal of this equation is to allow smarter bots to perform better by possibly seeking the tiles that are easier to paint. 

**Note:** If two robots occupy the same tile then the tile will be painted white, regardless of bot `id`.

As mentioned your bot will be a Python class where you will write the logic the bot will use to decide what to do next. How the bot determines what to do next is up to you. You could train an AI, do weighted path-planning, or simply hunt the highest scoring opponent. As long as it won't fry my laptop trying to run it, it's fine.

Each round your bot will execute the following function that will receive these arguments:

``` Python

# This function is called every round. It contains
#   self
#       id                  Your randomly assigned ID
#       position            Your current position on the grid
#   grid                    A np.array((N, N), dtype=np.int16) containing
#                           the current colours of all the grid tiles. As
#                           mentioned the colours are basically the id
#                           of the bot who painted it. 0 means unpainted, white.
#   enemies[]               A list of all the bots on the grid, including you
#       id                  Id of this enemy (or you)
#       position            Position of this enemy (or you) on the grid
#   game_info               General info about this game
#       current_round       The current round starting at 1
#       number_of_rounds    The current round starting at 1
#       grid_size           Width (or height) of the grid.
def determine_next_move(self, grid, enemies, game_info):
    # Your logic here
    return Move.UP  # This bot will always go up
```
**Note:** Any moves to outside the grid limits will simply be ignored.

## Final Scoring
The final standings will be determined in an epic tournament consisting of 1000 games consisting of a 1000 rounds each where all bots will be placed in a single arena. After each game the total the amount of painted tiles for each bot will be counted, and at the end all the tournament all the game's scores will be added together.

**Note:** The amount of games or rounds might be adjusted depending on the amount of bots submitted, or if it's found that 1000 is not long enough for an accurate representation. If the amount of bots is too large then a Round-Robin-ish implementation might be implemented.

## Submitting

Bots need to be submitted through a Github Pull Request (PR), meaning you need to create a GitHub account. You will create one PR for each bot. This PR will not be merged until the end. Rather, when you let me know you updated your code, then your commits will be `cherry-pick`ed into the `master` branch.

**Note:** You are allowed to submit a maximum of two bots.

**Steps to submit a bot:**
1. Clone the this repository.
2. Create your own fork where this bot will live. E.g. `git checkout -b bob-ross-bot`
3. Create the bot in the folder `robots/`, similar to the example bots.
4. In `game.py` add code to `import` your bot and `add_bot(...)` at the bottom of the list.
5. Commit, add, and push your code back into `origin` to be available online.
6. Create a Pull-Request from your branch into master with your bot name, and a short description of how it works.
7. Your code will then be manually moved into master, leaving your PR open to make future updates or changes.

Your branch might become outdated with `master` as other players contribute their bots. You can easily update your branch with `git fetch` followed by `git merge master --theirs`. This might require you to resolve some conflicts in `game.py`, but they should be trivial to fix. 

## Running the bot on your machine
You can develop and test your bot on your local machine, and should be doable on either Windows or Linux. All you need is the following Python packages on your machine, `pygame` and `numpy`.

You can run the game in two modes by running one of the following two files:
- `main.py`: Regular game with GUI.
- `tournament.py`: (Not yet ready) Run a test tournament without a GUI. After it's done it will print out the rankings. Use `--games 100` or `--rounds 100` to alter the length of the tournament. Defaults to one game of 1000 rounds.

## Rules
- Targetting a specific other bot is not allowed, although you may target the tactics of a general class of bot. 
- May not attempt to alter other bot's internal state.
- Bots may work together but must not communicate with each other and will not know each others IDs. The wins will be awarded individually rather than as a team.
- You may not attempt to alter any internal game variables, for example, but not limited to, the `id`, `position`, the `grid`, etc.
