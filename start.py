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
    player = pygame.image.load(MACGYVER).convert_alpha()
    player = pygame.transform.scale(player, (SPRITE_SIZE, SPRITE_SIZE))
    mygard = pygame.image.load(GARDIEN).convert_alpha()
    mygard = pygame.transform.scale(mygard, (SPRITE_SIZE, SPRITE_SIZE))

    # Generate Maze
    generate_maze()
    maze = Maze('n1')
    maze.generate()
    # Create Wall
    maze.wall(window)

    # Create MacGyver
    myplayer = Player(maze)

    # Create Medoc
    guard = Guard(maze)
    guard.guardPosition(window)

    # Randomly position items in the maze
    item = Item(maze)
    item.itemPosition()
    item.displayItems(myplayer, window)

    # Guard kill count
    guard_killed = 0
    # Ture  condition for wile loop
    done = 1
    direction = None
    while done:
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
        # new positions to be displayed on screen
        window.blit(fond, (0, 0))
        maze.wall(window)
        item.displayItems(myplayer, window)
        window.blit(player, myplayer.player_position)

        # Guard disapears if MacGyver make a contact
        if guard.gardien_position == myplayer.player_position:
            guard_killed = 1

        if guard_killed != 1:
            window.blit(mygard, guard.gardien_position)

         # refresh screen
        pygame.display.update()
        pygame.time.Clock().tick(10)

        # Game closes if MacGyver finds exit
        if maze.exit_position == myplayer.player_position and item.score == 3:
            go = 1
            while go:
                for event in pygame.event.get():
                    text = font.render('You Win!!', True, (0, 0, 0))
                    window.fill((255, 255, 255))
                    window.blit(text, ((SCREEN_SIZE - text.get_width()) // 2,
                                       (SCREEN_SIZE - text.get_height()) // 2))
                    pygame.display.flip()
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        go = 0
                    elif event.type == QUIT:
                        sys.exit()

            done = 0
        # Game closes if MacGyver makes a contact with the guard
        if guard.gardien_position == myplayer.player_position and item.score != 3:
            go = 1
            while go:
                for event in pygame.event.get():
                    text = font.render('You lose!!', True, (255, 255, 255))
                    window.fill((0, 0, 0))
                    window.blit(text, ((SCREEN_SIZE - text.get_width()) // 2,
                                       (SCREEN_SIZE - text.get_height()) // 2))
                    pygame.display.flip()

                    if event.type == KEYDOWN and event.key == K_RETURN:
                        go = 0
                    elif event.type == QUIT:
                        sys.exit()
            done = 0



