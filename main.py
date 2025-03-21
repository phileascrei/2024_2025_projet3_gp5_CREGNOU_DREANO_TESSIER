import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
 
from pynput.keyboard import Key, Controller
 
# Fonction pour dessiner un cube
def draw_cube():
    glBegin(GL_QUADS)
     
    # Face avant
    glColor3f(1, 0, 0)  # Rouge
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
     
    # Face arrière
    glColor3f(0, 1, 0)  # Vert
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
     
    # Face gauche
    glColor3f(0, 0, 1)  # Bleu
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
     
    # Face droite
    glColor3f(1, 1, 0)  # Jaune
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
     
    # Face supérieure
    glColor3f(1, 0, 1)  # Magenta
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
     
    # Face inférieure
    glColor3f(0, 1, 1)  # Cyan
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
     
    glEnd()
 
# Fonction pour gérer les événements du clavier
def handle_keys():
    keys = pygame.key.get_pressed()
 
    if keys[pygame.K_z]:
        glTranslatef(0, 0, 0.1)  # Avancer
    if keys[pygame.K_s]:
        glTranslatef(0, 0, -0.1)  # Reculer
    if keys[pygame.K_q]:
        glTranslatef(0.1, 0, 0)  # Gauche
    if keys[pygame.K_d]:
        glTranslatef(-0.1, 0, 0)  # Droite
 

def rotation_cube () :
    pass 




# Initialiser Pygame et OpenGL
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Jeu 3D avec Pygame et PyOpenGL")
 
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
 
# Variables pour la rotation
angle = 0
keyboard = Controller()

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
    handle_keys()
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
    # Appliquer une rotation et dessiner le cube
    glPushMatrix()
    glRotatef(angle, 0, 1, 0)  # Rotation sur l'axe Y
    draw_cube()
    glPopMatrix()
 
    # angle += 1  # Incrémenter l'angle de rotation


    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        angle += 1
    if keys[pygame.K_a]:
        angle -= 1

    pygame.display.flip()
    pygame.time.wait(10)
 
pygame.quit()