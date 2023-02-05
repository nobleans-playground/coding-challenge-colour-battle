import asyncio
import pygame, sys
from pygame.locals import *
from game import Game
 
# Setup
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 900
 
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Nobleo Colour Battle!')

game = Game(WINDOW)
game.setup() 
 
# The main function that controls the game
async def main ():
  looping = True
  
  # The main game loop
  while looping : 
    # Get inputs
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        game.handle_click(pygame.mouse.get_pos())
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    
    # game.process determines how long to sleep
    await asyncio.sleep(game.process())
 
asyncio.run(main())