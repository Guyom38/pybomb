 
import pygame
from pygame.locals import *
from Animation.animation import *
from Objet.objet import *

import variables as VAR
from variables import *

import fonctions as FCT
import random

class CPerso():
    def __init__(self, id, controle):
        self.id = id
        self.id_serveur = -1
        self.controlePar = controle
        
        self.animation = None
        self.modele = 1000
        
        self.bombeCycle = 0
        self.bombeDelais = 500
        
        self.pressionCycle = 0
        
        self.puissanceBombe = 1
        self.nbBombes = 1
        self.nbBombesPosees = 0
        self.vitesse = 30
        self.coupDePied = False
        self.coupDePoing = False
        
        self.listeObjets = []
        self.listeActions = []
        
        self.distance = 0
        self.distancePas = 0
        
        self.nouveau()
        
    def peutPoserBombe(self):
        if pygame.time.get_ticks() - self.bombeCycle < self.bombeDelais: return False
        if self.nbBombesPosees >= self.nbBombes: return False
        
        self.bombeCycle = pygame.time.get_ticks()
        return True
    
    def nouveau(self):
        VAR.nbPersonnages += 1
        self.animation = CAnimation(ENUM_CHOIX.PERSO)
        self.animation.etat = True
        self.listeObjets = []
        self.listeActions = []
        
        if self.controlePar == ENUM_CONTROLEPAR.JOUEUR_INTERNET:
            self.modele = 1000
            self.positionne_joueur()
            
        elif self.controlePar == ENUM_CONTROLEPAR.JOUEUR:
            self.modele = 1000
            self.positionne_joueur()
            #JOYSTICK
            
        elif self.controlePar == ENUM_CONTROLEPAR.ORDINATEUR:
            self.modele = 1100
            self.changer_direction()
            
            notStop = True
            while notStop:
                self.animation.x = random.randint(0, VAR.dimensionX)
                self.animation.y = random.randint(0, VAR.dimensionY)
                
                colision = False
                if VAR.terrain.enDehors_Terrain(self.animation.x, self.animation.y): colision = True
                if VAR.terrain.colision_Decors(self.animation.x, self.animation.y): colision = True
                if VAR.terrain.zone[self.animation.x][self.animation.y].traversable: colision = True
                
                if not colision:
                    notStop = False
            
            self.creation_zone_libre()
            
    def position_joueur(self):
        if self.id == 0:
            self.animation.x, self.animation.y = 1, 1
        elif self.id == 1:
            self.animation.x, self.animation.y = VAR.dimensionX -1, VAR.dimensionY-1
        elif self.id == 2:
            self.animation.x, self.animation.y = int(VAR.dimensionX / 2), int(VAR.dimensionY / 2)
        elif self.id == 3:
            self.animation.x, self.animation.y = 1, VAR.dimensionY -1
        elif self.id == 4:
            self.animation.x, self.animation.y = VAR.dimensionX -1, 1
            
    def creation_zone_libre(self):
        for x in range (-2, 2):
            for y in range (-2, 2):
                if VAR.terrain.enDehors_Terrain(self.animation.x, self.animation.y):
                    if VAR.terrain.zone[self.animation.x + x][self.animation.y + y].obstacle == ENUM_TYPE.BRICK:
                        VAR.terrain.zone[self.animation.x + x][self.animation.y + y].obstacle = ENUM_TYPE.AUCUN
                        VAR.terrain.zone[self.animation.x + x][self.animation.y + y].categorie = ENUM_OBJET.AUCUN 
                        
    def detruire(self):
        if self.animation.action == "MOURRIR": return 0
        self.animation.action = "MOURRIR"
        self.animation.etat = True
        
        for objet_ramasse in self.listeObjets:
            notStop = True
            while notStop:
                objX = random.randint(0, VAR.dimensionX)
                objY = random.randint(0, VAR.dimensionY)
                
                collision = False
                if VAR.terrain.collision_Decors(objX, objY): collision = True
                
                if not collision:
                    if VAR.terrain.zone[objX][objY].objet.categorie == ENUM_OBJET.AUCUN: notStop = False
        
        
            VAR.terrain.zone[objX][objY] = CObjet(-10, objX, objY, objet_ramasse)
        self.listeObjets = []
        
    def seDeplace(self):
        pas = 100
        bouge = False
        
        if self.gestion_mort(): return 0
        
        if pygame.time.get_ticks() - self.pressionCycle > self.vitesse:
            ancX = self.animation.x
            ancY = self.animation.y
            
            if self.controlePar == ENUM_CONTROLEPAR.JOUEUR_INTERNET:
                bouge = self.gestion_utilisateur(pas, False)
                
            elif self.controlePar == ENUM_CONTROLEPAR.JOUEUR:
                #Joystick
                bouge = self.gestion_utilisateur(pas, True)
                
            elif self.controlePar == ENUM_CONTROLEPAR.ORDINATEUR:
                if self.distancePas == self.distance:
                    if self.animation.x == int(self.animation.x) and self.animation.t == int(self.animation.y): 
                        self.changer_direction()
                    else:
                        self.distancePas += 1
                    
                    self.deplace(pas)
                    bouge = True
            
            if not bouge:
                self.animation.action = "ARRETER"
            else:
                self.aniamtion.action = "MARCHER"
                self.gestion_collision(ancX, ancY, pas)
                
                VAR.terrain.zone[int(self.animation.x)][int(self.animation.y)].objet.ramasser()
                
            self.ordinateur_pose_aleatoirement()
            self.pressionCycle = pygame.time.get_ticks() 
            
    def gestion_mort(self):
        if self.animation.action == "MOURRIR":
            if self.animation.estTerminee:
                self.animation.etat = False
                VAR.nbPersonnages -= 1
            
            return True
        return False
    
    def deplace(self, pas):
        if self.animation.direction == ENUM_DIRECTION.BAS:
            self.animation.y += pas
        elif self.animation.direction == ENUM_DIRECTION.GAUCHE:
            self.animation.x -= pas
        elif self.animation.direction == ENUM_DIRECTION.DROITE:
            self.animation.x += pas
        elif self.animation.direction == ENUM_DIRECTION.HAUT:
            self.animation.y -= pas
        
    def gestion_utilisateur(self, pas, joueurReel):
        bouge = False
        if len(self.listeActions) > 0:
            #{Joystick}
            sync = ""
            if not sync == "" and not sync == "T":
                self.deplace(pas)
                bouge = True
        return bouge
    
    def gestion_collision(self, ancX, ancY, pas):
        collision = False
        
        if VAR.terrain.collision_Decors(self.animation.x, self.animation.y, id = 0): collision = True
        
        self.ajsute_trajectoire(collision, ancX, ancY, 0.05)
        
        ifBombe = 
            
                
            