 
import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from Terrain.terrain import *
from Bombe.bombes import *
from Perso.perso import *


class CMoteur():
    def __init__(self):
        pygame.init()
        
        VAR.fenetre = pygame.display.set_mode((VAR.ecranX, VAR.ecranY), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBomb v0.01")
        
    def demarrer(self, dimX, dimY):
        print("    + demarrer")
        VAR.terrain = CTerrain()
        VAR.bombes = CBombes(30)
        VAR.personnages = [CPerso(0, ENUM_CONTROLEPAR.JOUEUR), CPerso(1, ENUM_CONTROLEPAR.ORDINATEUR), CPerso(2, ENUM_CONTROLEPAR.ORDINATEUR), CPerso(3, ENUM_CONTROLEPAR.ORDINATEUR)]

        self.chargement_decors()
        self.nouvelle_partie(dimX, dimY, 70, 70, 1, 1)
        
        self.boucle_principale()

    def nouvelle_partie(self, dimX, dimY, brick, objet, nbJ, nbO):
        print("    + nouvelle_partie")
        VAR.terrain = CTerrain(dimX, dimY, brick, objet, False)
        VAR.bombes = CBombes(30)
 
    def chargement_decors(self):
        print("    + chargement_decors")

        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\explosion.png", 500, 32, 32).items():
            IMG[id] = image
            
        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\decors2.png", 600, 40, 40).items():
            IMG[id] = image
        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\objets3.png", 700, 30, 36).items():
            IMG[id] = image
        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\sprites.png", 800, 21, 32).items():
            IMG[id] = image
        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\sprite0.png", 1000, 32, 40).items():
            IMG[id] = image
        for id, image in FCT.Generer_SpritesTexte_A_Partir_Image("Ressources\\sprite2.png", 1100, 32, 40).items():
            IMG[id] = image
        
        
    def boucle_principale(self):
        print("    + boucle_principale")
        VAR.clock = pygame.time.Clock()
        while VAR.boucle_jeu:
            
            for event in pygame.event.get():        
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    VAR.boucle_jeu = False
            
            self.afficher()
            pygame.display.update()
            
            VAR.clock.tick(VAR.nombreImageSeconde)
            animation+=1
            
        pygame.quit()   
        
        
    def afficher(self):
        VAR.fenetre.fill ((0,0,0))
        self.afficher_barre_scores()
        VAR.terrain.afficher_couche_basse()
        VAR.terrain.destruction_timing()
        VAR.terrain.afficher_couche_haute()
        VAR.bombes.afficher()
        self.afficher_persos()

    def afficher_barre_scores(self):
        pass

    def afficher_persos(self):
        for perso in VAR.Persos:
            if perso.animation.etat:
                perso.afficher()