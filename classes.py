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


        # corridor list contains open areas in pixel


        # index of exit in the structure list
        x = int(self.guard_position[0])
        y = int(self.guard_position[1])

        #check premisis
        up = (x, y - SPRITE_SIZE)
        down = (x, y + SPRITE_SIZE)
        left = (x - SPRITE_SIZE, y)
        right = (x + SPRITE_SIZE, y)
        # adjacent_cells
        neighbours =[up,down,left,right]
        #find an opened area
        adjacent_cells = [x for x in neighbours if x in self.unvisited]
        if not self.unvisited:
            self.unvisited = self.visited
            self.visited = set()
        if adjacent_cells:
            #Push the current_position to the stack
            self.stack.append(self.guard_position)
            next_cell = random.choice(adjacent_cells)
            self.unvisited.remove(next_cell)
            self.visited.add(next_cell)
            # move to that direction
            self.guard_position = (next_cell[0], next_cell[1])
        elif self.stack:
            last_cell = self.stack.pop()
            self.guard_position = last_cell

# Randomly create postion of items
class Item:

    def __init__(self, maze,):
        self.maze = maze
        self.score = 0

        item1 = pygame.image.load(ARROW).convert_alpha()
        item2 = pygame.image.load(TUBE).convert_alpha()
        item3 = pygame.image.load(ETHER).convert_alpha()

        self.item_name = [item1, item2, item3]
        self.item_position = []
        self.items_picked_up = []

    def itemPosition(self):
        for i in range(len(self.item_name)):
            item = random.choice(self.maze.corridor)
            self.item_position.append(item)
            self.maze.corridor.remove(item)

    def displayItems(self, player, window):

        self.player = player
        self.window = window

        item_obtained = False
        for i in range(len(self.item_position)):
            # Matching item name and position from two lists and display them on the screen
            self.window.blit(self.item_name[i], self.item_position[i])
            # Setting name and position of item obtained to a variable
            if self.player.player_position == self.item_position[i]:
                del_item_position = self.item_position[i]
                del_item_name = self.item_name[i]
                # Passes item picked up to a new list in order
                self.items_picked_up.append(del_item_name)
                # tracks the score
                self.score += 1
                item_obtained = True
        # Removes item obtained from the lists
        if item_obtained:
            self.item_position.remove(del_item_position)
            self.item_name.remove(del_item_name)

        # Display Items obtained on score board
        for i in range(len(self.items_picked_up)):
            self.window.blit(self.items_picked_up[i], (SPRITE_SIZE * i, SCREEN_SIZE))
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
        return self.player_position