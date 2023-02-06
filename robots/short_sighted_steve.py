import random
from .bot_control import Move

class ShortSightedSteve:
    def get_name(self):
        return "Short Sighted Steve"

    def get_contributor(self):
        return "Hein"

    def can_overwrite(self, id, tile):
        if tile == 0: return True
        return abs(id - tile) % 3 == 2

    def determine_next_move(self, grid, enemies, game_info):
        # Check each adjacent tile and see if it can overwrite that
        # tile by moving there. If it finds one, maybe move there. Otherwise
        # do a random movement

        x = self.position[0]
        y = self.position[1]
        l = grid.shape[0] # always square
        possible_moves = [ ]

        if y < l - 1 and self.can_overwrite(self.id, grid[y+1][x]):
            possible_moves += [Move.UP]
        
        if y > 0 and self.can_overwrite(self.id, grid[y-1][x]):
            possible_moves += [Move.DOWN]
        
        if x < l - 1 and self.can_overwrite(self.id, grid[y][x + 1]):
            possible_moves += [Move.RIGHT]
        
        if x > 0 and self.can_overwrite(self.id, grid[y][x - 1]):
            possible_moves += [Move.LEFT]

        if x > 0 and self.can_overwrite(self.id, grid[y][x]):
            possible_moves += [Move.STAY]

        # If couldn't find somewhere to go. 
        if len(possible_moves) == 0:
            possible_moves = [move for move in Move]

        # Pick one of the possible moves randomly
        return possible_moves[random.randint(0, len(possible_moves) - 1)]