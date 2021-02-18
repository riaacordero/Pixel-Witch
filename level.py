"""
Contains Level and Camera classes and data for each level.
"""

from sprite import *
import numpy as np

level_one_data = np.array([
    "PPPPPPPPPPPPPPPPP",
    "P---------------P",
    "P--D----------K-P",
    "PPPPPP-------PPPP",
    "P---------------P",
    "P---R---E---Y-B-P",
    "P---PPPPPPPPPPPPP",
    "P---------------P",
    "PB-E--Y---------P",
    "PPPPPPP---------P",
    "P-----PPPP------P",
    "P---------------P",
    "P-------------GPP",
    "P0---------G-PPPP",
    "P--Y---E-BPPPPPPP",
    "PPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPP"
])

level_two_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P-0----------------------PP",
    "P-------------------D----PP",
    "P---Y------------PPPPPP--PP",
    "PPPPPP-------------------PP",
    "P----------------------G-PP",
    "P--------------E-----PPPPPP",
    "P---PPPPPPPPPPPPP----PPPPPP",
    "P--------------------PPPPPP",
    "PR----E--------------PPPPPP",
    "PPPPPPP---G---------------P",
    "P-----PPPPP---------------P",
    "P-------------------------P",
    "P-------------Y-PPPPPPPPPPP",
    "P----------G-PPPP---------P",
    "P-------------------------P",
    "P--E--E-------------E---KBP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_three_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P-------------------------PP",
    "P------------------Y------PP",
    "P--K--------PPPPPPPPPPP---PP",
    "PPPPPP--------------------PP",
    "P----------------------G-PPP",
    "P----E---------------PPPPPPP",
    "P----PPPPPP----------PPPPPPP",
    "P--------------PPPPPPPPPPPPP",
    "PR-------------------PPPPPPP",
    "PPPPPPP---G--------Y------PP",
    "P-----PPPPP-------PPP-----PP",
    "P------------------------GPP",
    "P-----------G-PPPP-------PPP",
    "P-----------PPPPP-------0-PP",
    "P-------------------------PP",
    "P--D--E-----B------T------PP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_four_data = np.array([
    "PPPPPPPPPPPPPPPPPPPP",
    "P0-----------------P",
    "P----------------D-P",
    "P--------------PPPPP",
    "P------------G-PPPPP",
    "P----PPPP---PPPPPPPP",
    "P------------------P",
    "P----------------G-P",
    "P--------------PPPPP",
    "P--PPPPPPPPP-------P",
    "P------------------P",
    "P-----------------KP",
    "P--P---PPPPPPPPP--PP",
    "P-----------------PP",
    "P--BE----Y--------PP",
    "P--PPPPPPPPPP--PPPPP",
    "P-----------------PP",
    "P----Y-----E-----BPP",
    "PPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPP"
])

