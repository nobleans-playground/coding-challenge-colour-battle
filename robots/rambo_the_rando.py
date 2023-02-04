import random
import numpy as np


class RamboTheRando:
    @staticmethod
    def get_name(self):
        return "Rambo The Rando"

    @staticmethod
    def get_contributor(self):
        return "Hein"

    @staticmethod
    def determine_next_move(self, grid, enemies, storage, game_info):
        # Chooses a random target location, and moves there.
        # Once it's there, choose a new location.
        
        # Create a target in storage if doesn't exist
        if not "target" in storage:
            storage["target"] = np.zeros_like(self["position"])

        # If reached the target find a new target
        if np.array_equal(self["position"], storage["target"]):
            storage["target"][0] = random.randint(0, grid.shape[0] - 1)
            storage["target"][1] = random.randint(0, grid.shape[1] - 1)
        
        # Move in direction of target
        if storage["target"][0] > self["position"][0]:
            return "e"
        elif storage["target"][0] < self["position"][0]:
            return "w"
        elif storage["target"][1] > self["position"][1]:
            return "n"
        else:
            return "s"