import random

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
            possible_moves += ['n']
        
        if y > 0 and self.can_overwrite(self.id, grid[y-1][x]):
            possible_moves += ['s']
        
        if x < l - 1 and self.can_overwrite(self.id, grid[y][x + 1]):
            possible_moves += ['e']
        
        if x > 0 and self.can_overwrite(self.id, grid[y][x - 1]):
            possible_moves += ['w']

        if x > 0 and self.can_overwrite(self.id, grid[y][x]):
            possible_moves += ['h']

        # If couldn't find somewhere to go. 
        if len(possible_moves) == 0:
            possible_moves = ['n', 'w', 'e', 's', 'h']

        # Pick one of the possible moves randomly
        return possible_moves[random.randint(0, len(possible_moves) - 1)]