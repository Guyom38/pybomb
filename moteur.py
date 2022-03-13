 
import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from Terrain.terrain import *


class CMoteur():
    def __init__(self):
        pygame.init()
        
        VAR.fenetre = pygame.display.set_mode((VAR.EcranX, VAR.EcranY), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBomb v0.01")
        
    def demarrer(self):
        VAR.terrain = CTerrain()
    
    def chargement_decors(self):
        pass
        
        
    def boucle_principale(self):
        VAR.clock = pygame.time.Clock()
        while VAR.boucle_jeu:
            
            for event in VAR.evenements: #pygame.event.get():        
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    VAR.boucle_jeu = False
            
            self.afficher()
            pygame.display.update()
            
            VAR.clock.tick(VAR.nombreImageSeconde)
            animation+=1
            
        pygame.quit()   
        
        
    def afficher(self):
        pass