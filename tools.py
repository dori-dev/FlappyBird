import pygame

class Tools:
    def __init__(self, window, data_path):
        self.window = window
        self.sprites = pygame.image.load(data_path).convert_alpha()

    def button(self, image, x, y, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        w, h = image.get_width(), image.get_height()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1:
                action()
        self.window.blit(image, (x, y))

    def update_display(self, *objects):
        for obj in objects:
            if isinstance(obj, list):
                for o in obj:
                    o.draw(self.window)
            else:
                obj.draw(self.window)

        pygame.display.update()

    def resize_image(self, image, ratio=1):
        w, h = pygame.display.get_surface().get_size()
        if ratio == 1:
            width_ratio = w / 120
            height_ratio = h / 256
        else:
            width_ratio = ratio
            height_ratio = ratio

        new_width = int(image.get_size()[0] * width_ratio)
        new_height = int(image.get_size()[1] * height_ratio)

        return pygame.transform.scale(image, (new_width, new_height))

    def setup_image(self, width, height, x1, y1, x2, y2, scale=1, source=None,):
        if not source:
            source = self.sprites
        image = pygame.Surface(
            (width, height),
            pygame.SRCALPHA, 32
        ).convert_alpha()
        image.blit(source, (0, 0), (x1, y1, x2, y2))
        return self.resize_image(image, scale)

    def load_sprites(self):
        world = {}
        world['background'] = self.setup_image(140, 256, 0, 0, 140, 256)
        world['floor'] = self.setup_image(145, 56, 292, 0, 432, 56)
        world['pipe'] = self.setup_image(26, 160, 84, 323, 109, 482)

        bird_images = {}
        bird_images['descend'] = self.setup_image(20, 14, 1, 490, 20, 504)
        bird_images['idle'] = self.setup_image(20, 14, 29, 490, 48, 504)
        bird_images['ascend'] = self.setup_image(20, 14, 57, 490, 76, 504)

        messages = {}
        messages['game_title'] = self.setup_image(92, 24, 350, 90, 440, 115)
        messages['gameover'] = self.setup_image(96, 24, 395, 57, 460, 100)

        buttons = {}
        buttons['play'] = self.setup_image(52, 29, 354, 118, 406, 147)

        scoreboard = self.setup_image(113, 57, 3, 259, 116, 316)
        scoreboard = pygame.transform.scale(
            scoreboard, (int(113*2), int(57*2)))

        numbers = {}
        numbers[0] = self.setup_image(7, 10, 137, 306, 144, 316, 2)
        numbers[1] = self.setup_image(7, 10, 137, 477, 144, 488, 2)
        numbers[2] = self.setup_image(7, 10, 137, 489, 144, 499, 2)
        numbers[3] = self.setup_image(7, 10, 131, 501, 138, 511, 2)
        numbers[4] = self.setup_image(7, 10, 502, 0, 509, 10, 2)
        numbers[5] = self.setup_image(7, 10, 502, 12, 509, 22, 2)
        numbers[6] = self.setup_image(7, 10, 505, 26, 512, 36, 2)
        numbers[7] = self.setup_image(7, 10, 505, 42, 512, 52, 2)
        numbers[8] = self.setup_image(7, 10, 293, 242, 300, 252, 2)
        numbers[9] = self.setup_image(7, 10, 311, 206, 318, 216, 2)

        return world, bird_images, messages, buttons, numbers, scoreboard
