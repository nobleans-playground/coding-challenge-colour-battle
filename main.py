import asyncio
import pygame, sys
from pygame.locals import *
from game import Game
 
# Game Setup
FPS = 10
fpsClock = pygame.time.Clock()
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
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    # Main processing
    game.step()
    game.render()
    pygame.display.update()
    await asyncio.sleep(1 / FPS)
 
asyncio.run(main())