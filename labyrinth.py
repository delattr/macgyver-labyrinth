"""
MacGyver Labyrinth Game

MacGyver must collect 3 items in order to escape from the Labyrinthe
while avoiding a contact with the gardien.

Game ends if MacGyver collects all items and escapes the labyrinthe
or MacGyver and the guard make a contanct.
"""

import random
import pygame
from pygame.locals import *
from constantes import *
from classes import *

# Initialize pygame
pygame.init()

# Window size
window = pygame.display.set_mode((screen_size, screen_size + sprite_size))

# Window title
pygame.display.set_caption('MacGyver Labyrinthe')

# Load images
fond = pygame.image.load(fond).convert()
fond = pygame.transform.scale(fond, (screen_size, screen_size))
player = pygame.image.load(macgyver).convert_alpha()
player = pygame.transform.scale(player, (sprite_size, sprite_size))

# Set class instances
maze = Maze('n1')
maze.generate()
maze.wall(window)
maze.item()
myplayer = Player(maze)
maze.guard(window)

# Guard kill count
guard_killed = 0
# Ture  condition for wile loop
done = 1

while done:
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        # Close game
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            done = 0
        elif event.type == QUIT:
            done = 0

        # Direction key for Macgyver
        elif event.type == KEYDOWN and event.key == K_UP:
            myplayer.move('up')
        elif event.type == KEYDOWN and event.key == K_DOWN:
            myplayer.move('down')
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            myplayer.move('right')
        elif event.type == KEYDOWN and event.key == K_LEFT:
            myplayer.move('left')

    # Game closes if MacGyver finds exit
    if maze.exit_position == myplayer.player_position and maze.score == 3:
        done = 0
    # Game closes if MacGyver makes a contact with the guard
    if maze.gardien_position == myplayer.player_position and maze.score != 3:
        done = 0

    # new positions to be displayed on screen
    window.blit(fond, (0, 0))
    maze.wall(window)
    maze.displayItems(myplayer, window)
    window.blit(player, myplayer.player_position)

    # Guard disapears if MacGyver make a contact
    if maze.gardien_position == myplayer.player_position:
        guard_killed = 1
    if guard_killed != 1:
        maze.guard(window)
    # refresh screen
    pygame.display.flip()
