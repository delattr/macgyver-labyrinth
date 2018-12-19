import random
import pygame
from pygame.locals import *
from constants import *


class Maze:

    def __init__(self, structure):
        self.structure = structure
        self.sturcture = []
        self.corridor = []
        self.exit_position = 0
        self.starting_position = 0

    # Generate maze by reading the text file

    def blit_walls(self, window):

        wall = pygame.image.load(MUR).convert()
        depart = pygame.image.load(START).convert()
        sortie = pygame.image.load(EXIT).convert()

        row = 0
        for line in self.structure:
            column = 0
            for letter in line:
                y = row * SPRITE_SIZE
                x = column * SPRITE_SIZE
                if letter == 'x':    # x = wall
                    window.blit(wall, (x, y))
                elif letter == 's':  # s = starting postion
                    window.blit(depart, (x, y))
                    self.starting_position = (x, y)
                elif letter == 'o':  # 0 = corridor
                    self.corridor.append((x, y)) # Contains open areas
                elif letter == 'e':
                    window.blit(sortie, (x, y))
                    self.exit_position = (x, y)
                column += 1
            row += 1


# Determine position of the guard
class Guard:

    def __init__(self, maze):
        self.maze = maze
        self.guard_position = ()
        self.guard_position = random.choice(maze.corridor)
        self.unvisited = set(maze.corridor)
        self.stack = []
        self.visited = set()

    def set_guard_position(self):

        # Coordinate of guard in pixels
        x = int(self.guard_position[0])
        y = int(self.guard_position[1])

        # Check coordinates of neighbouring blocks
        up = (x, y - SPRITE_SIZE)
        down = (x, y + SPRITE_SIZE)
        left = (x - SPRITE_SIZE, y)
        right = (x + SPRITE_SIZE, y)
        neighbours =[up, down, left, right]
        # Find adjacent cells available
        adjacent_cells = [x for x in neighbours if x in self.unvisited]
        if not self.unvisited:
            self.unvisited = self.visited
            self.visited = set()
        if adjacent_cells:
            # Push the current position to the stack
            self.stack.append(self.guard_position)
            # Select next block to move
            next_cell = random.choice(adjacent_cells)
            # Mark next block as visited
            self.unvisited.remove(next_cell)
            self.visited.add(next_cell)
            # Move to next block
            self.guard_position = (next_cell)
        # If there are no adjacet cells and stack is not empty
        elif self.stack:
            last_cell = self.stack.pop()
            self.guard_position = last_cell

# Randomly create postion of items
class Item:

    def __init__(self, maze):
        self.corridor = maze.corridor
        self.score = 0


        arrow = pygame.image.load(ARROW).convert_alpha()
        tube = pygame.image.load(TUBE).convert_alpha()
        ether = pygame.image.load(ETHER).convert_alpha()

        self.items= [arrow,tube,ether]
        self.item_positions =[]
        self.items_obtained = []

    def set_item_positions(self):
        for index in enumerate(self.items):
            item = random.choice(self.corridor)
            self.corridor.remove(item)
            self.item_positions.append(item)

    def display_items(self, player_position, window):

        self.player_position = player_position
        self.window = window

        for index, value in enumerate(self.items) :
            # Matching item name and position from two lists and display them on the screen
            self.window.blit(value, self.item_positions[index])

        # Check if player has obtained an item
        if self.player_position in self.item_positions:
                # Find index number of the item postion
                for i,v in enumerate(self.item_positions):
                    if v == self.player_position:
                        # append the item to self.items_obtained
                        self.items_obtained.append(self.items[i])
                        # Remove the item from self.items
                        del self.items[i]
                self.item_positions.remove(self.player_position)
                self.score += 1

        if self.items_obtained:
            #Display Items obtained on the score board
            for index, value in enumerate(self.items_obtained) :
                self.window.blit(value, (SPRITE_SIZE * index, SCREEN_SIZE))
        # Displays a finish.png on score board
        if self.score == 3:
            end = pygame.image.load(FINISH).convert()
            self.window.blit(end, (SPRITE_SIZE * 3, SCREEN_SIZE))


class Player:

    def __init__(self, maze):
        # position of player in terms of coordiates and pixels
        self.maze = maze
        self.player_position = self.maze.starting_position

    def move(self, direction):
        # Calculate opstion of player in coordiates and pixels
        row = int(self.player_position[1] / SPRITE_SIZE)
        column = int(self.player_position[0] / SPRITE_SIZE)
        x_axis = self.player_position[0]
        y_axis = self.player_position[1]

        # Directin choosen by player
        if direction == 'up':
            # cannot go over the boarder of screen
            if y_axis > 0:
                # cannot go through the wall
                if self.maze.structure[row - 1][column] != "x":
                    # calculate new postion
                    y_axis -= SPRITE_SIZE
                    # passing new postion as a tuple to a variable
                    self.player_position = (x_axis, y_axis)

        elif direction == 'down':
            if y_axis < (SCREEN_SIZE - SPRITE_SIZE):
                if self.maze.structure[row + 1][column] != "x":
                    y_axis += SPRITE_SIZE
                    self.player_position = (x_axis, y_axis)

        elif direction == 'right':
            if x_axis < (SCREEN_SIZE - SPRITE_SIZE):
                if self.maze.structure[row][column + 1] != "x":
                    x_axis += SPRITE_SIZE
                    self.player_position = (x_axis, y_axis)

        elif direction == 'left':
            if x_axis > 0:
                if self.maze.structure[row][column - 1] != "x":
                    x_axis -= SPRITE_SIZE
                    self.player_position = (x_axis, y_axis)
        elif direction == None:
             return self.player_position
        return self.player_position