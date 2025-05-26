

import pygame
import sys
from pytmx.util_pygame import load_pygame

from Player import *
from data import *
from tools import *
from ia import FighterAI

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



# === GAME LOOP ===
clock = pygame.time.Clock()
joueur2 = Player(CONFIG["WINDOW_WIDTH"] // 2 - 20, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_LSHIFT, pygame.K_s, pygame.K_e)
joueur1 = Player(CONFIG["WINDOW_WIDTH"] // 2 + 20, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_RCTRL, pygame.K_g, pygame.K_r)
ia = FighterAI(joueur1)


running = True
while running:
    dt = clock.tick(CONFIG["FPS"]) / 10
    fenetre.fill(BLANC)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    draw_map(fenetre, tmx_data)
    ia.act(joueur1, collision_rects)
    joueur1.draw(fenetre)
    joueur1.draw_health_bar(fenetre, 20, 20)

    joueur2.update(touches, collision_rects)
    joueur2.draw(fenetre)
    joueur2.draw_health_bar(fenetre, CONFIG["WINDOW_WIDTH"] - 220, 20)

    if joueur1.rect.colliderect(joueur2.rect):
        if not (joueur1.is_attacking or joueur2.is_attacking):
            tolerance = 5
            if joueur1.pos_x < joueur2.pos_x:
                joueur1.pos_x = joueur2.rect.left - joueur1.rect.width // 2 + tolerance
                joueur2.pos_x = joueur1.rect.right + joueur2.rect.width // 2 - tolerance
            else:
                joueur1.pos_x = joueur2.rect.right + joueur1.rect.width // 2 - tolerance
                joueur2.pos_x = joueur1.rect.left - joueur2.rect.width // 2 + tolerance


    # Gestion des dégâts
    if joueur1.can_hit() and joueur1.rect.colliderect(joueur2.rect) and not joueur2.is_dodging:
        joueur2.health -= joueur1.get_attack_damage()
        joueur2.is_stunned = True
        joueur1.last_attack_frame = int(joueur1.frame_index)
        # Annule l'attaque et l'animation de joueur2 s'il prend des dégâts
        joueur2.is_attacking = False
        joueur2.etat = "idle"
        joueur2.frame_index = 0
        if joueur2.health < 0:
            joueur2.health = 0
        joueur2.reset_jump_state()

    if joueur2.can_hit() and joueur2.rect.colliderect(joueur1.rect) and not joueur1.is_dodging:
        joueur1.health -= joueur2.get_attack_damage()
        joueur1.is_stunned = True
        joueur2.last_attack_frame = int(joueur2.frame_index)
        # Annule l'attaque et l'animation de joueur1 s'il prend des dégâts
        joueur1.is_attacking = False
        joueur1.etat = "idle"
        joueur1.frame_index = 0
        if joueur1.health < 0:
            joueur1.health = 0
        joueur1.reset_jump_state()


    # === Système de récompense pour l'IA ===
    reward = 0
    
    # Bonus : l'IA touche l'adversaire
    if joueur1.can_hit() and joueur1.rect.colliderect(joueur2.rect) and not joueur2.is_dodging:
        reward += 10  # action positive
        reward -= 1 if joueur2.is_attacking else 0  # léger malus si elle attaque sans esquiver
    
    # Malus : l'IA prend un coup
    if joueur2.can_hit() and joueur2.rect.colliderect(joueur1.rect) and not joueur1.is_dodging:
        reward -= 10  # mauvaise action
    
    # Bonus si IA évite une attaque pendant qu’elle est proche
    if abs(joueur1.pos_x - joueur2.pos_x) < 100 and joueur2.is_attacking and joueur1.is_dodging:
        reward += 5
    
    # Petit malus si IA reste idle trop longtemps
    if joueur1.etat == "idle":
        reward -= 0.5
    
    # Apprentissage : feedback
    ia.reward_feedback(reward, joueur2)

    pygame.display.flip()

pygame.quit()
sys.exit()



