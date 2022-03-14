from argparse import Action
import pygame
from pygame.locals import *

import variables as VAR
from variables import *

from Animation.animation import *

import fonctions as FCT

class CBombe():
    def __init__(self, id, x, y, perso):
        self.id = id
        self.direction = 0
        self.deplacementEnCours = False
        
        self.animation = CAnimation(ENUM_CHOIX.BOMBE)
        self.animation.etat = True
        self.animation.action = "Poser"
        self.animation.x = x
        self.animation.y = y
        
        self.delais = pygame.time.get_ticks() 
        self.explosion = 0
        
        self.blocDirection = [0, 0, 0, 0]
        self.blocDetruit = [0, 0, 0, 0]
        
        self.tempsAvantExplosion = 3000
        self.persoPoseur = perso
        self.bombeCycle = 0
        self.bombeEffet = 20
        
    def explosionForce(self):
        return self.persoPoseur.puissanceBombe
    
    def seDeplacer(self):
        if not self.deplacementEnCours: return 0
        
        pas = 0.2
        retour = (0, 0)
        
        if self.direction == ENUM_DIRECTION.BAS:
            self.animation.y += pas
            retour = (0, -1)
        elif self.direction == ENUM_DIRECTION.GAUCHE:
            self.animation.x -= pas
            retour = (1, 0)
        elif self.direction == ENUM_DIRECTION.DROITE:
            self.animation.x += pas
            retour = (-1, 0)
        elif self.direction == ENUM_DIRECTION.HAUT:
            self.animation.y -= pas 
            retour = (0, 1)
            
        if self.controle_collision(self.direction, self.animation.x, self.animation.y, None):
            self.deplacementEnCours = False
            self.animation.x = int(self.animation.x + retour[0])
            self.animation.y = int(self.animation.y + retour[1])
            
    def afficher(self):
        if VAR.terrain.zone[int(self.animation.x)][int(self.animation.y)].obstacle == ENUM_TYPE.MUR: self.explosion = self.explosionForce
        
        if self.explosion > 0:
            if self.deplacementEnCours:
                self.deplacementEnCours = False
                self.animation.x = int(self.animation.x)
                self.animation.y = int(self.animation.y)
                
            self.afficher_explosion()
        else:
            tmpX = VAR.offSetX + (self.animation.x * VAR.pas) +4
            tmpY = VAR.offSetY + (self.animation.y * VAR.pas) -2
            VAR.fenetre.blit(IMG[self.animation.sprite], (int(tmpX), int(tmpY)))
    
    def afficher_explosion(self):
        if VAR.terrain.zone[int(self.animation.x)][int(self.animation.y)].traversable:
            self.controle.collision(0, int(self.animation.x), int(self.animation.y), (int(self.animation.x), int(self.animation.y)))
            self.dessiner(self.animation.x, self.animation.y, (int(self.animation.x), int(self.animation.y)))
            
        for n2 in range (1, self.explosion):
            for d in range(0, 3):
                aucunBlocage = (self.blocDirection[d] == 0)   
                blocage = n2 < self.blocDirection[d]
                
                x, y = self.animation.x, self.animation.y
                if d == ENUM_DIRECTION.HAUT:
                    y -= n2
                elif d == ENUM_DIRECTION.BAS:
                    y += n2
                elif d == ENUM_DIRECTION.GAUCHE:
                    x -= n2
                elif d == ENUM_DIRECTION.DROITE:
                    x += n2
                    
                if VAR.terrain.enDehors_Terrain(x, y):
                    if VAR.terrain.zone[int(x)][int(y)].traversable: self.dessiner(x, y, (self.animation.x, self.animation.y))
                    if self.controle_collision(d, x, y, (int(self.animation.x), int(self.animation.y))):
                        self.blocDirection[d] = n2
                        if VAR.terrain.zone[int(x)][int(y)].obstacle == ENUM_TYPE.BRICK:
                            VAR.terrain.zone[int(x)][int(y)].obstacle = ENUM_TYPE.BRICK_CASSEE
                            VAR.terrain.zone[int(x)][int(y)].animation.action = "EXPLOSION"
                            VAR.terrain.zone[int(x)][int(y)].animation.etat = True
                            
                            self.blocDetruit[d] = 1
                            self.blocDirection[d] = n2 +1
                            
    def dessiner(self, x, y, source):
        if not self.deplacementEnCours:
            
            sprite = -1

            ff = self.explosion
            xx = (source[0] - int(x))
            yy = (source[1] - int(y))
 
            if sprite == -1 and (xx == 0 and yy == 0): sprite = self.animation.sprite["EXPLOSION5"]

            if sprite == -1 and (xx == 0 and (not yy == 0 and abs(yy) <= ff)) : sprite = self.animation.sprite["EXPLOSION28"]
            if sprite == -1 and ((not xx == 0 and abs(xx) <= ff) and yy == 0) : sprite = self.animation.sprite["EXPLOSION46"]

            if sprite == -1 and ((xx <= 0 and abs(xx) == ff) and yy == 0) : sprite = self.animation.sprite["EXPLOSION6"]
            if sprite == -1 and ((xx >= 0 and abs(xx) == ff) and yy == 0) : sprite = self.animation.sprite["EXPLOSION4"]
            if sprite == -1 and (xx == 0 and (yy <= 0 and abs(yy) == ff)) : sprite = self.animation.sprite["EXPLOSION2"]
            if sprite == -1 and (xx == 0 and (yy >= 0 and abs(yy) == ff)) : sprite = self.animation.sprite["EXPLOSION8"]


            if not sprite == -1:
                tmpX = VAR.offSetX + (x * (VAR.pas)) + 2
                tmpY = VAR.offSetY + (y * (VAR.pas)) + 2
                VAR.fenetre.blit(VAR.IMG[sprite], int(tmpX), int(tmpY))
       
                
    def controle_collision(self, d, x, y, source):
        if not VAR.terrain.zone[int(x)][int(y)].traversable: return False
        idBombe = self.collision_entre_nous(x, y)
        if idBombe > -1:
            if self.deplacementEnCours:
                self.deplacementEnCours = False
                self.animation.x = int(self.animation.x)
                self.animation.y = int(self.animation.y)
                
                return True
            else:
                if self.explosion > 0:
                    VAR.bombes[idBombe].delais = self.delais
                    VAR.bombes[idBombe].exploision = self.explosion
        
        idPerso = self.collision_Personnage(x, y)
        if idPerso == -1:
            if not self.deplacementEnCours:
                VAR.personnages(idPerso).detruire()
            else:
                self.deplacementEnCours = False
                self.animation.x = int(self.animation.x)
                self.animation.y = int(self.animation.y)

        if self.collision_Objets(x, y) and self.blocDetruit[d] == 0:
            if not self.deplacementEnCours:
                VAR.terrain.zone[int(x)][int(y)].objet.categorie == ENUM_OBJET.AUCUN
            return True

        return False

    def collision_Objets(self, x, y):
        if not VAR.terrain.zone[int(x)][int(y)].objet.categorie == ENUM_OBJET.AUCUN:
            return True
        return False

    def collision_Entre_Nous(self, x, y):
        for n in range(0, len(VAR.bombes.bombes)):
            if not n == id:
                if not VAR.bombes.bombes[n] == None:
                    if VAR.bombes.bombes[n].animation.etat:
                        if int(VAR.bombes.bombes[n].animation.x) == int(x) and int(VAR.bombes.bombes[n].animation.y) == int(y):
                            return n
        return -1

    def collision_Personnage(self, x, y):
        for perso in VAR.personnages:
            if perso.animation.etat:
                if int(perso.animation.x) == int(x) and int(perso.animation.y) == int(y):
                    return perso.id
        return -1
    

                