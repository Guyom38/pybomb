 
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
        if self.obstacle == ENUM_TYPE.AUCUN : return True
        if self.obstacle == ENUM_TYPE.BRICK_CASSEE: return True
        return False
    
    def set_obstacle(self, valeur):
        if valeur == ENUM_TYPE.AUCUN:
            self.animation.set_action(FCT.iif(self.animation.x % 2 == 0 or self.animation.y % 2 == 0, "SOL1", "SOL2"))
        elif valeur == ENUM_TYPE.BRICK:
            self.animation.set_action("BRICK")
        elif valeur == ENUM_TYPE.MUR:
            self.animation.set_action("SOLIDE")
            
    def afficher(self, coucheHaute):
        if coucheHaute and self.obstacle == ENUM_TYPE.AUCUN: return 0
        if self.obstacle == ENUM_TYPE.BRICK_CASSEE and not self.animation.etat: return 0
        
        pX = int(VAR.offSetX + (self.animation.x * VAR.pas))
        pY = int(VAR.offSetY + (self.animation.y * VAR.pas))
        
        VAR.fenetre.blit(VAR.IMG[self.animation.sprite()], (pX, pY))
                 