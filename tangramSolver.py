from shapely import *
import pygame
from time import sleep
from Piece import Piece
from math import sqrt

reduction_factor = 1

#   rouding security
EPSILON = 10
ROTATION_GAP = 45
SMALL_AREA = 0.1

already_tested = []

# Créez les pièces du Tangram
bigTriangle1 = Piece(Polygon([(0, 0), (100, 0), (0, 100)]), 0, (0, 255, 154))
bigTriangle2 = Piece(Polygon([(0, 0), (100, 0), (0, 100)]), 1, (255, 154, 0))
mediumTriangle = Piece(Polygon([(0, 0), (50*sqrt(2), 0), (0, 50*sqrt(2))]), 2, (255, 0, 0))
smallTriangle1 = Piece(Polygon([(0, 0), (50, 0), (0, 50)]), 3, (189, 126, 0))
smallTriangle2 = Piece(Polygon([(0, 0), (50, 0), (0, 50)]), 4, (189, 0, 145))
square = Piece(Polygon([(0, 0), (50, 0), (50, 50), (0, 50)]), 5, (247, 255, 0))
trapeze = Piece(Polygon([(0, 0), (50, -50), (50, 0), (0, 50)]), 6, (0, 0, 204))
trapezeInversed = Piece(Polygon([(0, 0), (50, 50), (50, 0), (0, -50)]), 6, (0, 0, 204))

tangramPieces = [bigTriangle1,bigTriangle2,mediumTriangle,smallTriangle1,smallTriangle2,square,trapeze,trapezeInversed]

# Ajustez la taille de chaque pièce
for piece in tangramPieces:
    piece.scale(reduction_factor)

#Résolution du tangram
def solveTangram(shape,polys,screen):
    solution = []
    #On vérifie si la forme est un multipolygone ou un polygone et on résout en fonction
    if shape.geom_type == "MultiPolygon":
        solution = solveMultipolygon(shape,polys,screen)
    else:
        solution = solvePolygon(shape,polys,screen)
    return solution

#Résolution du multipolygone
def solveMultipolygon(multi_shapes,polys,screen):
    solution = []
    shapes = list(multi_shapes.geoms)
    for shape in shapes:
        local_solution = solvePolygon(shape,polys,screen)
        # S'il n'existe pas de solution pour le multipolygon alors rien ne sert de résoudre le reste des polygones
        if local_solution == None:
            return None
        solution.extend(local_solution)
        for sol in local_solution:
            polys = removePiece(polys,sol)
    return solution
    
#Résolution du polygone
def solvePolygon(shape,polys,screen):
    solution = []

    if shape.is_empty or shape.area < SMALL_AREA:
        return solution
    for shapePoint in shape.exterior.coords:
        polygons = polys.copy()
        for polygon in polygons:
            polygon.reset()
        while polygons:
            selectedPolygonReal,polygons = selectPolygon(shape,shapePoint,polygons)

            if(selectedPolygonReal == None):
                break
            selectedPolygon = selectedPolygonReal.copy()
            selectedPolygonReal.nextPosition(ROTATION_GAP)
            selectedPolygon.moveToPoint(shapePoint)

            # ####
            screen.fill((255,255,255))
            selectedPolygon.display(screen)
            ####


            difference = shape.difference(selectedPolygon.getPoly())
            #####   bug Fix ######
            if difference.geom_type == "GeometryCollection":
                for geom in difference.geoms:
                    if(geom.geom_type in ["MultiPolygon","Polygon"]):
                        difference = geom
                        break
            
            # difference = roundShape(difference,2)
            displayShape(difference,screen)

            # use the poly list because polygons list delete pieces as they don't fit
            sub_list = createSubList(polys,selectedPolygon)
            nextPolys = None

            if not checkTested(difference,sub_list):
                nextPolys = solveTangram(difference,sub_list,screen)

            if(nextPolys != None):
                solution.append(selectedPolygon)
                solution.extend(nextPolys)
                
                return solution
        #free memory for optimisation
        for poly in polygons:
            del(poly)
        del(polygons)
    saveTested(shape,polys.copy())
    for poly in polys:
        del(poly)
    del polys
    
    return None
    
