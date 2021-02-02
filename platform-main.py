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
main_menu = True

# LOAD IMAGES
bg_img = pygame.image.load('img/bg_img.png')
restart_img = pygame.image.load('img/restart_button.png')
start_img = pygame.image.load('img/start_button.png')
exit_img = pygame.image.load('img/exit.png')

def display_txt(text, font, text_color, x,y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        mouse_act = False

        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # mouse over
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:      # 0 is for left-click
                mouse_act = True
                self.clicked = True

        # mouse click
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return mouse_act

class Player():
    def __init__(self, x,y):
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
            for tile in world.tile_list:
				# X-DIR. COLLISION
                if tile[1].colliderect(self.rect.x + d_x, self.rect.y, self.width, self.height):
                    d_x = 0
                # Y-DIR. COLLISION
                if tile[1].colliderect(self.rect.x, self.rect.y + d_y, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.v_y < 0:
                        d_y = tile[1].bottom - self.rect.top
                        self.v_y = 0
                    #check if above the ground i.e. falling
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

class World():
    def __init__(self, data):
        self.tile_list = []
 
        #img
        floor = pygame.image.load('img/ground.png')
        floor_2 = pygame.image.load('img/ground-corn.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    fire = Enemy(column_count*tile_size, row_count*tile_size - 30)
                    enemy_grp.add(fire)
                if tile == 3:
                    lava = Lava(column_count*tile_size, row_count*tile_size)
                    lava_grp.add(lava)
                if tile == 4:
                    door = Door(column_count*tile_size, row_count*tile_size - (tile_size // 2))
                    door_grp.add(door)
                if tile == 5:
                    img = pygame.transform.scale(floor_2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/fireball.png')
        self.image = pygame.transform.scale(img, (30,30))
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
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size,int(tile_size*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# WORLD DATA
world_data = [
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
[1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# CREATE GAME MOBS
player = Player(100, screen_height -130)

enemy_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
door_grp = pygame.sprite.Group()
world = World(world_data)

# CREATE BUTTONS
restart_btn = Button(screen_width // 2 - 90, screen_height // 2, restart_img)
start_btn = Button(screen_width // 2 - 75, screen_height // 2, start_img)
exit_btn = Button(screen_width // 2 + 10, screen_height // 2, exit_img)

# GAME LOOP
Running = True

while Running:

    clock.tick(fps)
    screen.blit(bg_img, (0,0))

    if main_menu == True:
        if exit_btn.draw():
            Running = False
        if start_btn.draw():
            main_menu = False
    
    else:
        world.draw()

        if game_over == 0:
            enemy_grp.update()
            
        enemy_grp.draw(screen)
        lava_grp.draw(screen)
        door_grp.draw(screen)

        game_over = player.update(game_over)

        # LOSE
        if game_over == -1:
            if restart_btn.draw():
                player.reset(100, screen_height -130)
                game_over = 0
            if exit_btn.draw():
                main_menu = True
                player.reset(100, screen_height -130)
                game_over = 0
        
        # WIN
        if game_over == 1:
            if restart_btn.draw():
                player.reset(100, screen_height -130)
                game_over = 0 
            if exit_btn.draw():
                main_menu = True
                player.reset(100, screen_height -130)
                game_over = 0
    
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            Running = False

    pygame.display.update()
pygame.quit()