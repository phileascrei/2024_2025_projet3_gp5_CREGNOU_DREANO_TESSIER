from data import sprite_file, animations_data, CONFIG
import pygame

# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption("Marvel - Captain America")


sprite_sheet = pygame.image.load(sprite_file).convert_alpha()

def get_frame(x, y, largeur, hauteur):
    frame = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (x, y, largeur, hauteur))
    frame.set_colorkey((0,255,1,255))
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