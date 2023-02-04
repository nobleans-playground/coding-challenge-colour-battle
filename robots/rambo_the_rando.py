import random
import numpy as np


class RamboTheRando:

    def __init__(self):
        self.target = None

    def get_name(self):
        return "Rambo The Rando"

    def get_contributor(self):
        return "Hein"

    def determine_next_move(self, grid, enemies, game_info):
        # Chooses a random target location, and moves there.
        # Once it's there, choose a new location.
        
        # Create a target in storage if doesn't exist
        if  self.target is None:
            self.target = np.zeros_like(self.position)

        # If reached the target find a new target
        if np.array_equal(self.position, self.target):
            self.target[0] = random.randint(0, grid.shape[0] - 1)
            self.target[1] = random.randint(0, grid.shape[1] - 1)
        
        # Move in direction of target
        if self.target[0] > self.position[0]:
            return "e"
        elif self.target[0] < self.position[0]:
            return "w"
        elif self.target[1] > self.position[1]:
            return "n"
        else:
            return "s"