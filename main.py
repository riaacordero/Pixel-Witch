"""
This module contains the game loop. It initializes, displays, and makes use of objects from the classes of
other modules. It contains functions that display each of the separate locations of the game, and a few variables that
help the functions and/or identify the current game state.
"""

from pygame.locals import *
from text import *
from level import *
from button import Button

pygame.init()
clock = pygame.time.Clock()

# Set screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Witch")

# Set music player
music_player = MusicPlayer()

# Create buttons
pause_btn = Button(450, 10, pause_img, pause_hov_img)

# Create texts
main_title_text = Text(25, 120, "PIXEL WITCH", fff_forward_font, 45, black)
main_start_text = HoverableText(25, 290, "start", retro_gaming_font, 40, dark_gray, light_gray, gray)
main_howto_text = HoverableText(25, 345, "how-to", retro_gaming_font, 40, dark_gray, light_gray, gray)
main_exit_text = HoverableText(25, 400, "exit", retro_gaming_font, 40, dark_gray, light_gray, gray)

howto_back_text = HoverableText(15, 15, "BACK", retro_gaming_font, 28, dark_gray, light_gray, gray)
howto_one_text = HoverableText(125, 450, "1", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")
howto_two_text = HoverableText(175, 450, "2", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")
howto_three_text = HoverableText(225, 450, "3", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")
howto_four_text = HoverableText(275, 450, "4", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")
howto_five_text = HoverableText(325, 450, "5", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")
howto_six_text = HoverableText(375, 450, "6", retro_gaming_font, 28, dark_gray, light_gray, gray, pos="center")

selection_back_text = HoverableText(390, 15, "BACK", retro_gaming_font, 28, dark_gray, light_gray, gray)
selection_one_text = HoverableText(75, 125, "1", fff_forward_font, 28, dark_gray, light_gray, gray)
selection_two_text = HoverableText(125, 125, "2", fff_forward_font, 28, dark_gray, light_gray, gray)
selection_three_text = HoverableText(175, 125, "3", fff_forward_font, 28, dark_gray, light_gray, gray)
selection_four_text = HoverableText(225, 125, "4", fff_forward_font, 28, dark_gray, light_gray, gray)
selection_five_text = HoverableText(275, 125, "5", fff_forward_font, 28, dark_gray, light_gray, gray)

over_text = Text(125, 300, "GAME OVER", fff_forward_font, 32, black)
over_restart_text = HoverableText(190, 385, "restart", retro_gaming_font, 24, dark_gray, light_gray, gray)
over_main_text = HoverableText(175, 420, "main menu", retro_gaming_font, 24, dark_gray, light_gray, gray)

clear_score_text = Text(250, 125, "0", fff_forward_font, 80, black, pos="center")
clear_text = Text(250, 210, "GAME CLEARED", fff_forward_font, 24, black, pos="center")
clear_next_text = HoverableText(250, 320, "next", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")
clear_restart_text = HoverableText(250, 360, "restart", retro_gaming_font, 32, dark_gray, light_gray, gray,
                                   pos="center")
clear_main_text = HoverableText(250, 400, "main menu", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")

pause_resume_text = HoverableText(250, 200, "resume", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")
pause_restart_text = HoverableText(250, 250, "restart", retro_gaming_font, 32, dark_gray, light_gray, gray,
                                   pos="center")
pause_main_text = HoverableText(250, 300, "main menu", retro_gaming_font, 32, dark_gray, light_gray, gray, pos="center")

score_text = Text(100, 10, "0", retro_gaming_font, 28, purple)

# Create text subgroups
howto_number_texts = [howto_one_text, howto_two_text, howto_three_text, howto_four_text, howto_five_text,
                      howto_six_text]

# Create text groups
main_menu_texts = TextGroup(main_title_text, main_start_text, main_exit_text, main_howto_text)
how_to_texts = TextGroup(howto_back_text, howto_one_text, howto_two_text, howto_three_text, howto_four_text,
                         howto_five_text, howto_six_text)
level_selection_texts = TextGroup(selection_back_text, selection_one_text, selection_two_text, selection_three_text,
                                  selection_four_text, selection_five_text)
game_over_texts = TextGroup(over_text, over_restart_text, over_main_text)
game_clear_texts = TextGroup(clear_text, clear_next_text, clear_restart_text, clear_main_text, clear_score_text)
pause_texts = TextGroup(pause_resume_text, pause_restart_text, pause_main_text)

# How-to current image
howto_index = 0

# Create player
player = Player()

# Create levels
level_one = Level(level_one_data, player, 1, selection_one_text)
level_two = Level(level_two_data, player, 2, selection_two_text)
level_three = Level(level_three_data, player, 3, selection_three_text)
level_four = Level(level_four_data, player, 4, selection_four_text)
level_five = Level(level_five_data, player, 5, selection_five_text)

# Create level list
levels = (level_one, level_two, level_three, level_four, level_five)

# Player state
current_player_state = PlayerState.ALIVE

# Game state
running = True
paused = False
pause_cooldown = 0

# Score display helper variables
score_display = 0
"""score to be displayed, which starts at 0 and ends with the total score"""
score_display_cooldown = fps // 2
"""waits for score_display_cooldown to be zero before score_display is shown"""
score_display_speed = fps // 15
"""changes score_display for every 1/score_display_speed seconds"""

# Locations
current_location = Location.MAIN_MENU
"""Location currently shown in screen"""
from_start_or_main = False
"""True if the previous location is either the main menu or level selection screen"""


def display_main_menu():
    global running, current_location, from_start_or_main, current_player_state

    if not from_start_or_main:
        music_player.load_and_play(bgm_main_location, loops=-1, fade_ms=3000)
        
    screen.blit(bg_img, (0, 0))
    main_menu_texts.update()
    main_menu_texts.draw(screen)

    if main_exit_text.is_clicked():
        running = False
    elif main_howto_text.is_clicked():
        current_location = Location.HOW_TO
    elif main_start_text.is_clicked():
        from_start_or_main = True
        current_location = Location.LEVEL_SELECTION


def display_how_to():
    global howto_index, running, current_location

    screen.blit(bg_img, (0, 0))
    screen.blit(howto_images[howto_index], (0, 75))
    how_to_texts.update()
    how_to_texts.draw(screen)

    if howto_back_text.is_clicked():
        current_location = Location.MAIN_MENU
    for i in range(len(howto_number_texts)):
        if howto_number_texts[i].is_clicked():
            howto_index = i
            break


def display_level_select():
    global current_location, from_start_or_main, current_player_state

    if not from_start_or_main:
        music_player.load_and_play(bgm_main_location, loops=-1, fade_ms=3000)
    screen.blit(bg_img, (0, 0))
    level_selection_texts.update()
    level_selection_texts.draw(screen)

    if level_selection_texts.one_is_clicked():
        from_start_or_main = True

    if selection_back_text.is_clicked():
        current_location = Location.MAIN_MENU
    for level in levels:
        if level.button.is_clicked():
            music_player.stop_and_unload()
            select_sfx.play()
            level.reset()
            current_player_state = player.player_state
            current_location = level.number
            break


def display_pause(level: Level):
    global paused, pause_cooldown, current_location, from_start_or_main, current_player_state

    screen.blit(bg_img, (0, 0))
    pause_texts.update()
    pause_texts.draw(screen)

    if pause_texts.one_is_clicked():
        music_player.unpause()
        select_sfx.play()
        paused = False

    if pause_restart_text.is_clicked():
        music_player.stop_and_unload()
        level.reset()
        current_player_state = player.player_state
    if pause_main_text.is_clicked():
        music_player.stop_and_unload()
        from_start_or_main = False
        current_location = Location.MAIN_MENU


def display_game_over(level: Level):
    global current_player_state, current_location, from_start_or_main

    screen.blit(bg_game_over_img, (0, 0))
    screen.blit(pygame.transform.scale(death_img, (200, 200)), (150, 50))
    game_over_texts.update()
    game_over_texts.draw(screen)

    if game_over_texts.one_is_clicked():
        select_sfx.play()

    if over_restart_text.is_clicked():
        level.reset()
        current_player_state = player.player_state
    elif over_main_text.is_clicked():
        from_start_or_main = False
        current_location = Location.MAIN_MENU


def display_game_clear(level: Level):
    global current_player_state, current_location, from_start_or_main, \
        score_display, score_display_cooldown, score_display_speed

    screen.blit(bg_game_clear_img, (0, 0))
    if score_display_cooldown > 0:
        score_display_cooldown -= 1
    if score_display_speed > 0:
        score_display_speed -= 1
    if score_display_cooldown == 0 and score_display_speed == 0 and score_display != level.score:
        score_display_speed = fps // 15
        score_display += 1
        select_sfx.play()
    game_clear_texts.update()
    clear_score_text.update(str(score_display), pos="center", new_x=250, new_y=125)
    game_clear_texts.draw(screen, excluded=() if score_display == level.score else (clear_text,))

    if game_clear_texts.one_is_clicked():
        score_display = 0
        score_display_cooldown = fps // 2
        score_display_speed = fps // 15
        select_sfx.play()

    if clear_next_text.is_clicked():
        if level.number >= len(levels):
            from_start_or_main = False
            current_location = Location.MAIN_MENU
        else:
            levels[level.number].reset()
            current_player_state = player.player_state
            current_location += 1
    elif clear_restart_text.is_clicked():
        level.reset()
        current_player_state = player.player_state
    elif clear_main_text.is_clicked():
        from_start_or_main = False
        current_location = Location.MAIN_MENU


def display_level(level: Level):
    global current_player_state, paused, score_display

    music_player.load_and_play(bgm_level_location, loops=-1, fade_ms=3000)
    if not paused:
        level.update()
        current_player_state = player.player_state
        level.draw(screen)
        screen.blit(key_img if player.has_key else key_inactive, (10, 10))
        screen.blit(gem_img, (55, 10))
        score_text.draw(screen)
        score_text.update(str(level.score))

    pause_btn.update()
    pause_btn.draw(screen)
    if pause_btn.is_clicked() and not paused:
        music_player.pause()
        cancel_sfx.play()
        paused = True
    if paused:
        display_pause(level)
    if current_player_state == PlayerState.LOST:
        music_player.stop_and_unload()
        display_game_over(level)
    elif current_player_state == PlayerState.WON:
        music_player.stop_and_unload()
        display_game_clear(level)


# GAME LOOP
if __name__ == "__main__":
    while running:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        if current_location == Location.MAIN_MENU:
            display_main_menu()
        elif current_location == Location.HOW_TO:
            display_how_to()
        elif current_location == Location.LEVEL_SELECTION:
            display_level_select()
        elif current_location > 0:
            display_level(levels[current_location - 1])

        pygame.display.update()
    pygame.quit()