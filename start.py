"""
MacGyver Labyrinth Game

MacGyver must collect 3 items in order to escape from the Labyrinthe
while avoiding a contact with the gardien.

Game ends if MacGyver collects all items and escapes the labyrinthe
or MacGyver and the guard make a contanct.
"""

import pygame, sys
from pygame.locals import *
from constants import *
from classes import *
from maze import generate_maze


# Initialize pygame
pygame.init()
pygame.font.init()
# Window size
window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + SPRITE_SIZE))
# Window title
pygame.display.set_caption('MacGyver Labyrinthe')

# Load images
fond = pygame.image.load(FOND).convert()
macgyver = pygame.image.load(MACGYVER).convert_alpha()
macgyver = pygame.transform.scale(macgyver, (SPRITE_SIZE, SPRITE_SIZE))
medoc = pygame.image.load(GARDIEN).convert_alpha()
medoc = pygame.transform.scale(medoc, (SPRITE_SIZE, SPRITE_SIZE))
block = pygame.image.load(MUR).convert()
sirynge = pygame.image.load(SIRYNGE).convert()
win = pygame.image.load(WIN).convert()
loose = pygame.image.load(LOOSE).convert()
welcome = pygame.image.load(WELCOME).convert()

# Load music
pygame.mixer.init()
pygame.mixer.music.load(MUSIC)
#play music
pygame.mixer.music.play(loops=-1)

# Welcome screen
while 1:
    initiate = 0
    window.blit(welcome, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 'easy'
                initiate = 1
            elif event.key == pygame.K_2:
                mode = 'hard'
                initiate = 1
        if event.type == pygame.QUIT:
            sys.exit()

    # Initiate the maze
    while initiate:
        # auto-generate Maze
        structure = generate_maze()
        maze = Maze(structure)
        # Create Wall
        maze.blit_walls(window)
        # Create MacGyver
        myplayer = Player(maze)
        # Create Medoc
        guard = Guard(maze)
        guard.set_guard_position()
        # Randomly position items in the maze
        item = Item(maze)
        item.set_item_positions()
        # Guard kill count
        guard_killed = 0
        # Ture  condition for wile loop
        done = 1
        direction = None
        count = 0
        while done:
            count += 1
            x = myplayer.player_position[0]
            y = myplayer.player_position[1]
            # pygame.time.Clock().tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                # Direction key for Macgyver
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction ='up'
                    elif event.key == pygame.K_DOWN:
                        direction = 'down'
                    elif event.key == pygame.K_RIGHT:
                       direction ='right'
                    elif event.key == pygame.K_LEFT:
                        direction ='left'
                    elif event.key == pygame.K_ESCAPE:
                        # Display welcome screen
                        initiate = 0
                        done = 0
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or
                        event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                        direction = None
            # Set Player.player_postion
            myplayer.move(direction)
            # Varying the frequency of updating guard position to controll the game difficulty
            if mode == 'easy':
                if not count % 3:
                    guard.set_guard_position()
                    count = 0
            elif mode == 'hard':
                if count % 2:
                    guard.set_guard_position()
                    count = 0
            # New positions to be displayed on screen
            window.blit(fond, (0, 0))
            maze.blit_walls(window)
            item.display_items(myplayer.player_position, window)
            window.blit(macgyver, myplayer.player_position)
            # Hide Medoc if he's not been contacted by MacGyver
            if not guard_killed:
                window.blit(medoc, guard.guard_position)
            # If guard is killed and player obtains all items
                if item.score == 3:
                    window.blit(sirynge, myplayer.player_position)

            pygame.display.flip()


            # Gaurd contacted by Player
            if guard.guard_position == myplayer.player_position:
                # Player losses the game
                if item.score != 3:
                    end = 1
                    while end:
                        for event in pygame.event.get():
                            window.blit(loose,(0,0))
                            pygame.display.flip()
                            if event.type == KEYDOWN:
                                if event.key == K_RETURN:
                                    end = 0
                                elif event.key == K_ESCAPE:
                                    initiate = 0
                                    end = 0
                            if event.type == QUIT:
                                sys.exit()
                    done = 0
                # Player kills the guard
                elif item.score == 3:
                    guard_killed = 1
                    # Open exit route
                    maze.structure[13][14] = 'e'

            # Conditions for wining the game
            if maze.exit_position == myplayer.player_position and item.score == 3:
                end = 1
                while end:
                    for event in pygame.event.get():
                        window.blit(win,(0,0))
                        pygame.display.flip()
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN:
                                end = 0
                            elif event.key == K_ESCAPE:
                                initiate = 0
                                end = 0
                        if event.type == QUIT:
                            sys.exit()
                done = 0
            pygame.time.Clock().tick(10)