import pygame


# def toto ():
#     print("toto")
#     return 0

# class AnimateSprite(pygame.sprite.Sprite):
#     def __init__(self, sprite_sheet_name):
#         super().__init__()

#         # Paramètres de la sprite sheet
#         FRAME_WIDTH = 64 # Largeur d'une frame dans l'anim 
#         FRAME_HEIGHT = 64   # Hauteur d'une frame dans l'anim
#         FRAME_COUNT = 32  # Nombre total de frames dans l'anim
#         FRAME_ROWS = 4  # Nombre de lignes dans l'anim
#         FRAME_COLS = 8  # Nombre de colonnes dans l'anim

#         self.load_sprite_sheet = pygame








#     def load_sprite_sheet(self, sprite_sheet_name):
#         sprite_sheet = pygame.image.load("assets/player_sprite_sheet/PNG/Unarmed_Run/Unarmed_Run_full.png").convert_alpha()
#         self.rect = self.image.get_rect()
        

#     def animate(self, direction) :
#         if direction == 'right':
#             self.image = self.get_image(0, 128)
#         elif direction == 'left':
#             self.image = self.get_image(0, 64)
#         elif direction == 'down':
#             self.image = self.get_image(0, 0)  
#         elif direction == 'up':
#             self.image = self.get_image(0, 192)


import pygame

class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, frame_count, frame_duration):
        """
        Initialise une animation à partir d'une sprite sheet.
        :param sprite_sheet_path: Chemin vers l'image de la sprite sheet.
        :param frame_width: Largeur d'une frame.
        :param frame_height: Hauteur d'une frame.
        :param frame_count: Nombre total de frames dans la sprite sheet.
        :param frame_duration: Durée d'affichage de chaque frame (en millisecondes).
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0

        # Découper les frames
        self.frames = [
            self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            for i in range(frame_count)
        ]

    def update(self, dt):
        """
        Met à jour l'animation en fonction du temps écoulé.
        :param dt: Temps écoulé depuis la dernière frame (en millisecondes).
        """
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count

    def draw(self, surface, x, y):
        """
        Dessine la frame actuelle sur la surface donnée.
        :param surface: Surface Pygame où dessiner.
        :param x: Position X.
        :param y: Position Y.
        """
        surface.blit(self.frames[self.current_frame], (x, y))