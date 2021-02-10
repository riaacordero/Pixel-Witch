import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
fps = 60

# SET SCREEN
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Witch")

# GRID VARIABLES
tile_size = 30

# COLORS
black = (0, 0, 0)
dark_gray = (65, 64, 66)
light_gray = (209, 211, 212)
gray = (109, 110, 113)
purple = (179, 136, 255)

# FONT LOCATIONS
fff_forward_font = "font/FFF Forward.ttf"
retro_gaming_font = "font/Retro Gaming.ttf"

# BGM LOCATIONS
bgm_main_location = "music/bgm_main.wav"
bgm_level_location = "music/bgm_level.wav"

# Menu SFX
select_sfx = pygame.mixer.Sound('music/select1.wav')
cancel_sfx = pygame.mixer.Sound('music/select2.wav')
game_over_sfx = pygame.mixer.Sound('music/gameover.wav')
win_sfx = pygame.mixer.Sound('music/win.wav')

# In-game audio
jump_sfx = pygame.mixer.Sound('music/jump.wav')
potion_collect_sfx = pygame.mixer.Sound('music/collect1.wav')
gem_collect_sfx = pygame.mixer.Sound('music/collect2.wav')
key_collect_sfx = pygame.mixer.Sound('music/collect3.wav')
player_atk_sfx = pygame.mixer.Sound('music/attack.wav')

# LOAD IMAGES
bg_img = pygame.image.load('img/bg_img.png')
bg_game_over_img = pygame.image.load("img/bg_img.png")
bg_game_clear_img = pygame.image.load("img/bg_img.png")
bg_level_img = pygame.image.load("img/bg_img.png")

game_over_img = pygame.image.load("img/game_over.png")
death_img = pygame.image.load("img/dead.png")

enemy_img = pygame.image.load("img/enemy.png")
gem_img = pygame.transform.scale(pygame.image.load("img/gem.png"), (35, 35))
key_img = pygame.transform.scale(pygame.image.load("img/key.png"), (35, 35))
door_img = pygame.image.load("img/door.png")
platform_img = pygame.image.load("img/ground.png")
fireball_img = pygame.image.load("img/ball-atk.png")

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