level_five_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P-------------------------------P",
    "P----------------------------D--P",
    "P-------------------PPPPPPPPPPPPP",
    "P------------PPPPPPP------------P",
    "P-------PPPPPP---------G-----E-BP",
    "P-------------------Y--PPPPPPPPPP",
    "P----------------G-PPPPPPPPPPPPPP",
    "P--------------PPPPPPPPPPPPPPPPPP",
    "P--PPPPPPPPP-----------PPPPPPPPPP",
    "P----------------------PPPPPPPPPP",
    "P----------------------PPPPPPPPPP",
    "PPPP---PPPPPPP-----------PPPPPPPP",
    "P--------------------------PPPPPP",
    "P---E----------Y-PPP----------0-P",
    "P--PPPPPPPPPP--PPPPPP-----------P",
    "PB------------------PPPP--------P",
    "PPPPB------E-----K--PPPPP-B-----P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_six_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P--------------------PP-----------P",
    "P-K------------------PP-D-------0-P",
    "PPPP-------------G--RPPPPPPP---PPPP",
    "P-------G-PPPPPPPPPPPP------------P",
    "P-----PPPP-----------P----------G-P",
    "P--------------------PPP----PPPPPPP",
    "P---------------------------------P",
    "PPPPPP-----------------Y----------P",
    "P-------------E-----PPPPPPP---PPPPP",
    "P--------PPPPPPP------------------P",
    "P-------PPP-----------R-E---------P",
    "P-------------------PPPPPPPPPLLLLLP",
    "P------------------PPPPPPPPPPPPPPPP",
    "P--PPPPPP---------PPPPPPPPPPPPPPPPP",
    "P---------------PPPPPPPPPPPPPPPPPPP",
    "P-------------PPPPPPPPPPPPPPPPPPPPP",
    "P-B--------G--PPPPPPPPPPPPPPPPPPPPP",
    "PPPPLLLLLLPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_seven_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P--------------------PP-----------P",
    "P-E------------------PP-E-------K-P",
    "PPPP-------------G-E-PPPPPPP---PPPP",
    "P-------G-PPPPPPPPPPPP------------P",
    "P-----PPPP-----------E---------YG-P",
    "P--------------------PPP----PPPPPPP",
    "P---------------------------------P",
    "PPPPPP-----------------G----------P",
    "P---------Y---EB----PPPPPPPP----PPP",
    "P--------PPPPPPP------------------P",
    "P-T----PPPP-----------R-E------B--P",
    "PPPP---------------PPPPPPPPP---PPPP",
    "P----G----------------------------P",
    "P--PPPPPPPPP--------------------D-P",
    "P-----------------PPPPPPLLLLLPPPPPP",
    "P0--------------PPPPPPPPPPPPPPPPPPP",
    "P-B---------G-PPPPPPPPPPPPPPPPPPPPP",
    "PPPPLLLPLLLPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_eight_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P---------------------------------P",
    "P-E---------------------D-----E---P",
    "PPPP-------------G---PPPPPPPPPPPPPP",
    "P-------G-PPPPPPPPPPPP------------P",
    "P-----PPPP-----------E---------YG-P",
    "P--------------------PPP----PPPPPPP",
    "PK--------------------------------P",
    "PPPPPP----------------YG----------P",
    "P---------Y---EB----PPPPPPPP----PPP",
    "P--------PPPPPPP------------------P",
    "P------PPPP-----------R-E------B--P",
    "PPPP---------------PPPPPPP---PPPPPP",
    "P----G---------------------G------P",
    "P-------------------------------G-P",
    "PLLLLLPG----------PPPPPPLLLLLPPPPPP",
    "PPPPPPPPPPPP----PPPPPPPPPPPPPPPPPPP",
    "P-------------------------------0-P",
    "PB-----E---E------E------------Y--P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

level_nine_data = np.array([
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P-------------------P-------------P",
    "P-D-----------------P---Y-----E---P",
    "PPPP-------------G--PP--PPPPPPPPPPP",
    "P-------G-PPPPPPPPPPPP------------P",
    "P-----PPPPP----------E---------G--P",
    "P--------------------PPP----PPPPPPP",
    "P-------------G-------------------P",
    "PPPPPP----------------------------P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPP----PPP",
    "P--------PPPPPPP------------------P",
    "P-------GPP--------------------B--P",
    "PPPP-----P-E------RPPPPPPP---PPPPPP",
    "PPPPP----PPPPPPPPPPPPPPPPP---PPPPPP",
    "P-------------------------------G-P",
    "P-----T---------------------------P",
    "PP---PPPPPPP----PPPPPPPPPPPPPPPPPPP",
    "P-------------------------------0-P",
    "P---------------------------------P",
    "PB--------------------------------P",
    "PPPPPPPPPP--PPPPPP---PPPPPPPPPPPPPP",
    "PLLLLLLLLLLLLLLLLL---LLLLLLLLLLLLLL",
    "PPPPPPPPPPPPPPPPPP--BPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPP--PPPPPPPPPPPPPPP",
    "P---------------------------------P",
    "P---------------------------------P",
    "P-D-------------------------------P",
    "PPPP------------------------------P",
    "P------------------------G--------P",
    "PE-B---------------K-----R--------P",
    "PPPPPPPPLLLLLLLLLLLLPPPPPPPPLLLLLPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
])

levels_data = [level_one_data, level_two_data, level_three_data, level_four_data, level_five_data, level_six_data,
               level_seven_data, level_eight_data, level_nine_data]

levels_max_scores = [25, 40, 30, 20, 20, 30, 40, 60, 35]

