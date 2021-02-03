import pygame
from pygame import display
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fps = 60

# SET SCREEN
screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Pixel Witch")

# GRID VARIABLES
tile_size = 25
game_over = 0

# LOAD IMAGES
bg_img = pygame.image.load('img/bg_img.png')
def_start_img = pygame.image.load("img/default_start_btn.png")
hov_start_img = pygame.image.load("img/hovered_start_btn.png")
def_exit_img = pygame.image.load("img/default_exit_btn.png")
hov_exit_img = pygame.image.load("img/hovered_exit_btn.png")


def display_txt(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Button(pygame.sprite.Sprite):
    """
    Clickable item in screen. Changes image when mouse is hovered on top of it.
    """

    def __init__(self, x, y, default_image, hovered_image=None, *groups):
        super().__init__(*groups)
        self.default_image = default_image
        self.hovered_image = default_image if hovered_image is None else hovered_image
        self.image = default_image
        self.rect = self.default_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def update(self):
        self.image = self.hovered_image if self.is_hovered() else self.default_image

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed(3)[0]


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

        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
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
        # Contains some added technicalities in grouping sprites
        dirty = self.lostsprites
        self.lostsprites = []
        for s, old_r in self.spritedict.items():
            new_r = surface.blit(s.image, s.rect.move(self.camera))
            if old_r:
                if new_r.colliderect(old_r):
                    dirty.append(new_r.union(old_r))
                else:
                    dirty.append(new_r)
                    dirty.append(old_r)
            else:
                dirty.append(new_r)
            self.spritedict[s] = new_r
        return dirty


class Location:
    """
    Current place being shown in screen.
    """

    MAIN_MENU = -1
    LEVEL_LIST = 0
    LEVEL_ONE = 1
    LEVEL_TWO = 2
    LEVEL_THREE = 3


class ColorState:
    """
    State of the player based on the ColorSpace they are in. Except the default value BLACK,
    each ColorState gives the player a unique ability, accessible by pressing SPACE.
    """

    BLACK = 0

    RED = 1
    """Horizontal projectile attack based on what side the player is facing"""

    BLUE = 2
    """Jump"""

    YELLOW = 3
    """One-time use shield"""


class Potion(pygame.sprite.Sprite):
    """
    One-time use items which changes the player's ColorState based on the color of the ColorSpace.
    """

    def __init__(self, color_state, image, x, y, *groups):
        super().__init__(*groups)
        self.color_state = color_state
        self.image = image
        self.rect.x, self.rect.y = x, y


class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f'img/player-{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 30))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead = pygame.image.load('img/dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.v_y = 0
        self.jumped = False
        self.direction = 0
        self.mid_air = False

    def update(self, game_over):
        d_x = 0
        d_y = 0
        walk_cooldown = 5

        if game_over == 0:
            # KEY PRESS CONTROLS
            keypress = pygame.key.get_pressed()
            if keypress[pygame.K_SPACE] and not self.mid_air:
                self.mid_air = True
                self.v_y = -15
            if keypress[pygame.K_SPACE] == False:
                self.jumped = False
            if keypress[pygame.K_LEFT]:
                d_x -= 5
                self.counter += 1
                self.direction = -1
            if keypress[pygame.K_RIGHT]:
                d_x += 5
                self.counter += 1
                self.direction = 1
            if keypress[pygame.K_LEFT] == False and keypress[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # ANIMATION
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # GRAVITY
            self.v_y += 1
            if self.v_y > 10:
                self.v_y = 10
            d_y += self.v_y

            # COLLISION
            for tile in level_one.tile_list:
                # X-DIR. COLLISION
                if tile[1].colliderect(self.rect.x + d_x, self.rect.y, self.width, self.height):
                    d_x = 0
                # Y-DIR. COLLISION
                if tile[1].colliderect(self.rect.x, self.rect.y + d_y, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.v_y < 0:
                        d_y = tile[1].bottom - self.rect.top
                        self.v_y = 0
                    # check if above the ground i.e. falling
                    elif self.v_y >= 0:
                        d_y = tile[1].top - self.rect.bottom
                        self.v_y = 0
                        self.mid_air = False

            # ENEMY COLLISION
            if pygame.sprite.spritecollide(self, enemy_grp, False):
                game_over = -1

            # LAVA COLLISION
            if pygame.sprite.spritecollide(self, lava_grp, False):
                game_over = -1

            # DOOR COLLISION
            if pygame.sprite.spritecollide(self, door_grp, False):
                game_over = 1

            # COORD UPDATES
            self.rect.x += d_x
            self.rect.y += d_y

        elif game_over == -1:
            self.image = self.dead

        # To draw player into game
        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        # ALIVE
        img = pygame.image.load('img/player-1.png')
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()

        # DEAD
        dead = pygame.image.load('img/dead.png')
        self.dead = pygame.transform.scale(dead, (30, 30))
        self.rect = self.image.get_rect()

        # POSITION
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.v_y = 0
        self.jumped = False
        self.direc = 0
        self.mid_air = True


class Level:

    def __init__(self, data):
        self.tile_list = []

        # img
        floor = pygame.image.load('img/ground.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    fire = Enemy(column_count * tile_size, row_count * tile_size - 30)
                    enemy_grp.add(fire)
                if tile == 3:
                    lava = Lava(column_count * tile_size, row_count * tile_size)
                    lava_grp.add(lava)
                if tile == 4:
                    door = Door(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    door_grp.add(door)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/fireball.png')
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_count = 0

    def update(self):
        self.rect.y += self.move_direction
        self.move_count += 1
        if self.move_count > 20:
            self.move_direction *= -1
            self.move_count *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# LEVEL DATA
current_level = Location.MAIN_MENU

level_one_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# CREATE GAME MOBS AND TYPE GROUPS
player = Player(100, screen_height - 130)
enemy_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
door_grp = pygame.sprite.Group()

# CREATE LEVELS
level_one = Level(level_one_data)

# CREATE LEVEL GROUPS
main_menu_grp = pygame.sprite.Group()
game_over_grp = pygame.sprite.Group()
level_list_grp = pygame.sprite.Group()

# CREATE BUTTONS
start_btn = Button(screen_height // 20, screen_height // 1.5, def_start_img, hov_start_img)
main_menu_exit_btn = Button(screen_height // 20, screen_height // 1.25, def_exit_img, hov_exit_img)
restart_btn = Button(screen_width // 2 - 90, screen_height // 2, def_start_img)
exit_btn = Button(screen_width // 2 + 10, screen_height // 2, def_exit_img)

# ADD ITEMS TO LEVEL GROUPS
main_menu_grp.add(start_btn, main_menu_exit_btn)
game_over_grp.add(restart_btn, exit_btn)

# GAME LOOP
Running = True
while Running:

    clock.tick(fps)
    screen.blit(bg_img, (0, 0))

    if current_level == Location.MAIN_MENU:
        main_menu_grp.draw(screen)

        if main_menu_exit_btn.is_clicked():
            Running = False
        elif start_btn.is_clicked():
            current_level = Location.LEVEL_ONE

        main_menu_grp.update()

    else:
        level_one.draw()

        if game_over == 0:
            enemy_grp.update()

        enemy_grp.draw(screen)
        lava_grp.draw(screen)
        door_grp.draw(screen)

        game_over = player.update(game_over)

        # LOSE
        if game_over == -1:
            game_over_grp.draw(screen)

            if restart_btn.is_clicked():
                player.reset(100, screen_height - 130)
                game_over = 0
            if exit_btn.is_clicked():
                current_level = Location.MAIN_MENU
                player.reset(100, screen_height - 130)
                game_over = 0

            game_over_grp.update()

        # WIN
        if game_over == 1:
            game_over_grp.draw(screen)

            if restart_btn.is_clicked():
                player.reset(100, screen_height - 130)
                game_over = 0
            if exit_btn.is_clicked():
                current_level = Location.MAIN_MENU
                player.reset(100, screen_height - 130)
                game_over = 0

            game_over_grp.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    pygame.display.update()
pygame.quit()
