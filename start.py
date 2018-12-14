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


while 1:
    # Initialize pygame
    pygame.init()
    pygame.font.init()

    # Window size
    window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + SPRITE_SIZE))

    # Setting a font type
    font = pygame.font.SysFont('OCR A Std', 72)
    # Window title
    pygame.display.set_caption('MacGyver Labyrinthe')

    # Load images
    fond = pygame.image.load(FOND).convert()
    fond = pygame.transform.scale(fond, (SCREEN_SIZE, SCREEN_SIZE))
    macgyver = pygame.image.load(MACGYVER).convert_alpha()
    macgyver = pygame.transform.scale(macgyver, (SPRITE_SIZE, SPRITE_SIZE))
    medoc = pygame.image.load(GARDIEN).convert_alpha()
    medoc = pygame.transform.scale(medoc, (SPRITE_SIZE, SPRITE_SIZE))
    block = pygame.image.load(MUR).convert()

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
    item.itemPosition()
    item.displayItems(myplayer, window)

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
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or
                    event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    direction = None
        myplayer.move(direction)
        if count % 3:
            guard.set_guard_position()
            count -= 2
        # New positions to be displayed on screen
        window.blit(fond, (0, 0))
        maze.blit_walls(window)
        item.displayItems(myplayer, window)
        window.blit(macgyver, myplayer.player_position)
        # Hide Medoc if he contacts with MacGyver
        if guard.guard_position == myplayer.player_position:
            guard_killed = 1

        if not guard_killed:
            # Hide exit
            window.blit(medoc, guard.guard_position)

        pygame.display.flip()
        pygame.time.Clock().tick(10)

        if guard.guard_position == myplayer.player_position and item.score != 3:
            go = 1
            # Only display Medoc if he wins
            window.blit(medoc, guard.guard_position)
            while go:
                for event in pygame.event.get():
                    text = font.render('YOU LOST!!', True, (255, 11, 21))

                    window.blit(text, ((SCREEN_SIZE - text.get_width()) // 2,
                                       (SCREEN_SIZE - text.get_height()) // 2))
                    pygame.display.flip()

                    if event.type == KEYDOWN and event.key == K_RETURN:
                        go = 0
                    elif event.type == QUIT:
                        sys.exit()
            done = 0
        # create exit
        if guard_killed and item.score == 3:
            strucutre = maze.structure[13][14] = 'e'
            Maze(structure)

        # Game closes if MacGyver finds exit
        if maze.exit_position == myplayer.player_position and item.score == 3:
            go = 1
            while go:
                for event in pygame.event.get():
                    text = font.render('YOU WON!!', True, (11, 19, 255))

                    window.blit(text, ((SCREEN_SIZE - text.get_width()) // 2,
                                       (SCREEN_SIZE - text.get_height()) // 2))
                    pygame.display.flip()
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        go = 0
                    elif event.type == QUIT:
                        sys.exit()

            done = 0





