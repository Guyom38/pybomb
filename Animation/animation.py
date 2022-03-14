from argparse import Action
import pygame
from pygame.locals import *

import variables as VAR
from variables import *
from Animation.action import *

import fonctions as FCT

class CAnimation():
    def __init__(self, choix):
        self.etat = False
        self.x = 1
        self.y = 1
        self.frame = 0
        self.maxFrame = 4
        self.actions = {}
        
        self.cycle = 0
        self.frequence = 50
        
        self.action = "ARRETER"
        self.direction = ENUM_DIRECTION.BAS
        
        if choix == ENUM_CHOIX.PERSO:
            self.actions["MARCHER"] = CActions (0, 3, True, False, 0.1)
            self.actions["ARRETER"] = CActions ( 0, 1, False, False, 0.1)
            self.actions["MOURRIR"] = CActions ( 30, 4, False, True, 0.3)
        if choix == ENUM_CHOIX.BOMBE:
            self.actions["POSER"] = CActions ( 845, 3, False, False, 0.1)
            self.actions["EXPLOSION8"] = CActions ( 500, 4, False, True, 0.3)
            self.actions["EXPLOSION6"] = CActions ( 508, 4, False, True, 0.3)
            self.actions["EXPLOSION4"] = CActions ( 516, 4, False, True, 0.3)
            self.actions["EXPLOSION2"] = CActions ( 524, 4, False, True, 0.3)
            self.actions["EXPLOSION28"] = CActions ( 532, 4, False, True, 0.3)
            self.actions["EXPLOSION46"] = CActions ( 540, 4, False, True, 0.3)
            self.actions["EXPLOSION5"] = CActions ( 548, 4, False, True, 0.3)
        if choix == ENUM_CHOIX.OBJET:
            vitesseObjet = 0.1
            self.actions[ENUM_OBJET.COUP_PIED] = CActions ( 700, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.COUP_POING] = CActions ( 703, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.BOMBE] = CActions ( 706, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.COEUR] = CActions ( 709, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.FLAMME] = CActions ( 712, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.GANT] = CActions ( 715, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.TATANE] = CActions ( 718, 3,  True, False, vitesseObjet)
            self.actions[ENUM_OBJET.ROLLER] = CActions ( 721, 3,  True, False, vitesseObjet)
            
        if choix == ENUM_CHOIX.SURFACE:
            self.actions["SOL1"] = CActions ( 606, 1,  False, False, 50)
            self.actions["SOL2"] = CActions ( 607, 1,  False, False, 50)
            self.actions["SOLIDE"] = CActions ( 612, 1,  False, False, 50)
            self.actions["BRICK"] = CActions ( 600, 1,  False, False, 50)
            self.actions["EXPLOSION"] = CActions ( 601, 5,  False, True, 0.1) 
            
    def set_action(self, valeur):
        if self.action != valeur: self.frame = 0
        self.action = valeur
        if valeur in self.actions:
            self.maxFrame = self.actions[valeur].nbImages -1
            self.frequence = self.actions[valeur].vitesse
            
    def actualiser(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            if self.frame >= self.maxFrame:
                blocFrame = False
                if self.action in self.actions:
                    if self.actions(self.action).stopAnimation: 
                        blocFrame = True
                        self.etat = False
                if blocFrame == False: self.frame = 0
            else:
                self.frame += 1
                
            self.cycle = pygame.time.get_ticks()
            
    def sprite(self, act = "", actuel = True):
        if act != "": self.set_action(act)
        
        if self.action in self.actions:
            if actuel == True: self.actualiser()
            result = self.actions(self.action).premiereImage + self.frame + int(FCT.iif(self.actions(self.action).toutesDirection, self.retourne_direction_offset_image(self.direction), 0))
            return result

        return 0
    
    def retourne_direction_offset_image(self, direction):
        if direction == ENUM_DIRECTION.BAS: 
            return 0
        elif direction == ENUM_DIRECTION.GAUCHE:
            return 8
        elif direction == ENUM_DIRECTION.DROITE:
            return 24
        elif direction == ENUM_DIRECTION.HAUT:
            return 16
        
        return 0
        
                