#Enleve une pièce de la liste
def removePiece(list,piece):
    ret = []
    for p in list:
        if p.id != piece.id:
            ret.append(p)
    return ret

#Affiche la forme
def displayShape(shape,screen):
    if not shape.is_empty and shape.geom_type != "MultiPolygon":
        pygame.gfxdraw.filled_polygon(screen, shape.exterior.coords,(0,0,150))
        pygame.gfxdraw.aapolygon(screen, shape.exterior.coords,(0,0,150))
        pygame.display.update()

#Renvoi le polygone réel correspondant au polygone sélectionné
def getRealPoly(selected,polys):
    for poly in polys:
        if selected.id == poly.id:
            return poly

#Crée une sous liste sans la pièce sélectionnée
def createSubList(polygons,selectedPolygon):
    # print("create sub_list without n°" + str(selectedPolygon.id))
    sub_list = []
    for poly in polygons:
        if selectedPolygon.id != poly.id:
            resetedPoly = poly.copy()
            resetedPoly.reset()
            sub_list.append(resetedPoly)
    return sub_list

#Renvoi le polygone sélectionné et la liste des polygones restants
def selectPolygon(shape,point,polygons):
    selectedPolygon = None
    new_polygon_list = []
    found = False

    for p in polygons:
        if found:
            new_polygon_list.append(p)
        else:
            found = checkPiece(shape,point,p)
            if found:
                selectedPolygon = p

    return (selectedPolygon,new_polygon_list)
    
#Verifie si une pièce est dans la forme
def checkPiece(shape,point,piece):
    while not piece.allPositionUsed():
        if polygonIn(shape,point,piece):
            return True
        piece.nextPosition(ROTATION_GAP)
    return False

#Verifie si un polygone est dans la forme
def polygonIn(shape,point,piece):
    piece.moveToPoint(point)
    return fullyIn(piece.getPoly(),shape)

#   detects if a polygon is fully into another
#   returns true or false
def fullyIn(polygon,shape):

    multishape = MultiPolygon([shape])
    if not shape.is_valid:
        make_valid(shape)
        if not shape.is_valid:
            print("error")
    if not multishape.intersection(polygon).is_empty:
        intersection = multishape.intersection(polygon)
        if(abs(intersection.area - polygon.area) <= EPSILON):
            return True
        else:
            return False
    else:
        return False

#Crée une forme valide
def roundShape(shape,digit):
    if shape.geom_type == "MultiPolygon":
        shapes = list(shape.geoms)
        for poly in shapes:
            poly = roundPoly(poly,digit)
    else:
        shape = roundPoly(shape,digit)
    return shape
    
#Crée un polygone valide
def roundPoly(poly,digit):
    if poly.area < SMALL_AREA:
        return Polygon()
    coords = poly.exterior.coords[:]
    for i in range(len(coords)):
        x,y = coords[i]
        coords[i] = (round(x,digit),round(y,digit))
    poly = Polygon(coords)
    make_valid(poly)
    return poly

#Verifie si une forme est valide
def checkTested(shape,polygons):
    ids = []
    for poly in polygons:
        if poly.id == 1:
            ids.append(0)
        if poly.id == 4:
            ids.append(3)
        else:
            ids.append(poly.id)
    ids.sort()
    for tested in already_tested:
        if tested[0].equals_exact(shape, SMALL_AREA) and ids == tested[1]:
            print("avoided")
            return True
    return False

#Sauvegarde une forme testée
def saveTested(shape,polygons):
    ids = []
    for poly in polygons:
        if poly.id == 1:
            ids.append(0)
        if poly.id == 4:
            ids.append(3)
        else:
            ids.append(poly.id)
    ids.sort()
    already_tested.append([shape,ids])