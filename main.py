
import pygame
import sys
import json
from pytmx.util_pygame import load_pygame
from Player import *
from data import *
from tools import *
from ia import FighterAI

# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption(CONFIG["WINDOW_TITLE"])
sprite_sheet = pygame.image.load(sprite_file).convert_alpha()

# === CHARGER LA MAP ===
tmx_data = load_pygame(map_stage_01)

background = None
for layer in tmx_data.layers:
    if layer.name == "Background" and hasattr(layer, "image"):
        background = layer.image

collision_rects = []
for obj in tmx_data.objects:
    if obj.name.lower() == "collision":
        collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

# === GAME LOOP ===
clock = pygame.time.Clock()
joueur2 = Player(100, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_LSHIFT, pygame.K_s, pygame.K_e)
joueur1 = Player(100, CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RCTRL, pygame.K_DOWN, pygame.K_RSHIFT)
ia = FighterAI(joueur2)

# Charger la Q-table si elle existe
try:
    with open("q_table.json", "r") as f:
        ia.q_table = json.load(f)
        if not isinstance(ia.q_table, dict):
            print("Q-table invalide, réinitialisation.")
            ia.q_table = {}
except (FileNotFoundError, json.JSONDecodeError):
    print("Q-table non trouvée ou corrompue, réinitialisation.")
    ia.q_table = {}

running = True
while running:
    dt = clock.tick(CONFIG["FPS"]) / 10
    fenetre.fill(BLANC)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    draw_map(fenetre, tmx_data)
    joueur1.update(touches, collision_rects)
    joueur1.draw(fenetre)
    joueur1.draw_health_bar(fenetre, 20, 20)

    # IA joue
    ia.act(joueur1, collision_rects)
    joueur2.draw(fenetre)
    joueur2.draw_health_bar(fenetre, CONFIG["WINDOW_WIDTH"] - 220, 20)

    # Résolution de chevauchement
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
    reward = 0

    if joueur1.can_hit() and joueur1.rect.colliderect(joueur2.rect) and not joueur2.is_dodging:
        joueur2.health -= joueur1.get_attack_damage()
        joueur1.last_attack_frame = int(joueur1.frame_index)
        joueur2.is_attacking = False
        joueur2.etat = "idle"
        joueur2.frame_index = 0
        if joueur2.health < 0:
            joueur2.health = 0
        joueur2.reset_jump_state()

    if joueur2.can_hit() and joueur2.rect.colliderect(joueur1.rect) and not joueur1.is_dodging:
        joueur1.health -= joueur2.get_attack_damage()
        joueur2.last_attack_frame = int(joueur2.frame_index)
        joueur1.is_attacking = False
        joueur1.etat = "idle"
        joueur1.frame_index = 0
        reward += 10
        if joueur1.health < 0:
            joueur1.health = 0
    elif joueur2.is_attacking and not joueur2.rect.colliderect(joueur1.rect):
        reward -= 2

    if joueur2.health < joueur1.health:
        reward -= 1
    else:
        reward += 1

    ia.update_q_table(reward, ia.get_state(joueur1))

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

# Sauvegarde de la Q-table à la fin
with open("q_table.json", "w") as f:
    json.dump(ia.q_table, f)

pygame.quit()
sys.exit()
