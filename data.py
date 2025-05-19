import pygame  
import sys
from Player import *



# SPRITE SHEET
sprite_file = "assets/Arcade - Marvel vs Capcom - Captain America.jpg"



# === CONFIGURATION ===
CONFIG = {
    "WINDOW_WIDTH": 960,
    "WINDOW_HEIGHT": 540,
    "PLAYER_WIDTH": 100,
    "PLAYER_HEIGHT": 140,
    "FPS": 60,
    "PLAYER_SPEED": 5,
    "PLAYER_RUN_SPEED": 9,
    "GRAVITY": 1,
    "JUMP_FORCE": 18,
    "ANIMATION_SPEED": 0.2,
    "MAX_HEALTH": 100,
    "RECULE" : 10
}

# COULEURS 
BLANC = (255, 255, 255)
BLEU = (0, 0, 200)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)



# === ANIMATIONS ===
animations_data = {
    "idle": {"frames": 9, "width": 97, "height": 135, "line": 0},
    "walk": {"frames": 6, "width": 100, "height": 135, "line": 150},
    "run": {"frames": 6, "width": 100, "height": 135, "line": 285},
    "jump": {"frames": 6, "width": 100, "height": 170, "line": 420},
    "attack": {"frames": 8, "widths": [95, 145, 100, 130, 110, 140, 130, 100], "height": 150, "line": 840},
    "dodge": {"frames": 5, "widths": [120, 170, 160, 110, 110], "height": 130, "line": 2860}
}