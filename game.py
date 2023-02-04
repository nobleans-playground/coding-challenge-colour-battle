from world import World
import math
import numpy as np
import pygame

from robots.rambo_the_rando import RamboTheRando
from robots.short_sighted_steve import ShortSightedSteve

# The glue between the World and Pygame
# Includes rendering
class Game:

    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    FONT = (0, 0, 0)

    def __init__(self, window):
        self.world = World()
        self.add_bots()

        self.window = window
        
        # The canvas is where all the colours will be drawn
        self.canvas = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        self.canvas.set_alpha(200)

        # The scoreboard is where all the scores will be printed
        self.scoreboard = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont(None, 24)

    def add_bots(self):
        # This list currently has to be kept updated manually
        self.world.add_bot(RamboTheRando())
        self.world.add_bot(RamboTheRando())
        self.world.add_bot(ShortSightedSteve())
        self.world.add_bot(ShortSightedSteve())

    def setup(self):
        self.world.setup()

    def step(self):
        self.world.step()

    def render(self):
        self.window.fill(self.WHITE)
        grid = self.world.grid

        # Draw the colours
        w = math.floor(min(self.canvas.get_size()) / self.world.grid_length)
        for ix, iy  in np.ndindex(grid.shape):
            colour = self.world.colour_map[grid[iy, ix]] + (100,) 
            pygame.draw.rect(self.canvas, colour, (ix * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - (iy + 1) * w, w, w))
        self.window.blit(self.canvas, (0, 0)) # We blit also so that we can set a custom alpha

        # Draw the bots
        for bot in self.world.bots:
            position = ((bot.position[0]+0.5) * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - ((bot.position[1]+0.5) * w))
            pygame.draw.circle(self.window, self.world.colour_map[bot.id], position, w * 0.4, math.ceil(w/3))
            pygame.draw.circle(self.window, (0, 0, 0), position, w * 0.4, math.ceil(w/10))
            
        # Draw the score board
        self.scoreboard.fill(self.GREY)
        width = self.window.get_size()[0] - self.window.get_size()[1]
        score = self.world.get_score()
        max_score = self.world.grid.size
        border = 10
        spacing = 5    
        line_height = self.font.size("I")[1]
        colour_box_size = math.ceil(line_height * 0.8)
        name_x = border + colour_box_size + spacing
        name_y = border
        score_x = width * 0.8        
        scores = [  [   # Calculate all scores and sort the list
                        bot.get_name(), 
                        round(100*score[bot.id]/max_score),
                        self.world.colour_map[bot.id]
                    ]
                    for bot in self.world.bots]
        scores.sort(reverse=True, key=lambda e: e[1])
        for score in scores:
            # Draw colour square
            pygame.draw.rect(self.scoreboard, score[2], 
                             (border, name_y, colour_box_size, colour_box_size))

            # Draw name
            text = self.font.render(f"{score[0]}", True, self.FONT)
            self.scoreboard.blit(text, (name_x, name_y))

            # Draw score
            text = self.font.render(f"{score[1]} %", True, self.FONT)
            self.scoreboard.blit(text, (score_x, name_y))

            # Update write location
            name_y += line_height + spacing
        self.window.blit(self.scoreboard, (self.window.get_size()[1], 0))