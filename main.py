import asyncio
import pygame, sys
from pygame.locals import *
from game import Game
import argparse

parser = argparse.ArgumentParser(description='Nobleo Colour Run')
parser.add_argument('--rounds', type=int, default=1000,
                    help='number of rounds in a single game')
parser.add_argument('--auto-restart', type=int, default=None,
                    help='Auto restart the game after so many seconds')
parser.add_argument('--width', type=int, default=1150,
                    help='width of the window')
parser.add_argument('--height', type=int, default=700,
                    help='height of the window')
args = parser.parse_args()


# Setup
auto_restart = int(args.auto_restart) if args.auto_restart is not None else None
nr_rounds = int(args.rounds)
WINDOW_WIDTH = int(args.width)
WINDOW_HEIGHT = int(args.height)
 
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Nobleo Colour Battle!')

game = Game(WINDOW, nr_rounds, auto_restart)
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
    
    await asyncio.sleep(game.process())
 
asyncio.run(main())