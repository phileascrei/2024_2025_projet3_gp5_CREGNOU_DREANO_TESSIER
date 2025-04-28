import pygame


def toto ():
    print("toto")
    return 0

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_name):
        super().__init__()

        # Paramètres de la sprite sheet
        FRAME_WIDTH = 64 # Largeur d'une frame dans l'anim 
        FRAME_HEIGHT = 64   # Hauteur d'une frame dans l'anim
        FRAME_COUNT = 32  # Nombre total de frames dans l'anim
        FRAME_ROWS = 4  # Nombre de lignes dans l'anim
        FRAME_COLS = 8  # Nombre de colonnes dans l'anim

        self.load_sprite_sheet = pygame








    def load_sprite_sheet(self, sprite_sheet_name):
        sprite_sheet = pygame.image.load("assets/player_sprite_sheet/PNG/Unarmed_Run/Unarmed_Run_full.png").convert_alpha()
        self.rect = self.image.get_rect()
        

    def animate(self, direction) :
        if direction == 'right':
            self.image = self.get_image(0, 128)
        elif direction == 'left':
            self.image = self.get_image(0, 64)
        elif direction == 'down':
            self.image = self.get_image(0, 0)  
        elif direction == 'up':
            self.image = self.get_image(0, 192)