import pygame
import sys

# === CONFIGURATION ===
CONFIG = {
    "WINDOW_WIDTH": 960,
    "WINDOW_HEIGHT": 540,
    "PLAYER_WIDTH": 100,
    "PLAYER_HEIGHT": 140,
    "FPS": 60,
    "PLAYER_SPEED": 5,
    "PLAYER_RUN_SPEED": 9,
    "GRAVITY": 1,
    "JUMP_FORCE": 18,
    "ANIMATION_SPEED": 0.2,
    "MAX_HEALTH": 100
}

# === COULEURS ===
BLANC = (255, 255, 255)
BLEU = (0, 0, 200)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)

# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption("Marvel - Captain America")
sprite_sheet = pygame.image.load("assets/Arcade - Marvel vs Capcom - Captain America.jpg").convert_alpha()

# === ANIMATIONS ===
animations_data = {
    "idle": {"frames": 9, "width": 97, "height": 135, "line": 0},
    "walk": {"frames": 6, "width": 100, "height": 135, "line": 150},
    "run": {"frames": 6, "width": 100, "height": 135, "line": 285},
    "jump": {"frames": 6, "width": 100, "height": 170, "line": 420},
    "attack": {"frames": 8, "widths": [95, 145, 100, 130, 110, 140, 130, 100], "height": 150, "line": 840},
    "dodge": {"frames": 5, "widths": [120, 170, 160, 110, 110], "height": 130, "line": 2860}
}

def get_frame(x, y, largeur, hauteur):
    frame = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (x, y, largeur, hauteur))
    return frame

def load_frames(anim_name):
    frames = []
    data = animations_data[anim_name]
    x_offset = 0
    if "widths" in data:
        for width in data["widths"]:
            frames.append(get_frame(x_offset, data["line"], width, data["height"]))
            x_offset += width
    else:
        for i in range(data["frames"]):
            frames.append(get_frame(data["width"] * i, data["line"], data["width"], data["height"]))
    return frames

class Player:
    def __init__(self, x, y, left_key, right_key, jump_key, run_key):
        self.pos_x = x
        self.pos_y = y
        self.vitesse_y = 0
        self.in_air = False
        self.etat = "idle"
        self.frame_index = 0
        self.is_attacking = False
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
            "attack": load_frames("attack"),
            "dodge": load_frames("dodge")
        }

        self.image = self.frames_dict["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos_x, self.pos_y)

    def update(self, touches):
        if self.is_dodging:
            self._update_dodge()
            return

        self.etat = "idle"
        courir = touches[self.run_key]

        if touches[pygame.K_s] and not self.in_air and not self.is_charging_jump and not self.is_attacking:
            self.is_dodging = True
            self.frame_index = 0
            return

        if touches[pygame.K_e] and not self.is_attacking:
            self.frame_index = 0
            self.is_attacking = True

        if self.is_attacking:
            self._update_attack()
            return

        self._handle_movement(touches, courir)
        self._handle_jump(touches)
        self._apply_gravity()
        self._update_animation()

    def _handle_movement(self, touches, courir):
        if not self.is_charging_jump:
            if touches[self.left_key] and self.pos_x > 0:
                self.pos_x -= CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
                self.etat = "run" if courir else "walk"
                self.last_dir = "left"
                self.facing_left = True
            elif touches[self.right_key] and self.pos_x < CONFIG["WINDOW_WIDTH"]:
                self.pos_x += CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
                self.etat = "run" if courir else "walk"
                self.last_dir = "right"
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

    def _update_attack(self):
        self.etat = "attack"
        self.frame_index += CONFIG["ANIMATION_SPEED"]
        if self.frame_index >= len(self.frames_dict["attack"]):
            self.frame_index = 0
            self.is_attacking = False
        self._apply_gravity()

    def _update_dodge(self):
        self.etat = "dodge"
        self.frame_index += CONFIG["ANIMATION_SPEED"]
        recul = 10
        if self.last_dir == "right":
            self.pos_x -= recul
            if self.pos_x < 0:
                self.pos_x = 0
        else:
            self.pos_x += recul
            if self.pos_x > CONFIG["WINDOW_WIDTH"]:
                self.pos_x = CONFIG["WINDOW_WIDTH"]
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

    joueur1.update(touches)
    joueur1.draw(fenetre)
    joueur1.draw_health_bar(fenetre, 20, 20)

    pygame.draw.rect(fenetre, BLEU, joueur2)
    pygame.display.flip()

pygame.quit()
sys.exit() 