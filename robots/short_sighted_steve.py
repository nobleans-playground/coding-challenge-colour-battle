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
        # tile by moving there. If it finds one, move there. Otherwise
        # do a random movement

        x = self.position[0]
        y = self.position[1]
        l = grid.shape[0] # always square
        if y < l - 1 and self.can_overwrite(self.id, grid[y+1][x]):
            return 'n'
        
        if y > 0 and self.can_overwrite(self.id, grid[y-1][x]):
            return 's'
        
        if x < l - 1 and self.can_overwrite(self.id, grid[y][x + 1]):
            return 'e'
        
        if x > 0 and self.can_overwrite(self.id, grid[y][x - 1]):
            return 'w'

        # Couldn't find somewhere to go. 
        moves = ['n', 'w', 'e', 's', 'h']
        return moves[random.randint(0, len(moves) - 1)]