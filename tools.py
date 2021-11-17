"""toolkit for game.
"""
from typing import List
import pygame


class Tools:
    """Tools for game
    """

    def __init__(self, window, data_path):
        self.window = window
        self.sprites = pygame.image.load(data_path).convert_alpha()

    def button(self, image, x_pos, y_pos, action):
        """make button in game

        Args:
            image (pygame surface): image of button
            x_pos (int): position(x)
            y_pos (int): position(y)
            action (object): call function, when clicked button
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        width, height = image.get_width(), image.get_height()
        if x_pos+width > mouse[0] > x_pos and y_pos+height > mouse[1] > y_pos:
            if click[0] == 1:
                action()
        self.window.blit(image, (x_pos, y_pos))

    def update_display(self, *objects):
        """update display with *objects
        """
        for object_ in objects:
            if isinstance(object_, list):
                for obj in object_:
                    obj.draw(self.window)
            else:
                object_.draw(self.window)

        pygame.display.update()

    @staticmethod
    def resize_image(image, ratio=1):
        """resize the image

        Args:
            image (pygame surface): image
            ratio (int, optional): ratio for manual width and height ratio. Defaults to 1.

        Returns:
            pygame surface: image changed scale
        """
        width, height = pygame.display.get_surface().get_size()
        if ratio == 1:
            width_ratio = width / 120
            height_ratio = height / 256
        else:
            width_ratio = ratio
            height_ratio = ratio

        new_width = int(image.get_size()[0] * width_ratio)
        new_height = int(image.get_size()[1] * height_ratio)

        return pygame.transform.scale(image, (new_width, new_height))

    def setup_image(self, size: tuple, positions: List[tuple], scale=1, source=None):
        """setup the image

        Args:
            size (tuple): width and height
            positions (List[tuple): position 1, position 2
            scale (int, optional): scale of image. Defaults to 1.
            source (image, optional): new image source. Defaults to None.

        Returns:
            pygame surface: image be setup
        """
        width, height = size
        x_pos1, y_pos1, x_pos2, y_pos2 = positions
        if not source:
            source = self.sprites
        image = pygame.Surface(
            (width, height),
            pygame.SRCALPHA, 32
        ).convert_alpha()
        image.blit(source, (0, 0), (x_pos1, y_pos1, x_pos2, y_pos2))
        return self.resize_image(image, scale)

    def load_images(self):
        """load all images need for game

        Returns:
            tuple: all image(dict or etc)
        """
        world = {}
        world['background'] = self.setup_image((140, 256), (0, 0, 140, 256))
        world['floor'] = self.setup_image((145, 56), (292, 0, 432, 56))
        world['pipe'] = self.setup_image((26, 160), (84, 323, 109, 482))

        bird_images = {}
        bird_images['descend'] = self.setup_image((20, 14), (1, 490, 20, 504))
        bird_images['idle'] = self.setup_image((20, 14), (29, 490, 48, 504))
        bird_images['ascend'] = self.setup_image((20, 14), (57, 490, 76, 504))

        messages = {}
        messages['game_title'] = self.setup_image(
            (92, 24), (350, 90, 440, 115))
        messages['gameover'] = self.setup_image((96, 24), (395, 57, 460, 100))

        buttons = {}
        buttons['play'] = self.setup_image((52, 29), (354, 118, 406, 147))

        scoreboard = self.setup_image((113, 57), (3, 259, 116, 316))
        scoreboard = pygame.transform.scale(
            scoreboard, (int(113*2), int(57*2)))

        numbers = {}
        numbers[0] = self.setup_image((7, 10), (137, 306, 144, 316), 2)
        numbers[1] = self.setup_image((7, 10), (137, 477, 144, 488), 2)
        numbers[2] = self.setup_image((7, 10), (137, 489, 144, 499), 2)
        numbers[3] = self.setup_image((7, 10), (131, 501, 138, 511), 2)
        numbers[4] = self.setup_image((7, 10), (502, 0, 509, 10), 2)
        numbers[5] = self.setup_image((7, 10), (502, 12, 509, 22), 2)
        numbers[6] = self.setup_image((7, 10), (505, 26, 512, 36), 2)
        numbers[7] = self.setup_image((7, 10), (505, 42, 512, 52), 2)
        numbers[8] = self.setup_image((7, 10), (293, 242, 300, 252), 2)
        numbers[9] = self.setup_image((7, 10), (311, 206, 318, 216), 2)

        icon = self.setup_image((100, 85), (379, 173, 478, 257), 1)

        return world, bird_images, messages, buttons, numbers, scoreboard, icon
