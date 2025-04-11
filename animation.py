import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_name):
        super().__init__()
        self.sprite_sheet_name = sprite_sheet_name
        self.load_sprite_sheet(sprite_sheet_name)
        self.current_frame = 0
        self.animation_speed = 0.1  
        self.last_update = pygame.time.get_ticks()

    def load_sprite_sheet(self, sprite_sheet_name):
        self.image = pygame.image.load(f"assets/{sprite_sheet_name}.png").convert_alpha()
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