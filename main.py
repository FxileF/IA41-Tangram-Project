import pygame
from pygame import gfxdraw
from math import sqrt
from shapely import *
from tangramSolver import *
import numpy as np
from launcher import *

pygame.init()

background_colour = (255,255,255)
pygame.display.set_caption('Tangram')
running = True

screen_taille = (720, 480)

screen = pygame.display.set_mode(screen_taille)
#lancement du launcher
Launcher = launcher(screen)
Launcher.run()
