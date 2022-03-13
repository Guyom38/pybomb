 
import pygame
from pygame.locals import *

from Terrain.surface import CSurface
import Objet.objet import *

import variables as VAR
from variables import *

import fonctions as FCT

import random

class CTerrain():
    def __init__(self, dimX = 20, dimY = 16, bricks = 40, objets = 80, vide = False):
        
        
        self.pX, self.pY = -1, -1
        self.maxX, self.maxY = -1, -1
        self.minX, self.minY = -1, -1
        self.direction = 0
        
        self.cycle = 0
        self.frequence = 300
        
        self.cycleInterval = 0
        self.frequenceInterval = 200
        
        self.initialiser()
    
    def initialiser(self, dimX = 20, dimY = 16, bricks = 40, objets = 80, vide = False):    
        self.reglageBricks = bricks
        self.reglageObjets = objets   
         
        VAR.dimensionX = dimX
        VAR.dimensionY = dimY  
        self.zone = FCT.GenereMat2D(dimX, dimY)
        
        if not vide:
            obj = 0
            for y in range(0, VAR.dimensionY):
                for x in range(0, VAR.dimensionX):
                    obstacle = ENUM_TYPE.AUCUN
                    objet = ENUM_OBJET.AUCUN
                    
                    if self.y == 0 or self.y == VAR.dimensionY: obstacle = ENUM_TYPE.MUR
                    if self.x == 0 or self.x == VAR.dimensionX: obstacle = ENUM_TYPE.MUR
                    if self.x % 2 == 0 and self.y % 2 == 0: obstacle = ENUM_TYPE.MUR
                    
                    if obstacle == ENUM_TYPE.AUCUN:
                        if random.randint(0, 100) < self.reglageBricks:
                            obstacle = ENUM_TYPE.MUR
                            
                            if random.randint(0, 100) < self.reglageObjets:
                                objet = random.choices((ENUM_OBJET.BOMBE, ENUM_OBJET.FLAMME, ENUM_OBJET.ROLLER))
                                obj +=1
                    
                    self.zone[x][y] = CSurface(x, y, obstacle, CObjet(obj, x, y, objet))
    
    def afficher_couche_Haute(self):
        for y in range(0, VAR.dimensionY):
            for x in range(0, VAR.dimensionX):
                self.zone[x][y].afficher(True)