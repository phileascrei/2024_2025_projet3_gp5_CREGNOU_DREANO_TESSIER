import pygame
import animation


class Player(animation.AnimateSprite):
    def __init__(self,x ,y):
        super().__init__("Unarmed_Run_full")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 64),
            'right': self.get_image(0, 128),
            'up': self.get_image(0, 192)
            
        }

    def change_animation(self, name): 
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_right(self): self.position[0] += 2
    def move_left(self): self.position[0] -= 2
    def move_up(self): self.position[1] -= 2   
    def move_down(self): self.position[1] += 2


    
    def update(self):
        self.rect.topleft = self.position
        self.animate()

    def get_image(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.image, (0, 0), (x, y, 64, 64))
        return image