class MusicPlayer:
    """
    Class for handling music in runtime.
    """
    def __init__(self):
        self.running = False
        self.paused = False

    def load_and_play(self, music_location, loops, fade_ms=0):
        if not self.running and not self.paused:
            pygame.mixer.music.load(music_location)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.running = True

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def stop_and_unload(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.running = False


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
        self.rect.x, self.rect.y = x, y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.image = self.hovered_image if self.is_hovered() else self.default_image

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed(3)[0]


class Text:
    """
    Text shown in screen. Has ability to detect hovers and clicks.
    """

    def __init__(self, x, y, text, font_location, font_size, default_text_color, pos="topleft"):
        self.text = text
        self.font = pygame.font.Font(font_location, font_size)
        self.default_text_color = default_text_color
        self.default_text = self.font.render(text, True, default_text_color)
        self.rect = self.default_text.get_rect()
        self.x, self.y = x, y
        if pos == "topleft":
            self.rect.x, self.rect.y = x, y
        elif pos == "center":
            self.rect.center = x, y
        self.width, self.height = self.default_text.get_width(), self.default_text.get_height()
        self.hovered = False

    def draw(self):
        screen.blit(self.default_text, self.rect)

    def update(self, new_text="", pos="", new_x=0, new_y=0):
        self.hovered = self.is_hovered()

        if not new_text == "":
            self.default_text = self.font.render(new_text, True, self.default_text_color)
            self.rect = self.default_text.get_rect()
            self.width, self.height = self.default_text.get_width(), self.default_text.get_height()
            self.rect.x, self.rect.y = self.x, self.y

            if pos == "" or pos == "topleft":
                self.rect.x, self.rect.y = self.x, self.y
            elif pos == "center":
                self.rect.center = new_x, new_y

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed(3)[0]


class HoverableText(Text):
    """
    Text that changes appearance when mouse is hovered on it.
    """

    def __init__(self, x, y, text, font_location, font_size, default_text_color, hovered_text_color, hovered_bg_color,
                 pos="topleft"):
        super().__init__(x, y, text, font_location, font_size, default_text_color, pos)
        self.hovered_text_color = hovered_text_color
        self.hovered_text = self.font.render(text, True, hovered_text_color)
        self.hovered_bg_color = hovered_bg_color

    def draw(self):
        if self.hovered:
            pygame.draw.rect(screen, self.hovered_bg_color, self.rect)
            screen.blit(self.hovered_text, self.rect)
        else:
            screen.blit(self.default_text, self.rect)

    def update(self, new_text="", pos="", new_x=0, new_y=0):
        super().update(new_text)
        if not new_text == "":
            self.hovered_text = self.font.render(new_text, True, self.hovered_text_color)


class TextGroup:
    """
    Container for Text and HoverableText objects.
    """

    def __init__(self, *texts: Text):
        self.texts = list(texts)

    def draw(self, *, excluded=()):
        for text in self.texts:
            if text not in excluded:
                text.draw()

    def update(self):
        for text in self.texts:
            text.update()

    def one_is_clicked(self):
        """Returns true if one interactive text is clicked"""
        return any(isinstance(text, HoverableText) and text.is_clicked() for text in self.texts)

    def add(self, *texts):
        self.texts.extend(list(texts))

    def remove(self, *texts):
        for text in texts:
            self.texts.remove(text)


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

    PAUSE = -2
    LEVEL_SELECTION = -1
    MAIN_MENU = 0
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
        super().__init__(gem_img, x, y, 20, 20, *groups)  # image is placeholder


class Key(LevelSprite):
    """
    Key to open door and finish the level.
    """

    def __init__(self, x, y, *groups):
        super().__init__(key_img, x, y, 20, 20, *groups)  # image is placeholder


class Enemy(LevelSprite):
    """
    Sprites that results to game over if collided with the player.
    """

    def __init__(self, x, y, *groups):
        super().__init__(enemy_img, x, y, 65, 65, *groups)
        self.move_direction = 1
        self.move_count = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_count += 1
        if self.move_count > 20:
            self.move_direction *= -1
            self.move_count *= -1


class Door(LevelSprite):
    """
    Sprites that finish the level if collided with the player.
    """

    def __init__(self, x, y, *groups):
        super().__init__(door_img, x, y, 48, 48, *groups)


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


class Fireball(LevelSprite):
    """
    A fireball attack casted by a player when pressing SPACE while in yellow color state.
    """

    def __init__(self, *groups):
        super().__init__(fireball_img, 0, 0, 10, 10, *groups)
        self.attacking = False
        self.move_speed = 5
        self.direction = 0

    def attack(self, level):
        x_movement = self.direction * self.move_speed
        self.rect.x += x_movement

        # Platform collision
        for platform in level.platforms:
            if platform.rect.colliderect(self.rect) and platform in level.active_sprites:
                self.attacking = False
                return

        # Enemy collision
        for enemy in level.enemies:
            if enemy.rect.colliderect(self.rect) and enemy in level.active_sprites:
                self.attacking = False
                level.active_sprites.remove(enemy)
                return


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

        # STATE
        self.current_level = None
        self.has_key = False
        self.color_state = ColorState.WHITE
        self.player_state = PlayerState.ALIVE

        # MOVEMENT
        self.y_vel = 0
        self.jump_cooldown = 0
        self.direction = 1
        self.on_ground = True

        # ABILITY
        self.jump_cooldown = 0
        self.atk_cooldown = 0
        self.fireball = Fireball()
        self.has_shield = False

    def update(self):
        if self.player_state == PlayerState.ALIVE:
            self._refresh_cooldown()
            self._update_fireball()
            x_movement, y_movement = self._move()
            self._animate()
            y_movement = self._gravitate(y_movement)
            x_movement, y_movement, self.player_state = self._collide(x_movement, y_movement)

            # COORD UPDATES
            self.rect.x += x_movement
            self.rect.y += y_movement

    def _refresh_cooldown(self):
        if self.on_ground and self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1

    def _update_fireball(self):
        if self.fireball.attacking:
            self.current_level.active_sprites.add(self.fireball)
            self.fireball.attack(self.current_level)
        else:
            self.current_level.active_sprites.remove(self.fireball)
            self.fireball.rect.x, self.fireball.rect.y = self.rect.x + 15, self.rect.y + 10

    def _move(self):
        """
        Moves player based on certain key presses.
        :return: tuple representing x and y movement
        """

        x_movement, y_movement = 0, 0
        keypress = pygame.key.get_pressed()
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
        if keypress[K_SPACE]:
            if self.color_state == ColorState.BLUE and self.on_ground and self.jump_cooldown == 0:
                self.jump_cooldown = fps // 5  # 0.20 second cooldown
                self.on_ground = False
                self.y_vel = -20
                jump_sfx.play()
            elif self.color_state == ColorState.YELLOW and self.atk_cooldown == 0 and not self.fireball.attacking \
                    and self.fireball.rect.x == self.rect.x + 15 and self.fireball.rect.y == self.rect.y + 10:
                self.atk_cooldown = fps  # 1 second cooldown
                self.fireball.attacking = True
                self.fireball.direction = self.direction
                pass

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
                game_over_sfx.play()

        # DOOR COLLISION
        if self.current_level.door.rect.colliderect(self.rect) and self.has_key:
            player_state = PlayerState.WON
            win_sfx.play()

        # CONSUMABLE COLLISION
        for consumable in self.current_level.consumables:
            if consumable.rect.colliderect(self.rect) and consumable in self.current_level.active_sprites:
                if isinstance(consumable, BluePotion):
                    print("BLUE")
                    player.color_state = ColorState.BLUE
                    potion_collect_sfx.play()
                if isinstance(consumable, RedPotion):
                    print("RED")
                    player.color_state = ColorState.RED
                    potion_collect_sfx.play()
                if isinstance(consumable, YellowPotion):
                    print("YELLOW")
                    player.color_state = ColorState.YELLOW
                    potion_collect_sfx.play()
                if isinstance(consumable, Gem):
                    self.current_level.score += 5
                    gem_collect_sfx.play()
                if isinstance(consumable, Key):
                    self.has_key = True
                    key_collect_sfx.play()
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

        # STATE
        self.current_level = level
        self.has_key = False
        self.color_state = ColorState.WHITE
        self.player_state = PlayerState.ALIVE

        # MOVEMENT
        self.y_vel = 0
        self.direction = 1
        self.on_ground = True

        # ABILITY
        self.jump_cooldown = 0
        self.atk_cooldown = 0
        self.has_shield = False


level_one_data = [
    "PPPPPPPPPPPPPPPPPPPP",
    "P------------------P",
    "P------------------P",
    "P------------------P",
    "P-----D------------P",
    "P----PPPPPPP-------P",
    "P------------------P",
    "P------------PP----P",
    "PP--------E--------P",
    "P------------------P",
    "P------------------P",
    "P--GKB-E-KG------P-P",
    "P--PPPPPPPPPP------P",
    "P------------------P",
    "P-----------------PP",
    "P---------------PPPP",
    "P-------------PPPPPP",
    "P----YRB---E-------P",
    "PPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPP"
]

# CREATE BUTTONS
pause_btn = Button(400, 0, potion_blue_img, potion_red_img)

# CREATE TEXTS
main_start_text = HoverableText(25, 335, "start", retro_gaming_font, 40, dark_gray, light_gray, gray)
main_exit_text = HoverableText(25, 400, "exit", retro_gaming_font, 40, dark_gray, light_gray, gray)

level_selection_text = Text(150, 150, "LEVEL SELECTION", fff_forward_font, 40, black)

over_text = Text(125, 300, "GAME OVER", fff_forward_font, 32, black)
over_restart_text = HoverableText(190, 385, "restart", retro_gaming_font, 24, dark_gray, light_gray, gray)
over_main_text = HoverableText(175, 420, "main menu", retro_gaming_font, 24, dark_gray, light_gray, gray)

clear_score_text = Text(250, 125, "0", fff_forward_font, 80, black, pos="center")
clear_text = Text(250, 210, "GAME CLEARED", fff_forward_font, 24, black, pos="center")
clear_next_text = HoverableText(250, 320, "next", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")
clear_retry_text = HoverableText(250, 360, "retry", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")
clear_main_text = HoverableText(250, 400, "main menu", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")

pause_resume_text = HoverableText(250, 225, "resume", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")
pause_main_text = HoverableText(250, 275, "main menu", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")

score_text = Text(100, 10, "0", retro_gaming_font, 28, purple)

# CREATE TEXT GROUPS
main_menu_texts = TextGroup(main_start_text, main_exit_text)
game_over_texts = TextGroup(over_text, over_restart_text, over_main_text)
game_clear_texts = TextGroup(clear_text, clear_next_text, clear_retry_text, clear_main_text, clear_score_text)
pause_texts = TextGroup(pause_resume_text, pause_main_text)

# CREATE PLAYER
player = Player()

# CREATE LEVELS
level_one = Level(level_one_data, player)

# PLAYER STATE
current_player_state = PlayerState.ALIVE
player.reset(100, screen_height - 120, level_one)

# GAME STATE
music_player = MusicPlayer()
Running = True
paused = False
pause_cooldown = 0

score_display = 0
"""score to be displayed, which starts at 0 and ends with the total score"""
score_display_cooldown = fps // 2
"""waits for score_display_cooldown to be zero before score_display is shown"""
score_display_speed = fps // 10
"""changes score_display for every 1/score_display_speed seconds"""

current_location = Location.MAIN_MENU


def display_main_menu():
    global Running, current_location, current_player_state

    music_player.load_and_play(bgm_main_location, loops=-1, fade_ms=3000)
    screen.blit(bg_img, (0, 0))
    main_menu_texts.update()
    main_menu_texts.draw()

    if main_exit_text.is_clicked():
        Running = False
    elif main_start_text.is_clicked():
        music_player.stop_and_unload()
        current_location = Location.LEVEL_ONE
        level_one.reset()
        player.reset(100, screen_height - 130, level_one)
        current_player_state = player.player_state
        select_sfx.play()


def display_pause():
    global paused, pause_cooldown, current_location

    screen.blit(bg_img, (0, 0))
    pause_texts.update()
    pause_texts.draw()

    if pause_texts.one_is_clicked():
        music_player.unpause()

    if pause_resume_text.is_clicked():
        paused = False
    if pause_main_text.is_clicked():
        music_player.stop_and_unload()
        paused = False
        current_location = Location.MAIN_MENU


def display_game_over(level: Level):
    global current_player_state, current_location

    screen.blit(bg_game_over_img, (0, 0))
    screen.blit(pygame.transform.scale(death_img, (200, 200)), (150, 50))
    game_over_texts.update()
    game_over_texts.draw()

    if over_restart_text.is_clicked():
        level.reset()
        player.reset(100, screen_height - 130, level)
        current_player_state = player.player_state
    elif over_main_text.is_clicked():
        current_location = Location.MAIN_MENU


def display_game_clear(level: Level):
    global current_player_state, current_location, score_display, score_display_cooldown, score_display_speed

    screen.blit(bg_game_clear_img, (0, 0))
    if score_display_cooldown > 0:
        score_display_cooldown -= 1
    if score_display_speed > 0:
        score_display_speed -= 1
    if score_display_cooldown == 0 and score_display_speed == 0 and score_display != level.score:
        score_display_speed = fps // 10
        score_display += 1
    game_clear_texts.update()
    clear_score_text.update(str(score_display), pos="center", new_x=250, new_y=125)
    game_clear_texts.draw(excluded=() if score_display == level.score else (clear_text,))

    if game_clear_texts.one_is_clicked():
        print(game_clear_texts.texts)
        score_display = 0
        score_display_cooldown = fps // 2
        score_display_speed = fps // 10

    if clear_next_text.is_clicked():
        pass
    elif clear_retry_text.is_clicked():
        level.reset()
        player.reset(100, screen_height - 130, level)
        current_player_state = player.player_state
    elif clear_main_text.is_clicked():
        current_location = Location.MAIN_MENU


def display_level(level: Level):
    global current_player_state, paused, score_display

    music_player.load_and_play(bgm_level_location, loops=-1, fade_ms=3000)
    if not paused:
        level.update()
        current_player_state = player.player_state
        level.draw()
        screen.blit(key_img if player.has_key else key_img, (10, 10))
        screen.blit(gem_img, (55, 10))
        score_text.draw()
        score_text.update(str(level.score))

    pause_btn.update()
    pause_btn.draw()
    if pause_btn.is_clicked() and not paused:
        music_player.pause()
        paused = True
        cancel_sfx.play()
    if paused:
        display_pause()

    if current_player_state == PlayerState.LOST:
        music_player.stop_and_unload()
        display_game_over(level)
    elif current_player_state == PlayerState.WON:
        music_player.stop_and_unload()
        display_game_clear(level)


# GAME LOOP
if __name__ == "__main__":
    while Running:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                Running = False

        if current_location == Location.MAIN_MENU:
            display_main_menu()
        elif current_location == Location.LEVEL_ONE:
            display_level(level_one)

        pygame.display.update()
    pygame.quit()
