import data
import pygame
import sys



# === ⚙️ PARAMÈTRES GÉNÉRAUX ===
CONFIG = {
    "FPS": 60,
    "WINDOW_WIDTH": 1096,
    "WINDOW_HEIGHT": 800,
    "PLAYER_WIDTH": 100,
    "PLAYER_HEIGHT": 185,
    "PLAYER_SPEED": 5,
    "PLAYER_RUN_SPEED": 9,
    "GRAVITY": 1,
    "JUMP_FORCE": 32,
    "ANIMATION_SPEED": 0.1
}

# === 🎨 COULEURS ===
BLANC = (255, 255, 255)

# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption("Marvel - Captain America")

# === VARIABLES DU JEU ===
sol = CONFIG["WINDOW_HEIGHT"] - CONFIG["PLAYER_HEIGHT"]
joueur1 = pygame.Rect(100, sol, CONFIG["PLAYER_WIDTH"], CONFIG["PLAYER_HEIGHT"])
joueur2 = pygame.Rect(650, sol, CONFIG["PLAYER_WIDTH"], CONFIG["PLAYER_HEIGHT"])

sprite_sheet = pygame.image.load("assets/Arcade - Marvel vs Capcom - Captain America.jpg").convert_alpha()

# === ANIMATIONS ===
animations = {
    "idle": { "frames": 9, "width": 97, "height": 150, "line": 0 },
    "walk": { "frames": 6, "width": 100, "height": 140, "line": 150 },
    "run":  { "frames": 6, "width": 100, "height": 140, "line": 285 },
    "jump": { "frames": 6, "width": 100, "height": 170, "line": 420 }
}

# === FONCTIONS UTILITAIRES ===
def get_frame(x, y, largeur, hauteur):
    frame = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (x, y, largeur, hauteur))
    return frame

def load_frames(anim_name):
    frames = []
    data = animations[anim_name]

    for i in range(data["frames"]):
        frames.append(get_frame(data["width"] * i, data["line"], data["width"], data["height"]))

    return frames

# === CHARGEMENT DES FRAMES ===
idle_frames = load_frames("idle")
walk_frames = load_frames("walk")
run_frames = load_frames("run")
jump_frames = load_frames("jump")

# === VARIABLES DE JEU ===
frame_index = 0
vitesse_y1 = 0
en_lair1 = False
etat_j1 = "idle"

clock = pygame.time.Clock()
running = True

# === GAME LOOP ===
while running:
    dt = clock.tick(CONFIG["FPS"]) / 10
    fenetre.fill(BLANC)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    # Etat par défaut
    etat_j1 = "idle"
    courir = touches[pygame.K_LSHIFT] or touches[pygame.K_RSHIFT]

    # Déplacements
    if touches[pygame.K_q] and joueur1.left > 0:
        joueur1.x -= CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
        etat_j1 = "run" if courir else "walk"

    elif touches[pygame.K_d] and joueur1.right < CONFIG["WINDOW_WIDTH"]:
        joueur1.x += CONFIG["PLAYER_RUN_SPEED"] if courir else CONFIG["PLAYER_SPEED"]
        etat_j1 = "run" if courir else "walk"

    # Saut
    if touches[pygame.K_z] and not en_lair1:
        frame_index = 0
        vitesse_y1 = -CONFIG["JUMP_FORCE"]
        en_lair1 = True
        

    # Gravité
    vitesse_y1 += CONFIG["GRAVITY"]
    joueur1.y += vitesse_y1

    if joueur1.y >= sol:
        joueur1.y = sol
        vitesse_y1 = 0
        en_lair1 = False

    if en_lair1:
        etat_j1 = "jump"

    # Animation
    frame_index += CONFIG["ANIMATION_SPEED"]

    frames_dict = {
        "idle": idle_frames,
        "walk": walk_frames,
        "run": run_frames,
        "jump": jump_frames
    }

    frames = frames_dict[etat_j1]
    if frame_index >= len(frames):
        frame_index = 0

    image_j1 = frames[int(frame_index)]

    # Affichage
    fenetre.blit(image_j1, (joueur1.x, joueur1.y))
    pygame.draw.rect(fenetre, (0, 0, 200), joueur2)

    pygame.display.flip()

pygame.quit()
sys.exit()
