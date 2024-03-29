import pygame
from shapely import *
from Piece import Piece
from EventManager import EventManager
from DisplayManager import DisplayManager
from ShapeGestion import ShapeGestion

class TangramConstructor():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tangram')

        shape = Polygon([(0, 565.685424949238), (565.685424949238, 565.685424949238), (565.685424949238, 0), (400, 0), (0, 400), (0, 565.685424949238)])
        bigTriangle1 = Piece(Polygon([(0, 0), (400, 0), (0, 400)]), (0, 255, 154))
        bigTriangle2 = Piece(Polygon([(0, 0), (400, 0), (0, 400)]), (255, 154, 0))

        p1 = Piece(shape, (255, 0, 0))

        self.pieces = [p1, bigTriangle1, bigTriangle2]

    def run(self):
        ShapeGestion.saveFile("res/data.json", self.pieces[0].poly)
        ShapeGestion.importFile("res/data.json")
        
        eventManager = EventManager(self.pieces)
        displayManager = DisplayManager(self.pieces)

        while eventManager.running:
            eventManager.Event()
            displayManager.Update(self.screen)
    