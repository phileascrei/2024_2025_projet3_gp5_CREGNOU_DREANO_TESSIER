# # import pygame
# # from torch import *

# # # pygame setup
# # pygame.init()
# # screen = pygame.display.set_mode((1280, 720))
# # clock = pygame.time.Clock()
# # running = True
# # speed = 300
# # dt = 0

# # player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# # target_pos = pygame.Vector2(0, 0)

# # while running:
# #     # poll for events
# #     # pygame.QUIT event means the user clicked X to close your window
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False

# #     # fill the screen with a color to wipe away anything from last frame
# #     screen.fill("black")

# #     pygame.draw.circle(screen, "red", player_pos, 40)
# #     pygame.draw.circle(screen, "green", target_pos, 10)

# #     keys = pygame.key.get_pressed()
# #     if keys[pygame.K_z]:
# #         player_pos.y -= 300 * dt
# #     if keys[pygame.K_s]:
# #         player_pos.y += 300 * dt
# #     if keys[pygame.K_q]:
# #         player_pos.x -= 300 * dt
# #     if keys[pygame.K_d]:
# #         player_pos.x += 300 * dt
    
# #     if pygame.mouse.get_pressed()[2]:
# #         target_pos = pygame.Vector2(pygame.mouse.get_pos())
    
# #     if target_pos != player_pos:
# #         direction = target_pos - player_pos
# #         distance = direction.length()
# #         if distance > 5:  
# #             direction.normalize_ip() 
# #             player_pos += direction * speed * dt
# #         else:
# #             player_pos = target_pos


# #     # flip() the display to put your work on screen
# #     pygame.display.flip()

# #     # limits FPS to 60
# #     # dt is delta time in seconds since last frame, used for framerate-
# #     # independent physics.
# #     dt = clock.tick(60) / 1000

# # pygame.quit() 









































# import random
# import pygame
# import torch
# import torch.nn as nn
# import torch.optim as optim

# # Initialisation de pygame
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# speed = 300  
# dt = 0
# velocity = pygame.Vector2(0, 0)

# # Générer des obstacles sans chevauchement
# def generate_obstacles(n, safe_distance=100):
#     obstacles = []
#     for _ in range(n):
#         while True:
#             shape = random.choice(["circle", "rect"])
#             x, y = random.randint(100, 1180), random.randint(100, 620)  
#             if shape == "circle":
#                 radius = random.randint(30, 80)
#                 new_obs = {"shape": "circle", "pos": pygame.Vector2(x, y), "size": radius}
#             else:
#                 width, height = random.randint(50, 150), random.randint(50, 150)
#                 new_obs = {"shape": "rect", "pos": pygame.Vector2(x, y), "size": (width, height)}

#             if not any(check_obstacle_overlap(new_obs, obs, safe_distance) for obs in obstacles):
#                 obstacles.append(new_obs)
#                 break
#     return obstacles

# # Vérifier le chevauchement des obstacles
# def check_obstacle_overlap(obs1, obs2, safe_distance):
#     if obs1["shape"] == "circle" and obs2["shape"] == "circle":
#         return obs1["pos"].distance_to(obs2["pos"]) < (obs1["size"] + obs2["size"] + safe_distance)
#     elif obs1["shape"] == "rect" and obs2["shape"] == "rect":
#         x1, y1 = obs1["pos"]
#         w1, h1 = obs1["size"]
#         x2, y2 = obs2["pos"]
#         w2, h2 = obs2["size"]
#         return not (x1 + w1 + safe_distance < x2 or x2 + w2 + safe_distance < x1 or
#                     y1 + h1 + safe_distance < y2 or y2 + h2 + safe_distance < y1)
#     else:
#         rect = obs1 if obs1["shape"] == "rect" else obs2
#         circle = obs2 if obs1["shape"] == "rect" else obs1
#         rect_x, rect_y = rect["pos"]
#         rect_w, rect_h = rect["size"]
#         circle_x, circle_y = circle["pos"]
#         radius = circle["size"]

#         nearest_x = max(rect_x, min(circle_x, rect_x + rect_w))
#         nearest_y = max(rect_y, min(circle_y, rect_y + rect_h))
#         return pygame.Vector2(nearest_x, nearest_y).distance_to(pygame.Vector2(circle_x, circle_y)) < radius + safe_distance

# # Vérifier si une position est valide
# def is_position_valid(pos, obstacles, min_distance=50):
#     for obs in obstacles:
#         if obs["shape"] == "circle":
#             if pos.distance_to(obs["pos"]) < obs["size"] + min_distance:
#                 return False
#         else:
#             x, y = obs["pos"]
#             w, h = obs["size"]
#             if (x - min_distance <= pos.x <= x + w + min_distance and 
#                 y - min_distance <= pos.y <= y + h + min_distance):
#                 return False
#     return True

# # Réinitialiser le jeu
# def reset_game():
#     global player_pos, target_pos, obstacles, velocity

#     obstacles = generate_obstacles(5)

#     while True:
#         player_pos = pygame.Vector2(random.randint(50, 1230), random.randint(50, 670))
#         if is_position_valid(player_pos, obstacles, 80):
#             break

#     while True:
#         target_pos = pygame.Vector2(random.randint(50, 1230), random.randint(50, 670))
#         if is_position_valid(target_pos, obstacles, 100) and target_pos.distance_to(player_pos) > 200:
#             break

#     velocity = pygame.Vector2(0, 0)

# reset_game()

# # Modèle d'IA
# class DeplacementModel(nn.Module):
#     def __init__(self, obstacle_count):
#         super(DeplacementModel, self).__init__()
#         input_size = 4 + (2 * obstacle_count)  
#         self.fc1 = nn.Linear(input_size, 64)  
#         self.fc2 = nn.Linear(64, 32)
#         self.fc3 = nn.Linear(32, 2)  

