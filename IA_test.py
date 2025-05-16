import pygame
import numpy as np
import random

# Initialisation
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("Combat AI")

# Couleurs
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

# Q-learning
actions = ["forward", "backward", "attack", "block"]
Q_table = np.zeros((10, len(actions)))
epsilon, alpha, gamma = 0.2, 0.1, 0.9

# Variables de jeu
player_score = 0
enemy_score = 0
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)
COOLDOWN_TIME = 1000  # ms

# Réinitialisation de round
def reset_round():
    return 100, 400, 5, 5, "idle", "idle"

player_x, enemy_x, player_health, enemy_health, player_action, enemy_action = reset_round()
running = True

# Cooldowns
player_last_attack_time = 0
player_last_block_time = 0
enemy_last_attack_time = 0
enemy_last_block_time = 0

while running:
    screen.fill(BLACK)

    # Fin de partie
    if player_score >= 2 or enemy_score >= 2:
        winner = "Joueur" if player_score >= 2 else "IA"
        screen.blit(big_font.render(f"{winner} gagne le match !", True, WHITE), (100, 200))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Entrée joueur
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    can_player_attack = current_time - player_last_attack_time > COOLDOWN_TIME
    can_player_block = current_time - player_last_block_time > COOLDOWN_TIME
    can_enemy_attack = current_time - enemy_last_attack_time > COOLDOWN_TIME
    can_enemy_block = current_time - enemy_last_block_time > COOLDOWN_TIME

    if keys[pygame.K_LEFT]:
        player_x -= 5
        player_action = "forward"
    elif keys[pygame.K_RIGHT]:
        player_x += 5
        player_action = "backward"
    elif keys[pygame.K_a] and can_player_attack:
        player_action = "attack"
        player_last_attack_time = current_time
    elif keys[pygame.K_s] and can_player_block:
        player_action = "block"
        player_last_block_time = current_time
    else:
        player_action = "idle"

    # État IA
    distance = abs(enemy_x - player_x)
    state = min(int(distance / 60), 9)

    # Choix d'action uniquement si cooldown OK
    if (can_enemy_attack and can_enemy_block):
        if random.uniform(0, 1) < epsilon:
            action_idx = random.randint(0, len(actions) - 1)
        else:
            action_idx = np.argmax(Q_table[state])
        proposed_action = actions[action_idx]

        if proposed_action == "attack" and can_enemy_attack:
            enemy_action = "attack"
            enemy_last_attack_time = current_time
        elif proposed_action == "block" and can_enemy_block:
            enemy_action = "block"
            enemy_last_block_time = current_time
        else:
            enemy_action = proposed_action

    # Exécution action IA
    reward = -0.1
    if enemy_action == "forward":
        enemy_x -= 3
    elif enemy_action == "backward":
        enemy_x += 3
    elif enemy_action == "attack" and distance < 60:
        if player_action != "block":
            player_health -= 1
            reward = 1
    elif enemy_action == "block":
        reward = 0.2

    # Action joueur
    if player_action == "attack" and distance < 60:
        if enemy_action != "block":
            enemy_health -= 1

    # Q-learning update
    new_state = min(int(abs(enemy_x - player_x) / 60), 9)
    future_reward = np.max(Q_table[new_state])
    Q_table[state, action_idx] += alpha * (reward + gamma * future_reward - Q_table[state, action_idx])

    # Affichage
    player_color = RED if player_action == "attack" else GREEN
    enemy_color = RED if enemy_action == "attack" else GREEN
    pygame.draw.rect(screen, player_color, (player_x, 400, 50, 50))
    pygame.draw.rect(screen, enemy_color, (enemy_x, 400, 50, 50))
    pygame.draw.rect(screen, GREEN, (20, 20, player_health * 20, 20))
    pygame.draw.rect(screen, RED, (600 - enemy_health * 20, 20, enemy_health * 20, 20))

    screen.blit(font.render(f"Joueur: {player_action}", True, WHITE), (20, 50))
    screen.blit(font.render(f"IA: {enemy_action}", True, WHITE), (20, 80))
    screen.blit(font.render(f"Score Joueur: {player_score}", True, WHITE), (20, 120))
    screen.blit(font.render(f"Score IA: {enemy_score}", True, WHITE), (20, 150))

    pygame.display.flip()
    clock.tick(60)

    # Fin de round
    if player_health <= 0 or enemy_health <= 0:
        round_winner = "Joueur" if enemy_health <= 0 else "IA"
        if round_winner == "Joueur":
            player_score += 1
        else:
            enemy_score += 1

        screen.blit(big_font.render(f"{round_winner} gagne le round !", True, WHITE), (100, 200))
        pygame.display.flip()
        pygame.time.delay(2000)
        player_x, enemy_x, player_health, enemy_health, player_action, enemy_action = reset_round()

pygame.quit()

