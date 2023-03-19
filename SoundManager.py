import os

import pygame

from settings import *


class SoundManager:
    """
        Singleton Class that manages the sound for the Tetris Application
    """
    MAIN_OST = "tetris_ost"
    MENU_OST = "menu_st"
    GAME_OVER_OST = "game_over_ost"
    HIGH_SCORE_OST = "high_score_ost"

    MOVE_SFX = "move"
    ROTATE_SFX = "rotate"
    HOLD_SFX = "hold"

    LAND_SFX = "floor"
    HARD_DROP_SFX = "harddrop"

    CLEAR_LINE_SFX = "clearlline"
    COMBO_BREAK_SFX = "combo_break_2"
    ALL_CLEAR_SFX = "all_clear"
    LEVEL_UP_SFX = "level_up"
    
    MENU_HOVER_SFX = "menuhover"
    MENU_HIT_SFX = "menuconfirm"
    
    HAS_lOADED = False
    
    __instance = None
    
    def __init__(self):
        if SoundManager.__instance is not None:
            raise Exception("This class is a Singleton! SoundManager instance has been created already!\n Please use the getInstance() method to get the SoundManager instance.")
        
        SoundManager.__instance = self
        self.channels = [SFX_CHANNEL, COMBO_CHANNEL, OST_CHANNEL, MENU_CHANNEL]
        self.volumes = {
            OST_CHANNEL: 0.2,
            SFX_CHANNEL: 0.6,
            COMBO_CHANNEL: 0.6,
            MENU_CHANNEL: 0.5
            
        }

        self.is_muted = False

        self.set_sound_channel()
        self.load_sounds()


    @staticmethod
    def getInstance():
        if SoundManager.__instance is None:
            SoundManager()
        return SoundManager.__instance

    def set_sound_channel(self):
        """
        Sets the sound channel for the game
        """
        for channel in self.channels:
            pygame.mixer.Channel(channel).set_volume(self.volumes[channel])
    #* Play Sounds *#
    
    def play_ost(self, id, loops = -1, update = True):
        """
        Plays an ost sound based on the [id]
        
        Args:
            loops: number of times to play the sound. -1 means infinite
            update: If not set and an ost sound is playing, continue playing the current ost sound
                    Else, play the new sound
        """
        if pygame.mixer.Channel(OST_CHANNEL).get_busy() and not update:
            return
        pygame.mixer.Channel(OST_CHANNEL).play(self.ost_dict[id], loops)
    
    def play_sfx(self, id, loops = 0, override = True):
        """
        Plays a sfx sound based on the [id]
        
        Args:
            loops: number of times to play the sound. -1 means infinite
            override: If set and a sfx sound is playing, stop playing the current sfx sound and play the new one
        """
        if not override:
            self.sfx_dict[id].set_volume(self.volumes[SFX_CHANNEL])
            self.sfx_dict[id].play(loops)
            return
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
    
    def play_menu(self, id, loops = 0):
        """
        Plays a Menu sfx sound based on the id
        
        Args:
            loops: number of times to play the sound. -1 means infinite
        """
        pygame.mixer.Channel(MENU_CHANNEL).play(self.menu_sfx_dict[id], loops)
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
        for channel in self.channels:
            pygame.mixer.Channel(channel).stop()
            
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
        
        for channel in self.channels:
            pygame.mixer.Channel(channel).set_volume(self.volumes[channel])
        self.is_muted = False

    #* Load Sounds *#
    
    def load_sounds(self):
        """
        Loads all neccessary sounds onto the system
        """
        # self.ost = pygame.mixer.Sound(os.path.join(SOUND_DIR, "tetrisOst.mp3"))
        self.ost_dict = {
            SoundManager.MAIN_OST : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_OST_DIR, "tetris_ost.mp3")),
            SoundManager.MENU_OST : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_OST_DIR, "menu_ost.mp3")),
            SoundManager.GAME_OVER_OST : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_OST_DIR, "game_over_ost.mp3")),
            SoundManager.HIGH_SCORE_OST : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_OST_DIR, "high_score_ost.mp3"))
        }

        self.sfx_dict = {
            SoundManager.MOVE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "move.ogg")),
            SoundManager.ROTATE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "rotate.ogg")),
            SoundManager.HOLD_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "hold.ogg")),

            SoundManager.LAND_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "floor.ogg")),
            SoundManager.HARD_DROP_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "harddrop.ogg")),

            SoundManager.CLEAR_LINE_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "clearline.ogg")),
            SoundManager.COMBO_BREAK_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "combo_break_2.ogg")),
            SoundManager.ALL_CLEAR_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "allclear.ogg")),
            SoundManager.LEVEL_UP_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "level_up.ogg"))
        }

        self.combos_sfx_dict = {}
        combos = (i for i in range(-1, 16))
        for combo in combos:
            self.combos_sfx_dict[combo] = pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, f"combo_{combo}.mp3"))
        
        self.menu_sfx_dict = {
            SoundManager.MENU_HOVER_SFX : pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "menuhover.ogg")),
            SoundManager.MENU_HIT_SFX: pygame.mixer.Sound(os.path.join(TETRIS_SOUND_SFX_DIR, "menuhit1.mp3"))                                                   
        }
