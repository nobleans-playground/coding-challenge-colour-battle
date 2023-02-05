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
    BLACK = (0, 0, 0)

    # 20 (actually 18, because black/white was removed) colours 
    # From: https://sashamaps.net/docs/resources/20-colors/
    COLOURS = [
        (230, 25, 75),
        (60, 180, 75),
        (255, 225, 25),
        (0, 130, 200),
        (245, 130, 48),
        (145, 30, 180),
        (70, 240, 240),
        (240, 50, 230),
        (210, 245, 60),
        (250, 190, 212),
        (0, 128, 128),
        (220, 190, 255),
        (170, 110, 40),
        (255, 250, 200),
        (128, 0, 0),
        (170, 255, 195),
        (128, 128, 0),
        (255, 215, 180),
        (0, 0, 128),
        (128, 128, 128),
    ]

    def __init__(self, window):
        self.world = World()
        self.add_bots()
        self.draw_bot_ids = False

        self.window = window
        
        # The canvas is where all the colours will be drawn
        self.canvas = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        self.canvas.set_alpha(100)

        # The scoreboard is where all the scores will be printed
        self.scoreboard = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont(None, 24)

    def add_bots(self):
        # This list currently has to be kept updated manually
        self.world.add_bot(RamboTheRando())
        self.world.add_bot(ShortSightedSteve())

    def setup(self):
        self.world.setup()
        self.cell_w = math.floor(min(self.canvas.get_size()) / self.world.grid_length)
        self.canvas_font = pygame.font.SysFont(None, math.ceil(self.cell_w * 0.8))

    def step(self):
        self.world.step()

    def colour_from_id(self, id):
        if id == 0: return self.WHITE
        return self.COLOURS[self.world.colour_map[id] % len(self.COLOURS)]

    def render(self):
        self.window.fill(self.WHITE)
        grid = self.world.grid
        w = self.cell_w

        # Draw the colours
        for ix, iy  in np.ndindex(grid.shape):
            colour_id = grid[iy, ix]
            colour = self.colour_from_id(colour_id)
            position = (ix * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - (iy + 1) * w
                        )
            pygame.draw.rect(self.canvas, colour, (*position, w, w))

            if self.draw_bot_ids:
                text_to_render = f"{colour_id}"
                text = self.canvas_font.render(text_to_render, True, self.BLACK + (50,))
                text_size = self.canvas_font.size(text_to_render)
                self.canvas.blit(text, (position[0] + w/2 - text_size[0]/2, position[1] + w/2 - text_size[1]/2))
        self.window.blit(self.canvas, (0, 0)) # We blit also so that we can set a custom alpha

        # Draw the bots
        for bot in self.world.bots:
            position = ((bot.position[0]+0.5) * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - ((bot.position[1]+0.5) * w))
            pygame.draw.circle(self.window, self.colour_from_id(bot.id), position, w * 0.4, math.ceil(w/3))
            pygame.draw.circle(self.window, (0, 0, 0), position, w * 0.4, math.ceil(w/10))
            
        # Draw the score board
        self.scoreboard.fill(self.GREY)
        width = self.window.get_size()[0] - self.window.get_size()[1]
        border = 10
        spacing = 5    
        line_height = self.font.size("I")[1]
        colour_box_size = math.ceil(line_height * 0.95)
        name_x = border + colour_box_size + spacing
        name_y = border
        score_x = width * 0.8        
        
        scores = self.world.get_score()
        max_score = self.world.grid.size
        sorted_scores = [  [   # Calculate all scores and sort the list
                        bot.get_name(), 
                        round(100*scores[bot.id]/max_score),
                        bot.id,
                    ]
                    for bot in self.world.bots]
        sorted_scores.sort(reverse=True, key=lambda e: e[1])

        for score in sorted_scores:
            bot_name, bot_score, bot_id = score
            # Draw colour square
            pygame.draw.rect(self.scoreboard, self.colour_from_id(colour_id), 
                             (border, name_y, colour_box_size, colour_box_size))
            
            # Draw number over the square
            if self.draw_bot_ids:
                font = pygame.font.SysFont(None, colour_box_size)
                text_to_render = f"{bot_id}"
                text = font.render(text_to_render, True, self.BLACK + (50,))
                text_size = font.size(text_to_render)
                self.scoreboard.blit(text, (
                    border + colour_box_size/2 - text_size[0]/2, 
                    name_y + colour_box_size/2 - text_size[1]/2
                    ))

            # Draw name
            text = self.font.render(f"{bot_name}", True, self.BLACK)
            self.scoreboard.blit(text, (name_x, name_y))

            # Draw score
            text = self.font.render(f"{bot_score} %", True, self.BLACK)
            self.scoreboard.blit(text, (score_x, name_y))

            # Update write location
            name_y += line_height + spacing
        self.window.blit(self.scoreboard, (self.window.get_size()[1], 0))