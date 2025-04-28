# import pygame
# import pytmx
# import pyscroll
# import pytmx.util_pygame
# from player import Player

# class Game:

#     def __init__(self):
#         #fenêtre du jeu
#         self.screen = pygame.display.set_mode((1920, 1080))
#         pygame.display.set_caption("Jeux 2D")

#         #charger la carte
#         tmx_data = pytmx.util_pygame.load_pygame("assets\carte.tmx")
#         map_data = pyscroll.data.TiledMapData(tmx_data)
#         map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size(), clamp_camera=True)
#         map_layer.zoom = 2

#         #générer le joueur
#         player_position = tmx_data.get_object_by_name("player")
#         self.player = Player(player_position.x, player_position.y)

#         #desiner le groupe de calques
#         self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
#         self.group.add(self.player)

#     def handle_input(self):
#         pressed = pygame.key.get_pressed()
#         if pressed[pygame.K_UP]:
#             self.player.move_up()
#             self.player.change_animation('up')
#         elif pressed[pygame.K_DOWN]:
#             self.player.move_down()
#             self.player.change_animation('down')
#         elif pressed[pygame.K_LEFT]:
#             self.player.move_left()
#             self.player.change_animation('left')
#         elif pressed[pygame.K_RIGHT]:
#             self.player.move_right()
#             self.player.change_animation('right')


       
#     def run(self):

#         clock = pygame.time.Clock()
#         #garder la fenêtre ouverte
#         running = True
#         while running:
#             self.handle_input()
#             self.group.update()
#             self.group.center(self.player.rect.center)
#             self.group.draw(self.screen)
#             pygame.display.flip()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#             clock.tick(60)
#         pygame.quit()





import pygame
from animation import Animation

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        # Charger une animation (exemple avec une sprite sheet)
        self.player_animation = Animation(
            sprite_sheet_path="assets/player_sprite_sheet/PNG/Unarmed_Run/Unarmed_Run_full.png",  # Chemin vers la sprite sheet
            frame_width=64,  # Largeur d'une frame
            frame_height=64,  # Hauteur d'une frame
            frame_count=4,  # Nombre de frames
            frame_duration=100  # Durée de chaque frame (en ms)
        )

        self.player_pos = pygame.Vector2(100, 100)

    def run(self):
        while self.running:
            dt = self.clock.tick(60)  # Temps écoulé en millisecondes
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        # Mettre à jour l'animation
        self.player_animation.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Effacer l'écran
        # Dessiner l'animation
        self.player_animation.draw(self.screen, self.player_pos.x, self.player_pos.y)
        pygame.display.flip()