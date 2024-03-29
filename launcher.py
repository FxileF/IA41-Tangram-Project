import pygame
from pygame import gfxdraw
from math import sqrt
from shapely import *
from tangramSolver import *
import numpy as np
from tangram import *
from créerFond import *
from Choix import *

pygame.init()

# test 2


class launcher:
    def __init__(self, screen):
        #screen
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        #fond
        self.fond = pygame.image.load('image/fond.png')
        self.rect = self.fond.get_rect(topleft=(0, 0))

        #bouton resoudre
        self.resoudre=pygame.image.load('image/resoudre.png')

        self.resoudre_width = self.resoudre.get_width()
        self.resoudre_height = self.resoudre.get_height()

        #bouton creer un tangram
        self.creer=pygame.image.load('image/creerUnFond.png')

        self.creer_width = self.creer.get_width()
        self.creer_height = self.creer.get_height()

        #taille de la fenetre
        window_width, window_height = screen.get_size()

        #position du bouton resoudre centré
        self.resoudre_x =( (window_width - self.resoudre_width) // 2)
        self.resoudre_y =( (window_height - self.resoudre_height) // 2)-100

        self.rect1 = self.resoudre.get_rect(topleft=(self.resoudre_x, self.resoudre_y))
        self.mask_resoudre = pygame.mask.from_surface(self.resoudre)

        #position du bouton creer un tangram centré
        self.creer_x =( (window_width - self.creer_width) // 2)
        self.creer_y =( (window_height - self.creer_height) // 2)+100

        #position du bouton creer un tangram centré
        self.rect2 = self.creer.get_rect(topleft=(self.creer_x, self.creer_y))
        self.mask_creer = pygame.mask.from_surface(self.creer)

    #fonction qui gere les evenements
    def events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    break
                case pygame.MOUSEBUTTONDOWN:
                    self.OnMouseDown()
            
    #fonction qui gere les evenements de la souris
    def OnMouseDown(self):
        (x,y) = pygame.mouse.get_pos()
        if (self.resoudre_x <= x < self.resoudre_x + self.resoudre_width) and (self.resoudre_y <= y < self.resoudre_y + self.resoudre_height):
            choix=Choix(self.screen)
            choix.run()
        elif (self.creer_x <= x < self.creer_x + self.creer_width) and (self.creer_y <= y < self.creer_y + self.creer_height):
            gameConstructor = TangramConstructor(720, 480)
            gameConstructor.run()

    #fonction qui affiche les elements
    def display(self, screen):
        
        screen.blit(self.fond, self.rect.topleft)

        screen.blit(self.resoudre,self.rect1.topleft)
        screen.blit(self.creer,self.rect2.topleft)
        pygame.display.flip()

    #fonction qui lance le jeu
    def runTangram(self):
        screen = self.screen
        tan = TangramGame(720,480)
        tan.run()

    #fonction qui lance le launcher
    def run(self):
        while self.running:
            self.events()
            self.display(self.screen)
            self.clock.tick(60)



pygame.quit()

