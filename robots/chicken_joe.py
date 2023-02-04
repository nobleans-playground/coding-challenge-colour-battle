import random

class ChickenJoe:
    @staticmethod
    def get_name(self):
        return "Chicken Joe"

    @staticmethod
    def get_contributor(self):
        return "Hein"

    @staticmethod
    def can_overwrite(id, tile):
        if tile == 0: return True
        return abs(id - tile) % 3 == 2

    @staticmethod
    def determine_next_move(self, grid, enemies, storage, game_info):
        # Check each adjacent tile and see if it can overwrite that
        # tile by moving there. If it finds one, move there. Otherwise
        # do a random movement

        x = self["position"][0]
        y = self["position"][1]
        l = grid.shape[0] # always square
        if y < l - 1 and ChickenJoe.can_overwrite(self['id'], grid[y+1][x]):
            return 'n'
        
        if y > 1 and ChickenJoe.can_overwrite(self['id'], grid[y-1][x]):
            return 's'
        
        if x < l - 1 and ChickenJoe.can_overwrite(self['id'], grid[y][x + 1]):
            return 'e'
        
        if x > 1 and ChickenJoe.can_overwrite(self['id'], grid[y][x - 1]):
            return 'w'

        # Couldn't find somewhere to go. 
        moves = ['n', 'w', 'e', 's', 'h']
        return moves[random.randint(0, len(moves) - 1)]