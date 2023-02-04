import asyncio
import pygame, sys
from pygame.locals import *
from game import Game
from timeit import default_timer as timer
 
# Game Setup
FPS = 10
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
 
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('King of the Hill')

game = Game(WINDOW)
game.setup()
 
# The main function that controls the game
async def main ():
  looping = True
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    
    # Main processing
    start = timer()
    game.step()
    game.render()
    pygame.display.update()
    end = timer()
    await asyncio.sleep(max(0, 1 / FPS - (end - start)))
 
asyncio.run(main())