import pygame
import sys

# Initialisation
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Jeu 2D - Animation de course")
clock = pygame.time.Clock()

# Chargement de la sprite sheet
sprite_sheet = pygame.image.load("assets/player_sprite_sheet/PNG/Unarmed_Run/Unarmed_Run_full.png").convert_alpha()

# Paramètres de la sprite sheet
FRAME_WIDTH = 64
FRAME_HEIGHT = 64
FRAME_COUNT = 32  # Nombre total de frames dans la sprite sheet
FRAME_ROWS = 4  # Nombre de lignes dans la sprite sheet
FRAME_COLS = 8  # Nombre de colonnes dans la sprite sheet


# Extraction des frames (ligne 2 = vers la droite par exemple)
def get_frames(row):
    return [sprite_sheet.subsurface(pygame.Rect(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)) for col in range(FRAME_COLS)]

run_frames = get_frames(1)  # Ligne 2 = vers la droite

# Position du personnage
x, y = 100, 100
frame_index = 0
frame_delay = 100  # en millisecondes
last_update = pygame.time.get_ticks()

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Animation
    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        frame_index = (frame_index + 1) % len(run_frames)
        last_update = now

    screen.blit(run_frames[frame_index], (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
