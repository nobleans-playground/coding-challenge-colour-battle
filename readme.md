[View online](https://heinwessels.github.io/test/)


## Data passed to your function
``` Python

grid = np.array((N, N), dtype=np.int8)

game_info = {
    "step": 5,                  # Starts at 0
    "number_of_steps": 1000,    # amount of steps this round
    "grid_size" = (20, 20),     # Size of grid (always square)
}
```

## Rules:
- Deterministic (random is allowed)
- May not attempt to alter other bot's internal storage