 
import pygame
from pygame.locals import *
from Animation.animation import CAnimation

import variables as VAR
from variables import *

import fonctions as FCT

class CObjet():
    def __init__(self, id, x, y, categorie):
 
        self.maxObjets = 4
        self.animation = CAnimation(categorie)
        self.animation.x, self.animation.y = x, y
        
        self.categorie = categorie
        self.id = id
    
    
    def afficher(self):
        if self.categorie != ENUM_OBJET.AUCUN:
            pX = int(VAR.offSetX + (self.animation.x * VAR.pas))
            pY = int(VAR.offSetY + (self.animation.y * VAR.pas))
            
            VAR.fenetre.blit(VAR.IMG[self.animation.sprite()], (pX, pY))
            
    def ramasser(self, perso):
        categorie = VAR.terrain[self.animation.x][self.animation.y].categorie
        if categorie != ENUM_OBJET.AUCUN:
            if categorie == ENUM_OBJET.FLAMME:
                perso.puissanceBombe +=1
            elif categorie == ENUM_OBJET.ROLLER:
                perso.vitesse += 5
            elif categorie == ENUM_OBJET.BOMBE:
                perso.nbBombes +=1
            elif categorie == ENUM_OBJET.COUP_PIED:
                perso.coupPied = True
            elif categorie == ENUM_OBJET.COUP_POING:
                perso.coupPoint = True

            perso.listeObjets.append(categorie)
            VAR.terrain[self.animation.x][self.animation.y].categorie = ENUM_OBJET.AUCUN
