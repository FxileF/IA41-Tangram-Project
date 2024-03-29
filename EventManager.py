import pygame
from shapely import *

class EventManager():
    def __init__(self,_pieces):
        self.pieces = _pieces
        self.running = True
        self.pieceHeld = None

    # Fonction qui gère les évènements
    def Event(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    break
                case pygame.MOUSEBUTTONDOWN:
                    self.OnMouseDown()
                case pygame.MOUSEBUTTONUP:
                    self.OnMouseUp()
                case pygame.KEYDOWN:
                    self.OnKeyDown(event.key)
        
        if(self.pieceHeld != None):
            self.OnGrab()
            

    def OnKeyDown(self, key):
        if key == pygame.K_LEFT:
            self.RotatePiece(-5.0)  # Rotation vers la gauche (angle négatif)
        elif key == pygame.K_RIGHT:
            self.RotatePiece(5.0)   # Rotation vers la droite (angle positif)

    # Fonction qui gère les évènements de la souris
    def RotatePiece(self, angle):
        # Si une pièce est tenue
        if self.pieceHeld != None:
            otherPieces = self.pieces.copy()
            otherPieces.remove(self.pieceHeld)
            if self.pieceHeld:
                self.pieceHeld.rotate_input(angle,otherPieces)

    # Fonction qui gère les évènements de la souris
    def OnMouseDown(self):
        mousePos = pygame.mouse.get_pos()
        mousePosPoint = Point(mousePos)
        for piece in self.pieces:
            if(mousePosPoint.within(piece.poly)):
                self.pieceHeld = piece
                piece.OnMouseDown(mousePos)
    
    def OnMouseUp(self):
        if(self.pieceHeld != None):
            self.pieceHeld.OnMouseUp()
        self.pieceHeld = None

    def OnGrab(self):
        otherPieces = self.pieces.copy()
        otherPieces.remove(self.pieceHeld)
        self.pieceHeld.OnGrab(pygame.mouse.get_pos(),otherPieces)
