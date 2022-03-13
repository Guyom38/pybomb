 
import pygame
from pygame.locals import *
from Animation.animation import CAnimation

import variables as VAR
from variables import *

import fonctions as FCT

class CSurface():
    def __init__(self, x, y, obstacle, objet):

        self.animation = CAnimation(ENUM_CHOIX.SURFACE)
        self.animation.x, self.animation.y = x, y
        
        self.obstacle = obstacle
        self.objet = objet
        
    def traversable(self):
        return (self.obstacle == ENUM_TYPE.AUCUN or self.obstacle == ENUM_TYPE.BRICK_CASSEE)
    
    def get_obstacle(self):
        return self.obstacle
    
    def set_obstacle(self, valeur):
        if valeur == ENUM_TYPE.AUCUN:
            self.animation.action = FCT.iif(self.animation.x % 2 == 0 or self.animation.y % 2 == 0, "SOL1", "SOL2")
        elif valeur == ENUM_TYPE.BRICK:
            self.animation.action = "BRICK"
        elif valeur == ENUM_TYPE.MUR:
            self.animation.action = "SOLIDE"
            
    def afficher(self, coucheHaute):
        if coucheHaute and self.obstacle == ENUM_TYPE.AUCUN: return 0
        if self.obstacle == ENUM_TYPE.BRICK_CASSEE and not self.animation.etat: return 0
        
        pX = int(VAR.offSetX + (self.animation.x * VAR.pas))
        pY = int(VAR.offSetY + (self.animation.y * VAR.pas))
        
        VAR.fenetre.blit(VAR.IMG[self.animation.sprite], pX, pY)
                 