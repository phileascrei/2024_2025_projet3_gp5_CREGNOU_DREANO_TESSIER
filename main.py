
from Player import *
from data import *



# === INITIALISATION ===
pygame.init()
fenetre = pygame.display.set_mode((CONFIG["WINDOW_WIDTH"], CONFIG["WINDOW_HEIGHT"]))
pygame.display.set_caption("Marvel - Captain America")
sprite_sheet = pygame.image.load("assets/Arcade - Marvel vs Capcom - Captain America.jpg").convert_alpha()





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