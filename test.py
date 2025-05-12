# import pygame
# import sys

# # Initialisation de Pygame
# pygame.init()

# # Chargement de l'image sprite sheet
# sprite_sheet = pygame.image.load("assets/DS DSi - Jump Super Stars - Arale.png")
# sprite_sheet.set_colorkey((0, 0, 255))  # Supprime le bleu

# # Dimensions d'une frame individuelle (à ajuster)
# frame_width = 30
# frame_height = 45

# # Extraction des frames (par exemple les 8 premières de la première ligne)
# frames = []
# for i in range(4):  # nombre de frames à animer
#     frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
#     frames.append(frame)

# # Création de la fenêtre d'affichage
# screen = pygame.display.set_mode((frame_width * 10, frame_height * 10))
# pygame.display.set_caption("Animation d'Arale")

# # Horloge pour contrôler la vitesse de l'animation
# clock = pygame.time.Clock()

# # Index de frame
# frame_index = 0

# # Boucle principale
# running = True
# while running:
#     screen.fill((0, 0, 0))  # Fond noir au lieu du bleu
 

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:  # Touche flèche droite
#                 current_frames = run_frames
#             elif event.key == pygame.K_LEFT:  # Touche flèche gauche
#                 current_frames = idle_frames

#     # Affichage de la frame actuelle
#     current_frame = pygame.transform.scale(frames[frame_index], (frame_width * 2, frame_height * 2))
#     screen.blit(current_frame, (0, 0))

#     # Avancer à la frame suivante
#     frame_index = (frame_index + 1) % len(frames)

#     # Rafraîchissement
#     pygame.display.flip()
#     clock.tick(6)  # 6 FPS

# # Fermeture
# pygame.quit()
# sys.exit()







import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre d'affichage (doit être avant le chargement de l'image)
screen = pygame.display.set_mode((300, 300))  # Taille arbitraire pour l'exemple
pygame.display.set_caption("Animation d'Arale")

# Chargement de l'image sprite sheet
sprite_sheet = pygame.image.load("assets/DS DSi - Jump Super Stars - Arale.png").convert()
sprite_sheet.set_colorkey((0, 0, 255))  # Supprime le bleu

# Dimensions d'une frame individuelle (à ajuster)
frame_width = 30
frame_height = 45

# Extraction des animations (par exemple, 2 animations différentes)
idle_frames = [sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height)) for i in range(4)]
run_frames = [sprite_sheet.subsurface((i * frame_width, frame_height, frame_width, frame_height)) for i in range(8)]

# Animation actuelle
current_frames = idle_frames

# Horloge pour contrôler la vitesse de l'animation
clock = pygame.time.Clock()

# Index de frame
frame_index = 0

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))  # Fond noir

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Changer d'animation avec une touche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Touche flèche droite
                frame_width = 30
                current_frames = run_frames
            elif event.key == pygame.K_LEFT:  # Touche flèche gauche
                current_frames = idle_frames

    # Affichage de la frame actuelle
    current_frame = pygame.transform.scale(current_frames[frame_index], (frame_width * 2, frame_height * 2))
    screen.blit(current_frame, (0, 0))

    # Avancer à la frame suivante
    frame_index = (frame_index + 1) % len(current_frames)

    # Rafraîchissement
    pygame.display.flip()
    clock.tick(6)  # 6 FPS

# Fermeture
pygame.quit()
sys.exit()