class Camera(pygame.sprite.LayeredUpdates):
    """
    Game camera following the player that acts similarly with a pygame.sprite.Group() object.
    All sprites must be added to a Camera() object to make them adjust to it. There should be
    one camera per level so that each Camera() object can adjust depending on the level's size
    and so that the sprites in each level are grouped in only one Camera() object.
    """

    def __init__(self, target, level_size):
        super().__init__()

        self.target = target
        """Item to be followed by the camera (player)"""

        self.level_size = level_size
        """pygame.Rect(), size of the whole level in pixels"""

        self.camera = pygame.Vector2(0, 0)
        """Coordinates of the camera"""

    def update(self, *args):
        super().update(*args)
        if self.target:
            self.add(self.target)
            # Checks how far the target is from the center of the screen
            x = screen_width / 2 - self.target.rect.center[0]
            y = screen_height / 2 - self.target.rect.center[1]
            distance = pygame.Vector2(x, y)
            # Adjusts camera
            self.camera += (distance - self.camera) * 0.05
            # Makes sure camera does not go beyond the level's width and height
            self.camera.x = max(-(self.level_size.width - screen_width), min(0, self.camera.x))
            self.camera.y = max(-(self.level_size.height - screen_height), min(0, self.camera.y))

    def draw(self, surface):
        # Contains some added technicalities for grouping sprites
        dirty = self.lostsprites
        self.lostsprites = []
        for s, old_r in self.spritedict.items():
            new_r = surface.blit(s.image, s.rect.move(self.camera))
            if old_r is False:
                if new_r.colliderect(old_r):
                    dirty.append(new_r.union(old_r))
                else:
                    dirty.append(new_r)
                    dirty.append(old_r)
            else:
                dirty.append(new_r)
            self.spritedict[s] = new_r
        return dirty


class Overlay(pygame.sprite.Sprite):
    """
    Darkens the surrounding of the level.
    """

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = overlay_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Level:
    """
    The stage that comprises of the different sprites that can interact with the player.
    """

    def __init__(self, data: list, target: Player, number, button, *, is_underground, max_score):
        self.target = target
        self.width, self.height = len(data[0]) * tile_size, len(data) * tile_size
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.is_underground = is_underground
        self.background = Background(bg_underground_img if self.is_underground else bg_sky_img, self.width, self.height)
        self.music = bgm_level_underground if self.is_underground else bgm_level_sky

        self.number = number
        """Number to represent the level"""

        self.button = button
        """Button to click on level selection screen to go to this level."""

        self.score = 0
        """Score gained by the player by getting gems"""

        self.high_score = 0
        """Highest score gained by the player"""

        self.max_score = max_score
        """Highest possible score to get in the level"""

        # Groups present per level
        self.platforms = pygame.sprite.Group()
        self.lava_platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.consumables = pygame.sprite.Group()

        self.sprites = pygame.sprite.OrderedUpdates()
        """Group that comprises of all sprites in the level"""

        self.active_sprites = Camera(target, self.rect)
        """Camera group that comprises of all active sprites in the level"""

        self.active_sprites.add(self.background)

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                x, y = column_count * tile_size, row_count * tile_size
                if tile == "0":
                    self.target_x, self.target_y = x, y
                if tile == "P":
                    Platform(x, y, self.platforms, self.sprites)
                elif tile == "E":
                    Enemy(x, y - 30, self.enemies, self.sprites)
                elif tile == "D":
                    self.door = Door(x, y - (tile_size // 2), self.sprites)
                elif tile == "B":
                    BluePotion(x, y, self.consumables, self.sprites)
                elif tile == "R":
                    RedPotion(x, y, self.consumables, self.sprites)
                elif tile == "Y":
                    YellowPotion(x, y, self.consumables, self.sprites)
                elif tile == "G":
                    Gem(x, y, self.consumables, self.sprites)
                elif tile == "K":
                    Key(x, y, self.consumables, self.sprites)
                elif tile == "L":
                    LavaPlatform(x, y, self.lava_platforms, self.sprites)
                elif tile == "T":
                    Torch(x, y, self.consumables, self.sprites)
                column_count += 1
            row_count += 1

    def draw(self, screen):
        self.active_sprites.draw(screen)

    def update(self):
        self.active_sprites.update()

    def reset(self):
        """
        Resets all the sprites in the level, making previously removed consumables and enemies show up again
        """
        self.score = 0
        self.active_sprites.empty()
        self.active_sprites.add(self.background)
        for sprite in self.sprites:
            self.active_sprites.add(sprite)
        self.target.reset(self.target_x, self.target_y, self)
        self.door.reset()
