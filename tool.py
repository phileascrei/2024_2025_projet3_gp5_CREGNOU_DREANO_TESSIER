import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
speed = 300
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
target_pos = pygame.Vector2(0, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.circle(screen, "green", target_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_q]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    
    if pygame.mouse.get_pressed()[2]:
        target_pos = pygame.Vector2(pygame.mouse.get_pos())
    
    # if target_pos != player_pos:
    #     direction = target_pos - player_pos
    #     direction.normalize_ip()
    #     player_pos += direction * 300 * dt


    if target_pos != player_pos:
    # Calculer la direction entre player_pos et target_pos
        direction = target_pos - player_pos
        distance = direction.length()
        
        if distance > 5:  # Seuil de distance pour éviter les tremblements
            direction.normalize_ip()  # Normaliser in-place
            player_pos += direction * speed * dt
        else:
            # Si la distance est trop petite, juste placer le joueur sur la cible pour éviter les tremblements
            player_pos = target_pos


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit() 