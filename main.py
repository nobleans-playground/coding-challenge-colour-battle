import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)

from world import World
 
# Game Setup
FPS = 5
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

world = World()

from robots.rambo_the_rando import RamboTheRando
world.add_bot(RamboTheRando())
world.add_bot(RamboTheRando())
world.add_bot(RamboTheRando())
world.add_bot(RamboTheRando())
world.create()
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CANVAS = pygame.Surface(WINDOW.get_size(), pygame.SRCALPHA)
CANVAS.set_alpha(200)
pygame.display.set_caption('King of the Hill')
 
# The main function that controls the game
def main () :
  looping = True
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    # Processing
    # This section will be built out later

    world.step()
    
    # Render elements of the game
    WINDOW.fill((255, 255, 255))
    world.draw(CANVAS, WINDOW) 
    WINDOW.blit(CANVAS, (0,0))
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()