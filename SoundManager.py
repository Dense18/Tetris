import pygame
from settings import *
import os

class SoundManager:
    MAIN_OST_SFX = "tetrisOst"

    MOVE_SFX = "move"
    ROTATE_SFX = "rotate"
    HOLD_SFX = "hold"

    LAND_SFX = "floor"
    HARD_DROP_SFX = "harddrop"

    CLEAR_LINE_SFX = "clearlline"
    COMBO_BREAK_SFX = "combo_break_2"
    
    
    def __init__(self) -> None:
        self.set_sound_channel()
        self.load_sounds()

    def set_sound_channel(self):
        pygame.mixer.Channel(SFX_CHANNEL).set_volume(0.7)
        pygame.mixer.Channel(COMBO_CHANNEL).set_volume(0.7)
        pygame.mixer.Channel(OST_CHANNEL).set_volume(0.1)
    
    def play_ost(self, loops = -1):
        pygame.mixer.Channel(OST_CHANNEL).play(self.ost, - 1)
    
    def play_sfx(self, id):
        pygame.mixer.Channel(SFX_CHANNEL).play(self.sfx_dict[id])

    def play_combo(self, num_combo):
        combo = min(16, num_combo)
        pygame.mixer.Channel(COMBO_CHANNEL).play(self.combos_sfx_dict[combo])
    
    def stop_ost(self):
        pygame.mixer.Channel(OST_CHANNEL).stop()

    def stop_sfx(self):
        pygame.mixer.Channel(SFX_CHANNEL).stop()

    def stop_combo(self):
        pygame.mixer.Channel(COMBO_CHANNEL).stop()
    
    def stop(self):
        self.stop_ost()
        self.stop_sfx()
        self.stop_combo()
        
    def load_sounds(self):
        self.ost = pygame.mixer.Sound(os.path.join(SOUND_DIR, "tetrisOst.mp3"))

        self.sfx_dict = {
            SoundManager.MOVE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "move.ogg")),
            SoundManager.ROTATE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "rotate.ogg")),
            SoundManager.HOLD_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "hold.ogg")),

            SoundManager.LAND_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "floor.ogg")),
            SoundManager.HARD_DROP_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "harddrop.ogg")),

            SoundManager.CLEAR_LINE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "clearline.ogg")),
            SoundManager.COMBO_BREAK_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "combo_break_2.ogg")),
        }

        self.combos_sfx_dict = {}
        combos = (i for i in range(17))
        for combo in combos:
            self.combos_sfx_dict[combo] = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, f"combo_{combo}.mp3"))
