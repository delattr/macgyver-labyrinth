from constants import *
import random

block = 'x'
cell = 'o'
start = 's'
visited_cells = set()
unvisited_cells = set()
stack = []


def generate_maze():

    # Generate initial cell blocks for auto generation:
    structure = []
    for y in range(0,TILE):          # TILE == maximum number of sprites for y-axis
        line =[]
        for x in range(0,TILE):      # Maxium number of sprites for x-axis
            if not y % 2:            # Block even number lines
                line.append(block)
            elif x % 2:              # creates cell for  odd number
                line.append(cell)
                unvisited_cells.add((y, x)) # store postion of cell
            else:
                line.append(block)
        structure.append(line)
    structure[0][1] = start


    #create unvisited cells

    # The depth-first search algorithm of maze generation is frequently implemented using backtracking:

    # Make the initial cell the current cell and mark it as visited
    current_cell = (1,1)

    # While there are unvisited cells
    while len(unvisited_cells) > 0:
        wall = ()
        # Define current cell's neighbours
        up = (current_cell[0] - 2, current_cell[1])
        down = (current_cell[0] + 2, current_cell[1])
        left = (current_cell[0], current_cell[1] - 2)
        right = (current_cell[0], current_cell[1] + 2)
        neighbours ={'up':up, 'down':down, 'left':left, 'right':right}
        # Find neighbours which have not been visited
        adjacent_cells = dict((k,v) for (k,v) in neighbours.items() if v in unvisited_cells)

        # If the current cell has any unvisited neighbouring cell
        if adjacent_cells:
            # Choose randomly one of the unvisited neighbours
            direction, next_cell = random.choice(list(adjacent_cells.items()))

            # Push the current cell to the stack
            stack.append(current_cell)
            unvisited_cells.remove(next_cell)
            # Remove the wall between the current cell and the chosen cell
            if direction == 'up':
                wall = (current_cell[0] - 1, current_cell[1])
            elif direction == 'down':
                wall = (current_cell[0] + 1, current_cell[1])
            elif direction == 'left':
                wall = (current_cell[0], current_cell[1] - 1)
            elif direction == 'right':
                wall = (current_cell[0], current_cell[1] + 1)
            structure[wall[0]][wall[1]] = cell
            # Make the chosen cell the current cell and mark it as visited
            visited_cells.add(current_cell)
            current_cell = next_cell
        # Else if stack is not empty
        elif unvisited_cells and stack:
             # Pop a cell from the stack
             last_cell = stack.pop()
             # Make it the current cell
             current_cell = last_cell

    return structure

if __name__ == '__main__':
    generate_maze()

