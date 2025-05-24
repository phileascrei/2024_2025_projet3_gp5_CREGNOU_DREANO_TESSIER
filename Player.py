import pygame
import os
import random
from data import CONFIG, ROUGE, VERT, NOIR
from tools import load_frames

class Player:
    def __init__(self, x, y, left_key, right_key, jump_key, run_key):
        self.pos_x = x
        self.pos_y = y
        self.vitesse_y = 0
        self.in_air = False
        self.etat = "idle"
        self.frame_index = 0
        self.is_attacking = False
        self.attack_type = None  # <- pour choisir l'attaque
        self.is_charging_jump = False
        self.charge_jump_timer = 0
        self.is_dodging = False
        self.last_dir = "right"
        self.facing_left = False

        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key
        self.run_key = run_key

        self.health = CONFIG["MAX_HEALTH"]

        self.frames_dict = {
            "idle": load_frames("idle"),
            "walk": load_frames("walk"),
            "run": load_frames("run"),
            "jump": load_frames("jump"),
            "dodge": load_frames("dodge"),
            "attack_1": load_frames("attack_1"),
            "attack_2": load_frames("attack_2"),
            "attack_3": load_frames("attack_3"),
        }

        self.image = self.frames_dict["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos_x, self.pos_y)

    def update(self, touches, collision_rects):
        if self.is_dodging:
            self._update_dodge()
            return

        if touches[pygame.K_s] and not self.in_air and not self.is_charging_jump and not self.is_attacking:
            self.is_dodging = True
            self.frame_index = 0
            return

        if touches[pygame.K_e] and not self.is_attacking and not self.is_dodging and not self.in_air:
            self.frame_index = 0
            self.is_attacking = True
            self.start_attack()

        if self.is_attacking:
            self._update_attack()
            return

        self.etat = "idle"
        courir = touches[self.run_key]
        self._handle_movement(touches, courir)
        self._handle_jump(touches)
        self._apply_gravity()
        self._update_animation()

    def start_attack(self):
        attacks = ["attack_1", "attack_2", "attack_3"]
        weights = CONFIG["ATTACK_PROBABILITY"]
        self.etat = random.choices(attacks, weights=weights, k=1)[0]
        self.frame_index = 0
        self.is_attacking = True


    def _update_attack(self): 
        # Dash sur attack_3 entre la 3e et la 8e frame (index 2 à 7 inclus)
        if self.etat == "attack_3":
            dash_start = 2
            dash_end = 7
            dash_distance = CONFIG["DASH_SPEED"]  # dash réparti sur 6 frames
            if dash_start <= int(self.frame_index) <= dash_end:
                if self.facing_left:
                    self.pos_x -= dash_distance
                else:
                    self.pos_x += dash_distance

        self.frame_index += CONFIG["ANIMATION_SPEED"]
        if self.frame_index >= len(self.frames_dict[self.etat]):
            self.frame_index = 0 
            self.is_attacking = False 
        self._apply_gravity() 

    def _handle_movement(self, touches, courir):
        if not self.is_charging_jump:
            if touches[self.left_key] and self.pos_x > 0:
                self.pos_x -= CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
                self.etat = "run" if courir else "walk"
                self.facing_left = True
            elif touches[self.right_key] and self.pos_x < CONFIG["WINDOW_WIDTH"]:
                self.pos_x += CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
                self.etat = "run" if courir else "walk"
                self.facing_left = False

    def _handle_jump(self, touches):
        if touches[self.jump_key] and not self.in_air and not self.is_charging_jump:
            self.is_charging_jump = True
            self.charge_jump_timer = pygame.time.get_ticks()
            self.frame_index = 0

        if self.is_charging_jump:
            self.etat = "jump"
            self.frame_index = 0
            if not touches[self.jump_key]:
                self.vitesse_y = -CONFIG["JUMP_FORCE"]
                self.in_air = True
                self.is_charging_jump = False

    def _update_dodge(self):
        self.etat = "dodge"
        self.frame_index += CONFIG["ANIMATION_SPEED"]
        if self.facing_left:
            self.pos_x += CONFIG["RECULE"]
            self.pos_x = max(self.pos_x, 0)
        else:
            self.pos_x -= CONFIG["RECULE"]
            self.pos_x = min(self.pos_x, CONFIG["WINDOW_WIDTH"])
        if self.frame_index >= len(self.frames_dict["dodge"]):
            self.frame_index = 0
            self.is_dodging = False
        self._apply_gravity()

    def _apply_gravity(self):
        self.vitesse_y += CONFIG["GRAVITY"]
        self.pos_y += self.vitesse_y
        sol = CONFIG["WINDOW_HEIGHT"]
        if self.pos_y >= sol:
            self.pos_y = sol
            self.vitesse_y = 0
            self.in_air = False

    def _update_animation(self):
        if self.in_air and not self.is_charging_jump:
            self.etat = "jump"
        self.frame_index += CONFIG["ANIMATION_SPEED"]
        if self.frame_index >= len(self.frames_dict[self.etat]):
            self.frame_index = 0

    def draw(self, surface):
        self.image = self.frames_dict[self.etat][int(self.frame_index)]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (int(self.pos_x), int(self.pos_y))
        surface.blit(self.image, self.rect)

    def draw_health_bar(self, surface, x, y):
        bar_width = 200
        bar_height = 20
        fill = (self.health / CONFIG["MAX_HEALTH"]) * bar_width
        pygame.draw.rect(surface, ROUGE, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, VERT, (x, y, fill, bar_height))
        pygame.draw.rect(surface, NOIR, (x, y, bar_width, bar_height), 2)
    
    def reset(self):
        self.pos_x = 100
        self.pos_y = CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"]
        self.vitesse_y = 0
        self.in_air = False
        self.etat = "idle"
        self.frame_index = 0
        self.is_attacking = False
        self.is_charging_jump = False
        self.is_dodging = False
        self.facing_left = False
        self.health = CONFIG["MAX_HEALTH"]