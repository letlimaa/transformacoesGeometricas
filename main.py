import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Cube import wireCube

pygame.init()

# Configurações da tela
screen_width = 1200 
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL in Python - Reflexão e Animação")

# Variáveis (translação vertical)
cube1_x = -3.0  
cube1_y = 0.0
cube1_z = -5.0  # Posição inicial
move_speed = 0.03
y_direction = 1
y_boundary = 1.5

# Variáveis (espelhamento no eixo Y)
cube_y = 0.0
scale_y = 1.0

# Variáveis (escala e rotação)
cube2_x = 3.0 
escala = 1.0
encolher = True
escala_speed = 0.01

def initialise():
    glClearColor(*background_color)
    glColor(*drawing_color)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)


def display():
    global cube1_y, y_direction, escala, encolher, cube_y, scale_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5.0)

    # Cubo 1: Translação vertical
    glPushMatrix()
    glTranslatef(cube1_x, cube1_y, 0)
    wireCube() 
    glPopMatrix()

    # Atualiza posição do primeiro cubo
    cube1_y += move_speed * y_direction
    if cube1_y > y_boundary or cube1_y < -y_boundary:
        y_direction *= -1
        cube1_y = y_boundary if cube1_y > y_boundary else -y_boundary

    # Cubo 2: Espelhamento no eixo Y
    glPushMatrix()
    glTranslatef(0, cube_y, 0)
    glScalef(1.0, scale_y, 1.0)
    wireCube()
    glPopMatrix()
    
    # Atualiza posição e reflexão
    cube_y += move_speed * y_direction
    if abs(cube_y) >= y_boundary:
        y_direction *= -1
        scale_y *= -1  # Espelha no eixo Y ao atingir a borda

    # Cubo 3: Escala e rotação
    glPushMatrix()
    glTranslatef(cube2_x, 0.0, 0.0)
    glRotatef(pygame.time.get_ticks() / 50, 10, 0, 1)
    glScalef(escala, escala, escala)
    wireCube()
    glPopMatrix()

    # Atualiza a escala do terceiro cubo
    if encolher:
        escala -= escala_speed
        if escala <= 1.0:
            encolher = False
    else:
        escala += escala_speed
        if escala >= 1.5:
            encolher = True


done = False
initialise()
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cube1_y += move_speed * 5
            elif event.key == pygame.K_DOWN:
                cube1_y -= move_speed * 5

    display()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
