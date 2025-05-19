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
    y_offset = data.get("line", 0)
    frames_per_row = data.get("frames_per_row", data["frames"])
    # Nouvelle clé optionnelle pour la 2e ligne
    y_offset2 = data.get("line2", None)

    if "widths" in data:
        for i, width in enumerate(data["widths"]):
            # Si on passe à la 2e ligne et "line2" existe, on l'utilise
            if (i == frames_per_row) and y_offset2 is not None:
                x_offset = 0
                y_offset = y_offset2
            frames.append(get_frame(x_offset, y_offset, width, data["height"]))
            x_offset += width
            if (i + 1) % frames_per_row == 0 and i + 1 != len(data["widths"]):
                x_offset = 0
                # Si "line2" n'existe pas, on continue comme avant
                if y_offset2 is None:
                    y_offset += data["height"]
    else:
        for i in range(data["frames"]):
            if (i == frames_per_row) and y_offset2 is not None:
                x_offset = 0
                y_offset = y_offset2
            frames.append(get_frame(x_offset, y_offset, data["width"], data["height"]))
            x_offset += data["width"]
            if (i + 1) % frames_per_row == 0 and i + 1 != data["frames"]:
                x_offset = 0
                if y_offset2 is None:
                    y_offset += data["height"]
    return frames