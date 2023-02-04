import random

class RamboTheRando:
    def get_name(self):
        return "Rambo The Rando"

    def get_contributor(self):
        return "Hein"

    def determine_next_move(self, id, grid, enemies, game_info):
        moves = ['n', 'w', 'e', 's', 'h']
        return moves[random.randint(0, len(moves) - 1)]