#     def forward(self, x):
#         x = torch.relu(self.fc1(x))
#         x = torch.relu(self.fc2(x))
#         return self.fc3(x)

# # Vérification des collisions
# def check_collision(player_pos):
#     for obs in obstacles:
#         if obs["shape"] == "circle":
#             if player_pos.distance_to(obs["pos"]) < obs["size"] + 20:
#                 return True  
#         else:  
#             obs_x, obs_y = obs["pos"]
#             width, height = obs["size"]
#             if (obs_x <= player_pos.x <= obs_x + width) and (obs_y <= player_pos.y <= obs_y + height):
#                 return True  
#     return False  

# # Boucle de mise à jour du jeu
# def update_game():
#     global dt, player_pos, velocity  

#     screen.fill("black")

#     pygame.draw.circle(screen, "red", player_pos, 40)
#     pygame.draw.circle(screen, "green", target_pos, 10)

#     for obs in obstacles:
#         if obs["shape"] == "circle":
#             pygame.draw.circle(screen, "blue", obs["pos"], obs["size"])
#         else:
#             pygame.draw.rect(screen, "blue", (obs["pos"].x, obs["pos"].y, obs["size"][0], obs["size"][1]))

#     inputs = [player_pos.x, player_pos.y, target_pos.x, target_pos.y]
#     for obs in obstacles:
#         inputs.extend([obs["pos"].x, obs["pos"].y])  

#     inputs_tensor = torch.tensor([inputs], dtype=torch.float32)
#     predicted_direction = model(inputs_tensor).detach().numpy()[0]
    
#     new_velocity = pygame.Vector2(predicted_direction[0], predicted_direction[1])
#     if new_velocity.length() > 0:
#         new_velocity = new_velocity.normalize() * speed

#     velocity.update(new_velocity)

#     if check_collision(player_pos):
#         print("💥 Collision ! Réinitialisation.")
#         reset_game()
#         return  

#     if player_pos.distance_to(target_pos) < 25:
#         print("✅ Objectif atteint ! Nouvelle cible.")
#         reset_game()
#         return  

#     player_pos += velocity * dt  

#     pygame.display.flip()
#     dt = clock.tick(60) / 1000

# # Initialisation de l'IA
# model = DeplacementModel(len(obstacles))  
# optimizer = optim.Adam(model.parameters(), lr=0.001)
# criterion = nn.MSELoss()

# # Boucle principale
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     update_game()

# pygame.quit()

























# import random
# import pygame
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch import Tensor

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# speed = 300  # Vitesse constante
# dt = 0

# # Déclaration globale des positions et de la vélocité
# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# target_pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
# velocity = pygame.Vector2(0, 0)  # Vélocité du joueur

# # Paramètres de punition
# punish_threshold = 400  
# punish_time_limit = 2  
# punish_timer = 0  

# # Classe du modèle d'IA
# class DeplacementModel(nn.Module):
#     def __init__(self):
#         super(DeplacementModel, self).__init__()
#         self.fc1 = nn.Linear(4, 64)  
#         self.fc2 = nn.Linear(64, 32)
#         self.fc3 = nn.Linear(32, 2)  

#     def forward(self, x):
#         x = torch.relu(self.fc1(x))
#         x = torch.relu(self.fc2(x))
#         return self.fc3(x)

# # Entraînement du modèle
# def entrainer_model(model, inputs, targets, optimizer, criterion):
#     model.train()
#     inputs = torch.tensor(inputs, dtype=torch.float32)
#     targets = torch.tensor(targets, dtype=torch.float32)

#     predictions = model(inputs)

#     loss = criterion(predictions, targets)

#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()

#     return loss.item()

# def train_ia():
#     global player_pos, target_pos, punish_timer, velocity  

#     screen.fill("black")

#     pygame.draw.circle(screen, "red", player_pos, 40)
#     pygame.draw.circle(screen, "green", target_pos, 10)

#     inputs = [player_pos.x, player_pos.y, target_pos.x, target_pos.y]
    
#     direction = target_pos - player_pos
#     if direction.length() > 0:
#         direction.normalize_ip()
#     targets = [direction.x, direction.y]

#     loss = entrainer_model(model, [inputs], [targets], optimizer, criterion)

#     inputs_tensor = torch.tensor([inputs], dtype=torch.float32)
#     predicted_direction = model(inputs_tensor).detach().numpy()[0]
    
#     # Met à jour la vélocité au lieu de la position directement
#     velocity.update(predicted_direction[0], predicted_direction[1])
#     velocity = velocity.normalize() * speed  # Applique la vitesse constante

#     # Vérifier si la cible est atteinte
#     if player_pos.distance_to(target_pos) < 25:
#         target_pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
#         punish_timer = 0  

#     # Vérifier si l'IA s'éloigne trop
#     if player_pos.distance_to(target_pos) > punish_threshold:
#         punish_timer += dt
#         if punish_timer > punish_time_limit:
#             player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#             target_pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
#             punish_timer = 0  
#             print("L'IA a été punie pour s'être éloignée trop longtemps !")

#     font = pygame.font.SysFont('Arial', 24)
#     loss_text = font.render(f"Loss: {loss:.4f}", True, (255, 255, 255))
#     screen.blit(loss_text, (10, 10))

# # Initialiser le modèle
# model = DeplacementModel()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
# criterion = nn.MSELoss()

# # Boucle principale du jeu
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     train_ia()

#     # Appliquer la vélocité mise à jour à la position
#     player_pos += velocity * dt

#     pygame.display.flip()
#     dt = clock.tick(60) / 1000

# pygame.quit()


