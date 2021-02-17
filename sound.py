"""
This module loads the background music and additional sound effects, and contains the MusicPlayer class which is used
to manipulate the current background music.
"""

import pygame.mixer

pygame.mixer.init()

# BGM LOCATIONS
bgm_main = "assets/sound/bgm_main.wav"
bgm_level_sky = "assets/sound/bgm_level.wav"
bgm_level_underground = "assets/sound/bgm_under_level.wav"

# Menu SFX
select_sfx = pygame.mixer.Sound(r"assets/sound/select1.wav")
cancel_sfx = pygame.mixer.Sound(r"assets/sound/select2.wav")
game_over_sfx = pygame.mixer.Sound(r"assets/sound/gameover.wav")
win_sfx = pygame.mixer.Sound(r"assets/sound/win.wav")

# In-game audio
jump_sfx = pygame.mixer.Sound(r"assets/sound/jump.wav")
potion_collect_sfx = pygame.mixer.Sound(r"assets/sound/collect1.wav")
gem_collect_sfx = pygame.mixer.Sound(r"assets/sound/collect2.wav")
key_collect_sfx = pygame.mixer.Sound(r"assets/sound/collect3.wav")
torch_collect_sfx = pygame.mixer.Sound(r"assets/sound/torch.wav")
player_atk_sfx = pygame.mixer.Sound(r"assets/sound/attack.wav")
enemy_hit_sfx = pygame.mixer.Sound(r"assets/sound/hit.wav")
shield_sfx = pygame.mixer.Sound(r"assets/sound/shield.wav")
shield_blink_sfx = pygame.mixer.Sound(r"assets/sound/select1.wav")


class MusicPlayer:
    """
    Class for handling sound in runtime.
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
