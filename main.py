
import pygame
import sys
from pytmx.util_pygame import load_pygame

from Player import *
from data import *

# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption("Marvel - Captain America")
sprite_sheet = pygame.image.load(sprite_file).convert_alpha()

# === CHARGER LA MAP ===
tmx_data = load_pygame(map_stage_01)

# Charger l'image de fond du calque "Background"
background = None
for layer in tmx_data.layers:
    if layer.name == "Background" and hasattr(layer, "image"):
        background = layer.image

# Récupérer les rectangles de collision depuis Tiled
collision_rects = []
for obj in tmx_data.objects:
    if obj.name.lower() == "collision":  # ignore la casse
        collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

# Affichage de la map (image layers + tile layers)
def draw_map(surface, tmx_data):
    for layer in tmx_data.layers:
        if hasattr(layer, "image") and layer.image:
            surface.blit(layer.image, (0, 0))  # image de fond
        elif hasattr(layer, "tiles"):
            for x, y, image in layer.tiles():
                surface.blit(image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# === GAME LOOP ===
clock = pygame.time.Clock()
joueur1 = Player(100, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_LSHIFT)
joueur2 = pygame.Rect(650, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], CONFIG["PLAYER_WIDTH"], CONFIG["PLAYER_HEIGHT"])

running = True
while running:
    dt = clock.tick(CONFIG["FPS"]) / 10
    fenetre.fill(BLANC)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    draw_map(fenetre, tmx_data)  # affiche background + tuiles
    joueur1.update(touches, collision_rects)
    joueur1.draw(fenetre)
    joueur1.draw_health_bar(fenetre, 20, 20)

    pygame.draw.rect(fenetre, BLEU, joueur2)  # joueur2 temporaire
    pygame.display.flip()

pygame.quit()
sys.exit()
