import os

import pygame

from settings import *


class SoundManager:
    """
        Manages the sound for the Tetris Game
    """
    MAIN_OST_SFX = "tetrisOst"

    MOVE_SFX = "move"
    ROTATE_SFX = "rotate"
    HOLD_SFX = "hold"

    LAND_SFX = "floor"
    HARD_DROP_SFX = "harddrop"

    CLEAR_LINE_SFX = "clearlline"
    COMBO_BREAK_SFX = "combo_break_2"
    
    
    def __init__(self):
        self.channels = [SFX_CHANNEL, COMBO_CHANNEL, OST_CHANNEL]

        self.ost_volume = 0.1
        self.combo_volume = 0.7
        self.sfx_volume = 0.7

        self.is_muted = False

        self.set_sound_channel()
        self.load_sounds()


    def set_sound_channel(self):
        """
        Sets the sound channel for the game
        """
        pygame.mixer.Channel(SFX_CHANNEL).set_volume(self.sfx_volume)
        pygame.mixer.Channel(COMBO_CHANNEL).set_volume(self.combo_volume)
        pygame.mixer.Channel(OST_CHANNEL).set_volume(self.ost_volume)
    
    #* Play Sounds *#
    
    def play_ost(self, loops = -1):
        """
        Plays the Main Tetris OST sound [loops] times
        
        Args:
            loops: number of times to play the sound. -1 means infinite
        """
        pygame.mixer.Channel(OST_CHANNEL).play(self.ost, loops)
    
    def play_sfx(self, id, loops = 0):
        """
        Plays a sfx sound based on the id
        
        Args:
            loops: number of times to play the sound. -1 means infinite
        """
        pygame.mixer.Channel(SFX_CHANNEL).play(self.sfx_dict[id], loops)

    def play_combo(self, num_combo, loops = 0):
        """
        Plays a combo sfx sound based on the [num_combo]
        
        Args:
            num_combo: the number of combos of the Tetris game
            loops: number of times to play the sound. -1 means infinite
        """
        combo = min(15, num_combo)
        pygame.mixer.Channel(COMBO_CHANNEL).play(self.combos_sfx_dict[combo], loops)
    
    #* Stop Sounds *#
    
    def stop_ost(self):
        """
        Stops the Main Tetris OST sound
        """
        pygame.mixer.Channel(OST_CHANNEL).stop()

    def stop_sfx(self):
        """
        Stops all sfx sounds
        """
        pygame.mixer.Channel(SFX_CHANNEL).stop()

    def stop_combo(self):
        """
        Stops all combo sfx sounds
        """
        pygame.mixer.Channel(COMBO_CHANNEL).stop()
    
    def stop(self):
        """
        Stops all sounds
        """
        self.stop_ost()
        self.stop_sfx()
        self.stop_combo()

    #* Mute/Unmute Sounds *#
    
    def toggle_mute(self):
        """
        Toggles mute status of all sounds
        """
        self.unmute() if self.is_muted else self.mute()

    def mute(self):
        """
        Mute all sounds
        """
        for channel in self.channels:
            pygame.mixer.Channel(channel).set_volume(0) 
        self.is_muted = True

    def unmute(self):
        """
        Unmute all sounds
        """
        if not self.is_muted:
            return
        
        pygame.mixer.Channel(OST_CHANNEL).set_volume(self.ost_volume)
        pygame.mixer.Channel(SFX_CHANNEL).set_volume(self.sfx_volume)
        pygame.mixer.Channel(COMBO_CHANNEL).set_volume(self.combo_volume)
        self.is_muted = False

    #* Load Sounds *#
    
    def load_sounds(self):
        """
        Loads all neccessary sounds onto the system
        """
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
        combos = (i for i in range(-1, 16))
        for combo in combos:
            self.combos_sfx_dict[combo] = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, f"combo_{combo}.mp3"))
