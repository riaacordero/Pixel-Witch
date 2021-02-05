import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fps = 60

# SET SCREEN
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Witch")

# GRID VARIABLES
tile_size = 30

# LOAD IMAGES
bg_img = pygame.image.load('img/bg_img.png')
bg_game_over_img = pygame.image.load("img/bg_img.png")
bg_level_img = pygame.image.load("img/bg_img.png")

def_start_img = pygame.image.load("img/default_start_btn.png")
hov_start_img = pygame.image.load("img/hovered_start_btn.png")
def_exit_img = pygame.image.load("img/default_exit_btn.png")
hov_exit_img = pygame.image.load("img/hovered_exit_btn.png")
def_restart_img = pygame.image.load("img/default_restart_btn.png")
hov_restart_img = pygame.image.load("img/hovered_restart_btn.png")
def_return_img = pygame.image.load("img/default_return_btn.png")
hov_return_img = pygame.image.load("img/hovered_return_btn.png")
game_over_img = pygame.image.load("img/game_over.png")
death_img = pygame.image.load("img/dead.png")

enemy_img = pygame.image.load("img/fireball.png")
door_img = pygame.image.load("img/door.png")
platform_img = pygame.image.load("img/ground.png")

potion_blue_img = pygame.image.load("img/potion-blue.png")
potion_red_img = pygame.image.load("img/potion-red.png")
potion_yellow_img = pygame.image.load("img/potion-yellow.png")

player_default_left_images = []
player_default_right_images = []
player_atk_left_images = []
player_atk_right_images = []
player_health_left_images = []
player_health_right_images = []
player_jump_left_images = []
player_jump_right_images = []

player_size = (40, 40)
for num in range(1, 4):
    player_img = pygame.image.load(f"img/player-{num}.png")
    player_right_img = pygame.transform.scale(player_img, player_size)
    player_left_img = pygame.transform.flip(player_right_img, True, False)
    player_default_right_images.append(player_right_img)
    player_default_left_images.append(player_left_img)

    player_atk_img = pygame.image.load(f"img/player-state/player-atk-{num}.png")
    player_atk_right_img = pygame.transform.scale(player_atk_img, player_size)
    player_atk_left_img = pygame.transform.flip(player_atk_right_img, True, False)
    player_atk_right_images.append(player_atk_right_img)
    player_atk_left_images.append(player_atk_left_img)

    player_health_img = pygame.image.load(f"img/player-state/player-health-{num}.png")
    player_health_right_img = pygame.transform.scale(player_health_img, player_size)
    player_health_left_img = pygame.transform.flip(player_health_right_img, True, False)
    player_health_right_images.append(player_health_right_img)
    player_health_left_images.append(player_health_left_img)

    player_jump_img = pygame.image.load(f"img/player-state/player-jump-{num}.png")
    player_jump_right_img = pygame.transform.scale(player_jump_img, player_size)
    player_jump_left_img = pygame.transform.flip(player_jump_right_img, True, False)
    player_jump_left_images.append(player_jump_left_img)
    player_jump_right_images.append(player_jump_right_img)


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


