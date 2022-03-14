 
import pygame
from pygame.locals import *

from Terrain.surface import CSurface
from Objet.objet import *

import variables as VAR
from variables import *

import fonctions as FCT

import random

class CTerrain():
    def __init__(self, dimX = 20, dimY = 16, bricks = 40, objets = 80, vide = False):
        print("CTerrain")
        
        self.pX, self.pY = -1, -1
        self.maxX, self.maxY = -1, -1
        self.minX, self.minY = -1, -1
        self.direction = 0
        
        self.cycle = 0
        self.frequence = 300
        
        self.cycleInterval = 0
        self.frequenceInterval = 200
        
        self.initialiser( dimX, dimY, bricks , objets , vide)
    
    def initialiser(self, dimX = 20, dimY = 16, bricks = 40, objets = 80, vide = False):   
        print("    + initialiser") 
        self.reglageBricks = bricks
        self.reglageObjets = objets   
         
        VAR.dimensionX = dimX
        VAR.dimensionY = dimY  
        self.zone = FCT.GenereMat2D(dimX, dimY, None)
        
        if not vide:
            obj = 0

            for y in range(0, VAR.dimensionY):
                for x in range(0, VAR.dimensionX):
                    obstacle = ENUM_TYPE.AUCUN
                    objet = ENUM_OBJET.AUCUN
                    
                    if y == 0 or y == VAR.dimensionY: obstacle = ENUM_TYPE.MUR
                    if x == 0 or x == VAR.dimensionX: obstacle = ENUM_TYPE.MUR
                    if x % 2 == 0 and y % 2 == 0: obstacle = ENUM_TYPE.MUR
                    
                    if obstacle == ENUM_TYPE.AUCUN:
                        if random.randint(0, 100) < self.reglageBricks:
                            obstacle = ENUM_TYPE.MUR
                            
                            if random.randint(0, 100) < self.reglageObjets:
                                objet = random.choice((ENUM_OBJET.BOMBE, ENUM_OBJET.FLAMME, ENUM_OBJET.ROLLER))
                                obj +=1
                    
                    self.zone[x][y] = CSurface(x, y, obstacle, CObjet(obj, x, y, objet))
    
    def afficher_couche_haute(self):
        for y in range(0, VAR.dimensionY):
            for x in range(0, VAR.dimensionX):
                self.zone[x][y].afficher(True)

                if not self.zone[x][y].animation.etat and (self.zone[x][y].obstacle == ENUM_TYPE.BRICK_CASSEE or self.zone[x][y].traversable()):
                    self.zone[x][y].objet.afficher()

    def afficher_couche_basse(self):        
        for y2 in range(VAR.dimensionY):
            for x2 in range(VAR.dimensionX):
                x = VAR.offSetX + (x2 * VAR.pas)
                y = VAR.offSetY + (y2 * VAR.pas)

                if self.zone[x2][y2].traversable():
                    if x2 % 2 == 0 or y2 % 2 == 0:
                        VAR.fenetre.blit(VAR.IMG[606], (x, y))
                    else:
                        VAR.fenetre.blit(VAR.IMG[607], (x, y))

    def collision_decors(self, x, y, graph = False):
        pas = VAR.pas

        tX = int(x)
        tY = int(y)

        for nY in range (tY-1, tY+1):
            for nX in range (tX -1, tX +1):
                if not (nX == tX and nY == tY):
                    if not self.en_dehors_terrain(nX, nY):
                        if not self.zone[nX][nY].traversable():
                            if FCT.collision(nX * pas, nY * pas, pas, pas, int(x * pas) +8, int(y*pas)+8, pas - 16, pas - 16): 
                                return True
        return False
    
    def en_dehors_terrain(self, x, y):
        if x < 0 or x > VAR.dimensionX: return True
        if y < 0 or y > VAR.dimensionY: return True
        return False

    def destruction_timing(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            if self.pX == -1:
                self.maxX = VAR.dimensionX -1
                self.maxY = VAR.dimensionY -1
                self.minX = 1
                self.minY = 1

                self.pX = 1
                self.pY = 1

                self.direction = 0

            if pygame.time.get_ticks() - self.cycleInterval > self.frequenceInterval:
                self.cycleInterval = pygame.time.get_ticks()
                self.zone[self.pX][self.pY].set_obstacle(ENUM_TYPE.MUR)

                for perso in VAR.personnages:
                    if int(perso.animation.x) == self.pX and int(perso.animation.y) == self.pY:
                        perso.animation.set_action("MOURRIR")
                        perso.animation.etat = True

                if self.direction == 0:
                    if self.pX < self.maxX:
                        self.pX +=1
                    else:
                        self.direction = 1
                        self.minX +=1
                elif self.direction == 1:
                    if self.pY < self.maxY:
                        self.pY +=1
                    else:
                        self.direction = 2
                        self.minY +=1   
                elif self.direction == 2:
                    if self.pX >= self.maxX:
                        self.pX -=1
                    else:
                        self.direction = 3
                        self.minX -=1         
                elif self.direction == 3:
                    if self.pY >= self.maxY:
                        self.pY -1
                    else:
                        self.direction = 0
                        self.minY -=1                  
