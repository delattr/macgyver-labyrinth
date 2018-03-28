import random
import pygame
from pygame.locals import *
from constantes import *


class Maze:

    def __init__(self, text):
        self.text = text
        self.sturcture = []
        self.corridor = []
        self.exit_position = 0
        self.starting_position = 0

    # Generate maze by reading the text file
    def generate(self):
        with open(self.text, "r") as text:
            structure_list = []
            for line in text:
                each_line = []
                for letter in line:
                    if letter != '\n':
                        each_line.append(letter)
                structure_list.append(each_line)
            self.structure = structure_list

    # converting coordinate to actual pixels
    def wall(self, window):

        wall = pygame.image.load(mur).convert()
        depart = pygame.image.load(start).convert()
        sortie = pygame.image.load(exit).convert()

        row = 0
        for line in self.structure:
            column = 0
            for letter in line:
                y = row * sprite_size
                x = column * sprite_size
                if letter == 'x':    # x = wall
                    window.blit(wall, (x, y))
                elif letter == 's':  # s = starting postion
                    window.blit(depart, (x, y))
                    self.starting_position = (x, y)
                elif letter == '0':  # 0 = corridor
                    self.corridor.append((x, y))
                elif letter == 'e':
                    window.blit(sortie, (x, y))
                    self.exit_position = (x, y)
                column += 1
            row += 1


# Determine position of the guard
class Guard:

    def __init__(self, maze):
        self.maze = maze
        self.guard_position = 0

    def guardPosition(self, window):

        row = int(self.maze.exit_position[1] / sprite_size)
        column = int(self.maze.exit_position[0] / sprite_size)

        x_axis = int(column * sprite_size)
        y_axis = int(row * sprite_size)

        up = row - 1
        down = row + 1
        left = column - 1
        right = column + 1

        possible_position = {}

        # Find coordiates of blocks around the exit and add them to a dictioanry
        try:
            possible_position['up'] = self.maze.structure[up][column]
        except IndexError:
            pass
        try:
            possible_position['down'] = self.maze.structure[down][column]
        except IndexError:
            pass
        try:
            possible_position['left'] = self.maze.structure[row][left]
        except IndexError:
            pass
        try:
            possible_position['right'] = self.maze.structure[row][right]
        except IndexError:
            pass
        # Checking for blocks which has value of '0'
        check_position = {k: v for k, v in possible_position.items() if v == '0'}
        # Selects a random block by passing a key from the check_position dictionary
        gardien_case = random.choice(list(check_position.keys()))
        # Calculate postion of the guard to be displayed on the screen
        if gardien_case == 'up':
            y_axis -= sprite_size
            self.gardien_position = (x_axis, y_axis)

        elif gardien_case == 'down':
            y_axis += sprite_size
            self.gardien_positon = (x_axis, y_axis)

        elif gardien_case == 'right':
            x_axis += sprite_size
            self.gardien_position = (x_axis, y_axis)

        elif gardien_case == 'left':
            x_axis -= sprite_size
            self.gardien_position = (x_axis, y_axis)

        self.maze.corridor.remove(self.gardien_position)
        mygard = pygame.image.load(gardien).convert_alpha()
        window.blit(mygard, self.gardien_position)


# Randomly reate postion of items
class Item:

    def __init__(self, maze):
        self.maze = maze
        self.score = 0

        item1 = pygame.image.load(arrow).convert_alpha()
        item2 = pygame.image.load(tube).convert_alpha()
        item3 = pygame.image.load(ether).convert_alpha()

        self.item_name = [item1, item2, item3]
        self.item_position = []
        self.items_picked_up = []

    def itemPosition(self):
        for i in range(3):
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
            self.window.blit(self.items_picked_up[i], (sprite_size * i, screen_size))
        # Displays a finish.png on score board
        if len(self.items_picked_up) == 3:
            end = pygame.image.load(finish).convert()
            self.window.blit(end, (sprite_size * 3, screen_size))


class Player:

    def __init__(self, maze):
        # position of player in terms of coordiates and pixels
        self.maze = maze
        self.player_position = self.maze.starting_position

    def move(self, direction):
        # Calculate opstion of player in coordiates and pixels
        row = int(self.player_position[1] / sprite_size)
        column = int(self.player_position[0] / sprite_size)
        x_axis = self.player_position[0]
        y_axis = self.player_position[1]

        # Directin choosen by player
        if direction == 'up':
            # cannot go over the boarder of screen
            if y_axis > 0:
                # cannot go through the wall
                if self.maze.structure[row - 1][column] != "x":
                    # calculate new postion
                    y_axis -= sprite_size
                    # passing new postion as a tuple to a variable
                    self.player_position = (x_axis, y_axis)

        elif direction == 'down':
            if y_axis < (screen_size - sprite_size):
                if self.maze.structure[row + 1][column] != "x":
                    y_axis += sprite_size
                    self.player_position = (x_axis, y_axis)

        elif direction == 'right':
            if x_axis < (screen_size - sprite_size):
                if self.maze.structure[row][column + 1] != "x":
                    x_axis += sprite_size
                    self.player_position = (x_axis, y_axis)

        elif direction == 'left':
            if x_axis > 0:
                if self.maze.structure[row][column - 1] != "x":
                    x_axis -= sprite_size
                    self.player_position = (x_axis, y_axis)
