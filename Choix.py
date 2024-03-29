import pygame
from pygame import gfxdraw
from math import sqrt
from shapely import *
from tangramSolver import *
import numpy as np
from tangram import *
from créerFond import *

pygame.init()

# test 2


class Choix:
    def __init__(self, screen):
        #screen
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        #fond
        self.fond = pygame.image.load('image/fond.png')
        self.rect = self.fond.get_rect(topleft=(0, 0))

        #bouton carré basique
        self.carre_basique=pygame.image.load('image/carre_basique.png')

        self.carre_width = self.carre_basique.get_width()
        self.carre_height = self.carre_basique.get_height()
        
        #bouton Multipolygon
        
        self.multipolygon=pygame.image.load('image/multipolygone.png')
        
        self.multipolygon_width = self.multipolygon.get_width()
        self.multipolygon_height = self.multipolygon.get_height()
        
        #bouton chameau
        
        self.chat=pygame.image.load('image/chat.png')

        self.chat_width = self.chat.get_width()
        self.chat_height = self.chat.get_height()
        
        #bouton lapin
        
        self.lapin=pygame.image.load('image/lapin.png')
        
        self.lapin_width = self.lapin.get_width()
        self.lapin_height = self.lapin.get_height()
        
        #bouton ours
        
        self.ours=pygame.image.load('image/ours.png')
        
        self.ours_width = self.ours.get_width()
        self.ours_height = self.ours.get_height()
        
        #bouton forme construite
        
        self.forme_construite=pygame.image.load('image/formeConstruite.png')
        
        self.forme_construite_width = self.forme_construite.get_width()
        self.forme_construite_height = self.forme_construite.get_height()
        
        #Bouton forme 4 pieces
        
        self.forme_4_pieces=pygame.image.load('image/forme_4_pieces.png')
        
        self.forme_4_pieces_width = self.forme_4_pieces.get_width()
        self.forme_4_pieces_height = self.forme_4_pieces.get_height()
        
        #taille de la fenetre
        window_width, window_height = screen.get_size()

        #position des boutons centré
        self.carre_x =( (window_width - self.carre_width) // 2)
        self.carre_y =( (window_height - self.carre_height) // 2)-150
        
        self.multipolygon_x =( (window_width - self.multipolygon_width) // 2)
        self.multipolygon_y =( (window_height - self.multipolygon_height) // 2)-100
        
        self.chat_x =( (window_width - self.chat_width) // 2)
        self.chat_y =( (window_height - self.chat_height) // 2)-50
        
        self.lapin_x =( (window_width - self.lapin_width) // 2)
        self.lapin_y =( (window_height - self.lapin_height) // 2)
        
        self.ours_x =( (window_width - self.ours_width) // 2)
        self.ours_y =( (window_height - self.ours_height) // 2)+50
        
        self.forme_construite_x =( (window_width - self.forme_construite_width) // 2)
        self.forme_construite_y =( (window_height - self.forme_construite_height) // 2)+100
        
        self.forme_4_pieces_x =( (window_width - self.forme_4_pieces_width) // 2)
        self.forme_4_pieces_y =( (window_height - self.forme_4_pieces_height) // 2)+150
        
        self.rect1 = self.carre_basique.get_rect(topleft=(self.carre_x, self.carre_y))
        self.mask_carre = pygame.mask.from_surface(self.carre_basique)
        
        self.rect2 = self.multipolygon.get_rect(topleft=(self.multipolygon_x, self.multipolygon_y))
        self.mask_multipolygon = pygame.mask.from_surface(self.multipolygon)
        
        self.rect3 = self.chat.get_rect(topleft=(self.chat_x, self.chat_y))
        self.mask_chat = pygame.mask.from_surface(self.chat)
        
        self.rect4 = self.lapin.get_rect(topleft=(self.lapin_x, self.lapin_y))
        self.mask_lapin = pygame.mask.from_surface(self.lapin)
        
        self.rect5 = self.ours.get_rect(topleft=(self.ours_x, self.ours_y))
        self.mask_ours = pygame.mask.from_surface(self.ours)
        
        self.rect6 = self.forme_construite.get_rect(topleft=(self.forme_construite_x, self.forme_construite_y))
        self.mask_forme_construite = pygame.mask.from_surface(self.forme_construite)
        
        self.rect7 = self.forme_4_pieces.get_rect(topleft=(self.forme_4_pieces_x, self.forme_4_pieces_y))
        self.mask_forme_4_pieces = pygame.mask.from_surface(self.forme_4_pieces)
        
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
        #Si on clique sur le bouton carré basique
        if (self.carre_x <= x < self.carre_x + self.carre_width) and (self.carre_y <= y < self.carre_y + self.carre_height):
            print("carre")
            self.runTangram("carre")
        #Si on clique sur le bouton multipolygon
        if (self.multipolygon_x <= x < self.multipolygon_x + self.multipolygon_width) and (self.multipolygon_y <= y < self.multipolygon_y + self.multipolygon_height):
            print("multipolygon")
            self.runTangram("multipolygon")
        #Si on clique sur le bouton chat
        if (self.chat_x <= x < self.chat_x + self.chat_width) and (self.chat_y <= y < self.chat_y + self.chat_height):
            print("chat")
            self.runTangram("chat")
        #Si on clique sur le bouton lapin
        if (self.lapin_x <= x < self.lapin_x + self.lapin_width) and (self.lapin_y <= y < self.lapin_y + self.lapin_height):
            print("lapin")
            self.runTangram("lapin")
        #Si on clique sur le bouton ours
        if (self.ours_x <= x < self.ours_x + self.ours_width) and (self.ours_y <= y < self.ours_y + self.ours_height):
            print("ours")
            self.runTangram("ours")
        #Si on clique sur le bouton forme construite
        if (self.forme_construite_x <= x < self.forme_construite_x + self.forme_construite_width) and (self.forme_construite_y <= y < self.forme_construite_y + self.forme_construite_height):
            print("forme construite")
            self.runTangram("forme construite")
        #Si on clique sur le bouton forme 4 pieces
        if (self.forme_4_pieces_x <= x < self.forme_4_pieces_x + self.forme_4_pieces_width) and (self.forme_4_pieces_y <= y < self.forme_4_pieces_y + self.forme_4_pieces_height):
            print("forme 4 pieces")
            self.runTangram("forme 4 pieces")
            

    #fonction qui affiche les boutons
    def display(self, screen):
        
        screen.blit(self.fond, self.rect.topleft)
        screen.blit(self.carre_basique,self.rect1.topleft)
        screen.blit(self.multipolygon,self.rect2.topleft)
        screen.blit(self.chat,self.rect3.topleft)
        screen.blit(self.lapin,self.rect4.topleft)
        screen.blit(self.ours,self.rect5.topleft)
        screen.blit(self.forme_construite,self.rect6.topleft)
        screen.blit(self.forme_4_pieces,self.rect7.topleft)
        pygame.display.flip()

    #fonction qui lance le jeu
    def runTangram(self,fond):
        screen = self.screen
        tan = TangramGame(720,480,fond)
        tan.run()

    #fonction qui lance le launcher
    def run(self):
        while self.running:
            self.events()
            self.display(self.screen)
            self.clock.tick(60)



pygame.quit()