class PlayerState:
    """
    Current state of the player in the game.
    """

    ALIVE = 0
    LOST = -1
    WON = 1


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
    State of the player based on the ColorSpace they are in. Except the default value WHITE,
    each ColorState gives the player a unique ability, accessible by pressing SPACE.
    """

    WHITE = 0

    RED = 1
    """Horizontal projectile attack based on what side the player is facing"""

    BLUE = 2
    """Jump"""

    YELLOW = 3
    """One-time use shield"""


class LevelSprite(pygame.sprite.Sprite):
    """
    All the sprites seen in a single level.
    """

    def __init__(self, image, x, y, width, height, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class Background(LevelSprite):
    """
    Moving background in a single level.
    """

    def __init__(self, width, height, *groups):
        super().__init__(bg_level_img, 0, 0, width, height, *groups)


class Platform(LevelSprite):
    """
    Wall, floor, or obstacles that are able to collide with the player.
    """

    def __init__(self, x, y, *groups):
        super().__init__(platform_img, x, y, tile_size, tile_size, *groups)


class Potion(LevelSprite):
    """
    One-time use items which changes the player's ColorState based on its color.
    """

    def __init__(self, color_state, image, x, y, *groups):
        super().__init__(image, x, y, tile_size, tile_size, *groups)
        self.color_state = color_state


class BluePotion(Potion):
    """
    Potion that gives the player the ability to jump.
    """

    def __init__(self, x, y, *groups):
        super().__init__(ColorState.BLUE, potion_blue_img, x, y, *groups)


class RedPotion(Potion):
    """
    Potion that gives the player the ability to attack.
    """

    def __init__(self, x, y, *groups):
        super().__init__(ColorState.RED, potion_red_img, x, y, *groups)


class YellowPotion(Potion):
    """
    Potion that gives the player a shield.
    """

    def __init__(self, x, y, *groups):
        super().__init__(ColorState.YELLOW, potion_yellow_img, x, y, *groups)


class Gem(LevelSprite):
    """
    Gems that the player collects to gain points.
    """

    def __init__(self, x, y, *groups):
        super().__init__(enemy_img, x, y, 20, 20, *groups)  # image is placeholder


class Key(LevelSprite):
    """
    Key to open door and finish the level.
    """

    def __init__(self, x, y, *groups):
        super().__init__(enemy_img, x, y, 20, 20, *groups)  # image is placeholder


class Enemy(LevelSprite):
    """
    Sprites that results to game over if collided with the player.
    """

    def __init__(self, x, y, *groups):
        super().__init__(enemy_img, x, y, 30, 30, *groups)
        self.move_direction = 1
        self.move_count = 0

    def update(self):
        self.rect.y += self.move_direction
        self.move_count += 1
        if self.move_count > 20:
            self.move_direction *= -1
            self.move_count *= -1

class Door(LevelSprite):
    """
    Sprites that finish the level if collided with the player.
    """

    def __init__(self, x, y, *groups):
        super().__init__(door_img, x, y, tile_size, int(tile_size * 1.5), *groups)


class Level:
    """
    The stage that comprises of the different sprites that can interact with the player.
    """

    def __init__(self, data: list, target: pygame.sprite.Sprite):
        self.target = target
        self.width, self.height = len(data[0]) * tile_size, len(data) * tile_size
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.background = Background(self.width, self.height)

        self.score = 0
        """Score gained by the player by getting gems"""

        # LEVEL GROUPS
        self.platforms = pygame.sprite.Group()
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
                if tile == "P":
                    Platform(column_count * tile_size, row_count * tile_size, self.platforms, self.sprites)
                elif tile == "E":
                    Enemy(column_count * tile_size, row_count * tile_size - 30, self.enemies, self.sprites)
                elif tile == "D":
                    self.door = Door(column_count * tile_size, row_count * tile_size - (tile_size // 2), self.sprites)
                elif tile == "B":
                    BluePotion(column_count * tile_size, row_count * tile_size, self.consumables, self.sprites)
                elif tile == "R":
                    RedPotion(column_count * tile_size, row_count * tile_size, self.consumables, self.sprites)
                elif tile == "Y":
                    YellowPotion(column_count * tile_size, row_count * tile_size, self.consumables, self.sprites)
                elif tile == "G":
                    Gem(column_count * tile_size, row_count * tile_size, self.consumables, self.sprites)
                elif tile == "K":
                    Key(column_count * tile_size, row_count * tile_size, self.consumables, self.sprites)
                column_count += 1
            row_count += 1

    def draw(self):
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


class Player(pygame.sprite.Sprite):
    """
    The sprite being controlled by the user.
    """

    def __init__(self, *groups):
        super().__init__(*groups)
        # ANIMATION
        self.index = 0
        self.counter = 0
        self.image = player_default_right_images[self.index]

        # DISPLAY
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.width, self.height = self.image.get_width(), self.image.get_height()

        # MOVEMENT
        self.y_vel = 0
        self.jump_cooldown = 0
        self.direction = 0
        self.on_ground = True

        # STATE
        self.current_level = None
        self.has_key = False
        self.color_state = ColorState.WHITE
        self.player_state = PlayerState.ALIVE

    def update(self):
        if self.player_state == PlayerState.ALIVE:
            x_movement, y_movement = self._move()
            self._animate()
            y_movement = self._gravitate(y_movement)
            x_movement, y_movement, self.player_state = self._collide(x_movement, y_movement)

            # COORD UPDATES
            self.rect.x += x_movement
            self.rect.y += y_movement

        # To draw player into game
        screen.blit(self.image, self.rect)

    def _move(self):
        """
        Moves player based on certain key presses.
        :return: tuple representing x and y movement
        """
        x_movement, y_movement = 0, 0
        keypress = pygame.key.get_pressed()
        if self.on_ground and self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if keypress[K_SPACE] and self.on_ground and self.jump_cooldown == 0:
            self.jump_cooldown = fps // 5  # 0.20 second cooldown
            self.on_ground = False
            self.y_vel = -20
        if keypress[K_LEFT] and not keypress[K_RIGHT]:
            x_movement -= 5
            self.counter += 1
            self.direction = -1
        if keypress[K_RIGHT] and not keypress[K_LEFT]:
            x_movement += 5
            self.counter += 1
            self.direction = 1
        if not keypress[K_LEFT] and not keypress[K_RIGHT]:
            self.counter = 0
            self.index = 0
            self._display_frame()

        return x_movement, y_movement

    def _animate(self):
        walk_cooldown = 5
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(player_default_right_images):
                self.index = 0
            self._display_frame()

    def _gravitate(self, y_movement):
        self.y_vel += 1
        if self.y_vel > 10:
            self.y_vel = 10
        y_movement += self.y_vel
        return y_movement

    def _collide(self, x_movement, y_movement):
        """
        Applies collision with player and other level sprites.
        :return: tuple representing x and y movement and player state
        """
        player_state = PlayerState.ALIVE

        for platform in self.current_level.platforms:
            # X-DIR. COLLISION
            if platform.rect.colliderect(self.rect.x + x_movement, self.rect.y, self.width, self.height):
                x_movement = 0
            # Y-DIR. COLLISION
            if platform.rect.colliderect(self.rect.x, self.rect.y + y_movement, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.y_vel < 0:
                    y_movement = platform.rect.bottom - self.rect.top
                    self.y_vel = 0
                # check if above the ground i.e. falling
                elif self.y_vel >= 0:
                    y_movement = platform.rect.top - self.rect.bottom
                    self.y_vel = 0
                    self.on_ground = True

        # ENEMY COLLISION
        for enemy in self.current_level.enemies:
            if enemy.rect.colliderect(self.rect) and enemy in self.current_level.active_sprites:
                player_state = PlayerState.LOST

        # DOOR COLLISION
        if self.current_level.door.rect.colliderect(self.rect) and self.has_key:
            player_state = PlayerState.WON

        # CONSUMABLE COLLISION
        for consumable in self.current_level.consumables:
            if consumable.rect.colliderect(self.rect) and consumable in self.current_level.active_sprites:
                if isinstance(consumable, BluePotion):
                    print("BLUE")
                    player.color_state = ColorState.BLUE
                if isinstance(consumable, RedPotion):
                    print("RED")
                    player.color_state = ColorState.RED
                if isinstance(consumable, YellowPotion):
                    print("YELLOW")
                    player.color_state = ColorState.YELLOW
                if isinstance(consumable, Gem):
                    self.current_level.score += 5
                if isinstance(consumable, Key):
                    self.has_key = True
                self.current_level.active_sprites.remove(consumable)

        return x_movement, y_movement, player_state

    def _display_frame(self):
        if self.direction == 1:
            if self.color_state == ColorState.WHITE:
                self.image = player_default_right_images[self.index]
            elif self.color_state == ColorState.BLUE:
                self.image = player_jump_right_images[self.index]
            elif self.color_state == ColorState.RED:
                self.image = player_health_right_images[self.index]
            elif self.color_state == ColorState.YELLOW:
                self.image = player_atk_right_images[self.index]
        if self.direction == -1:
            if self.color_state == ColorState.WHITE:
                self.image = player_default_left_images[self.index]
            elif self.color_state == ColorState.BLUE:
                self.image = player_jump_left_images[self.index]
            elif self.color_state == ColorState.RED:
                self.image = player_health_left_images[self.index]
            elif self.color_state == ColorState.YELLOW:
                self.image = player_atk_left_images[self.index]

    def reset(self, x, y, level: Level):
        # ANIMATION AND DISPLAY
        self.image = player_default_right_images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # MOVEMENT
        self.y_vel = 0
        self.direction = 0
        self.on_ground = True
        self.jump_cooldown = 0

        # STATE
        self.current_level = level
        self.has_key = False
        self.color_state = ColorState.WHITE
        self.player_state = PlayerState.ALIVE


level_one_data = [
    "PPPPPPPPPPPPPPPPPPPP",
    "P------------------P",
    "P------------------P",
    "P------------------P",
    "P-----D------------P",
    "P----PPPPPPP-------P",
    "P------------------P",
    "P------------PP----P",
    "P---------E--------P",
    "P------------------P",
    "P------------------P",
    "P------E-KG------P-P",
    "P--PPPPPPPPPP------P",
    "P------------------P",
    "P-----------------PP",
    "P---------------PPPP",
    "P-------------PPPPPP",
    "P-----BRY----------P",
    "PPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPP"
]

# CREATE PLAYER
player = Player()

# CREATE LEVELS
level_one = Level(level_one_data, player)

# CREATE LEVEL GROUPS
main_menu_grp = pygame.sprite.Group()
game_over_grp = pygame.sprite.Group()
level_list_grp = pygame.sprite.Group()

# CREATE BUTTONS
start_btn = Button(25, 335, def_start_img, hov_start_img)
main_menu_exit_btn = Button(25, 400, def_exit_img, hov_exit_img)
game_over_restart_btn = Button(80, 400, def_restart_img, hov_restart_img)
game_over_return_btn = Button(285, 400, def_return_img, hov_return_img)


# ADD ITEMS TO LEVEL GROUPS
main_menu_grp.add(start_btn, main_menu_exit_btn)
game_over_grp.add(game_over_restart_btn, game_over_return_btn)

# PLAYER STATE
current_player_state = PlayerState.ALIVE
player.reset(100, screen_height - 120, level_one)

# GAME STATE
Running = True
current_location = Location.MAIN_MENU


def display_main_menu():
    global Running, current_location, current_player_state

    screen.blit(bg_img, (0, 0))
    main_menu_grp.draw(screen)
    main_menu_grp.update()

    if main_menu_exit_btn.is_clicked():
        Running = False
    elif start_btn.is_clicked():
        current_location = Location.LEVEL_ONE
        level_one.reset()
        player.reset(100, screen_height - 130, level_one)
        current_player_state = player.player_state


def display_game_over(level: Level):
    global current_player_state, current_location

    screen.blit(bg_game_over_img, (0, 0))
    screen.blit(pygame.transform.scale(death_img, (200, 200)), (150, 50))
    screen.blit(game_over_img, (100, 325))
    game_over_grp.draw(screen)

    if game_over_restart_btn.is_clicked():
        level.reset()
        player.reset(100, screen_height - 130, level)
        current_player_state = player.player_state
    elif game_over_return_btn.is_clicked():
        current_location = Location.MAIN_MENU
    game_over_grp.update()


def display_level(level: Level):
    global current_player_state
    level.update()
    level.draw()
    current_player_state = player.player_state

    if current_player_state == PlayerState.LOST:
        display_game_over(level)
    elif current_player_state == PlayerState.WON:
        display_game_over(level)


# GAME LOOP
if __name__ == "__main__":
    while Running:

        clock.tick(fps)

        if current_location == Location.MAIN_MENU:
            display_main_menu()
        elif current_location == Location.LEVEL_ONE:
            display_level(level_one)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False

        pygame.display.update()
    pygame.quit()
