import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets\\player_sprite_sheet\\PNG\\Unarmed_Idle\\Unarmed_Idle_full.png").convert_alpha()
        self.sprite_sheet.set_colorkey([0, 0, 0])
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]

    def move_right(self): self.position[0] += 5
    def move_left(self): self.position[0] -= 5
    def move_up(self): self.position[1] -= 5   
    def move_down(self): self.position[1] += 5


    
    def update(self):
        self.rect.topleft = self.position

    def get_image(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64))
        return image