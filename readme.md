# King of the Hill: Colour Run!

The goal is the fill as much as possible of the canvas with your bot's colour. You determine in which direction your bot should move. *Be weary of other bots who might want to paint over your hard work!*

[View the already submitted bots battle online here!](https://heinwessels.github.io/test/)

You will write your bot's logic in a Python class. In each iteration of the game a specific function in your bot will be called (with relevant information as arguments), and your bot will need to decide in which direction to turn.

Here you can see two examples of two existing bots:
- [Rambo the Rando](https://github.com/heinwessels/test/blob/master/robots/rambo_the_rando.py)
- [Short Sighted Steve](https://github.com/heinwessels/test/blob/master/robots/short_sighted_steve.py)

## Some Concepts

### The Grid

This is the canvas on which your bot will paint. It's a 2D grid of integers, where the integer contains the `ID` of the bot who's colour is painted there, or `0` if it's unpainted. The size of the grid will be scaled with the amount of bots in on the grid, with the following equation:
``` Python
cells_per_bot = 8 * 8    # The amount of space every bot will have on average
grid_side_length = math.ceil(math.sqrt(cells_per_bot * number_of_bots))
grid = np.zeros(grid_side_length, grid_side_length, dtype=np.int8)
```

### Your Bot

As mentioned your bot will be a Python class. It will be assigned a random `ID`, which will relate to the colour it can paint, and determine which other colours it can overwrite or erase.

**Important**: How you determine what the bot should do is up to you. You could train an AI, do complex path planning, or simply hunt the highest scoring opponent.

``` Python
grid = np.array((N, N), dtype=np.int8)

game_info = {
    "step": 5,                  # Starts at 0
    "number_of_steps": 1000,    # amount of steps this round
    "grid_size" = (20, 20),     # Size of grid (always square)
}
```

## Rules:
- Targetting a specific other bot is not allowed (you may target the tactics of a general class of bot. 
- May not attempt to alter other bot's internal state.
- Bots may work together but must not communicate with each other and will not know each others IDs. The wins will be awarded individually rather than as a team.