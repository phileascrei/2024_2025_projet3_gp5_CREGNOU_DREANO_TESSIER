import pygame

#def une classe qui s'occupe des animations
class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f'assets/player_sprite_sheet/PNG/Unarmed_Run/{sprite_name}.png').convert_alpha()
        self.current_image = 0
        self.images = animations.get('player_running')
    def animate(self):
        self.current_image += 0.1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]

def load_animation_images(sprite_name):
    images = []   
    path = f"assets/player_sprite_sheet/PNG/Unarmed_Run/{sprite_name}.png"
    sprite_sheet = pygame.image.load(path)
    sprite_width = 64
    sprite_height = 64
    for i in range(0, sprite_sheet.get_width(), sprite_width):
        image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        image.blit(sprite_sheet, (0, 0), (i, 0, sprite_width, sprite_height))
        images.append(image)
    return images

animations = {
    'player_running': load_animation_images('Unarmed_Run_full')}

        
