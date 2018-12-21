import unittest
from classes import Maze, Guard, Item, Player
from maze import generate_maze, visited_cells, stack
import constants as const
import os

class Test(unittest.TestCase):

    def test_constants(self):
        # Get relative path for "images" directory
        cwd = os.getcwd()
        images_dir = os.path.join(cwd, 'images')
        images_path = os.path.relpath(images_dir, cwd)
        # realtive path for "music" directory
        music_dir = os.path.join(cwd, 'music')
        music_path = os.path.relpath(music_dir)
        # Test Constatant values
        self.assertEqual(const.SPRITE_SIZE, 32)
        self.assertEqual(const.TILE, 15)
        self.assertEqual(const.START, os.path.join(images_path,'depart.png'))
        self.assertEqual(const.FOND, os.path.join(images_path,'fond.jpg'))
        self.assertEqual(const.MUR, os.path.join(images_path,'mur.png'))
        self.assertEqual(const.MACGYVER, os.path.join(images_path,'macgyver.png'))
        self.assertEqual(const.NIDDLE, os.path.join(images_path,'niddle.png'))
        self.assertEqual(const.ETHER, os.path.join(images_path,'ether.png'))
        self.assertEqual(const.TUBE, os.path.join(images_path,'tube.png'))
        self.assertEqual(const.EXIT, os.path.join(images_path,'exit.png'))
        self.assertEqual(const.GARDIEN, os.path.join(images_path,'gardien.png'))
        self.assertEqual(const.FINISH, os.path.join(images_path,'finish.png'))
        self.assertEqual(const.SYRINGE, os.path.join(images_path,'syringe.png'))
        self.assertEqual(const.WIN, os.path.join(images_path,'win.png'))
        self.assertEqual(const.LOOSE, os.path.join(images_path,'loose.png'))
        self.assertEqual(const.WELCOME, os.path.join(images_path,'welcome.gif'))
        self.assertEqual(const.MUSIC, os.path.join(music_path,'bg-music.mp3'))

    def test_maze_structure(self):

        # Test if sturcture is 15x15
        structure = generate_maze()

        # Count rows
        for row in structure:
            self.assertEqual(len(row), 15)
        # count columns
        self.assertEqual(len(structure), 15)

if __name__ == '__main__':
    unittest.main()