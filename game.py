import pygame
import pytmx
import pyscroll
from player import Player

class Game:

    def __init__(self):
        #fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeux 2D")

        #charger la carte


        #générer le joueur
        self.player = Player()

    def run(self):
        #garder la fenêtre ouverte
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()