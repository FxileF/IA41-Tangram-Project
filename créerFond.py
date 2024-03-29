from shapely import *
import pygame
from Piece import Piece
from EventManager import EventManager
from DisplayManager import DisplayManager
from ShapeGestion import ShapeGestion

# Classe qui gère la création du Tangram
class TangramConstructor():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tangram')

        

    # Fonction qui lance le jeu
    def run(self):
        #On crée les pieces du tangram
        self.pieces=ShapeGestion.importFile("res/data.json")
        
        eventManager = EventManager(self.pieces)
        displayManager = DisplayManager(self.pieces)

        while eventManager.running:
            eventManager.Event()
            displayManager.Update(self.screen)
            
        ShapeGestion.saveFile("res/data.json", self.pieces)