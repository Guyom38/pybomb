 
import pygame
from pygame.locals import *
from Animation.animation import *
from Objet.objet import *

import variables as VAR
from variables import *

import fonctions as FCT
import random, math

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
        self.ancienAjustement = -1

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
                if VAR.terrain.collision_Decors(self.animation.x, self.animation.y): colision = True
                if VAR.terrain.zone[self.animation.x][self.animation.y].traversable: colision = True
                
                if not colision:
                    notStop = False
            
            self.creation_zone_libre()
            
    def positionne_joueur(self):
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
        
        idBombe = VAR.Bombes.il_Y_a_Til_Collision(self.animation.x, self.animation.y)
        if idBombe > -1 and not VAR.bombes.il_Y_a_Til_Collision(ancX, ancY) > -1:
            if self.coupDePied:
                VAR.bombes.bombes[idBombe].deplacementEnCours = True
                VAR.bombes.bombes[idBombe].direction = self.animation.direction
            collision = True

        persoConflit = self.collision_Autre_Personnage()
        if persoConflit > -1 and self.coupDePoing:
            if VAR.personnages[persoConflit].direction == ENUM_DIRECTION.BAS:
                VAR.personnages[persoConflit].animation.y += self.pas
            elif VAR.personnages[persoConflit].direction == ENUM_DIRECTION.GAUCHE:
                VAR.personnages[persoConflit].animation.x -= self.pas
            elif VAR.personnages[persoConflit].direction == ENUM_DIRECTION.DROITE:
                VAR.personnages[persoConflit].animation.x += self.pas
            elif VAR.personnages[persoConflit].direction == ENUM_DIRECTION.HAUT:
                VAR.personnages[persoConflit].animation.y -= self.pas
            collision = True

        if collision:
            if self.controlePar == ENUM_CONTROLEPAR.JOUEUR:
                self.animation.x = ancX
                self.animation.y = ancY
            elif self.controlePar == ENUM_CONTROLEPAR.ORDINATEUR:
                self.animation.x = int(ancX)
                self.animation.y = int(ancY)

                self.changer_Direction()

    def poser_bombe(self):
        VAR.bombes.poser(self, self.animation.x, self.animation.y)

    def ordinateur_pose_aleatoirement(self):
        if self.controlePar == ENUM_CONTROLEPAR.ORDINATEUR:
            if random.randint(0, 100) < 5:
                self.poser_Bombe()

    def changer_direction(self):
        notStop = True
        while notStop:
            
            newDirection = random.choice((ENUM_DIRECTION.BAS, ENUM_DIRECTION.GAUCHE, ENUM_DIRECTION.DROITE, ENUM_DIRECTION.HAUT))
            if newDirection == self.animation.direction:
                self.animation.direction = newDirection
                notStop = False
    
    def afficher(self):
        if not self.animation.etat: return 0
        self.seDeplace()

        posX = int(VAR.offSetX + (self.animation.x * VAR.pas) + 2)
        posY = int(VAR.offSetY + (self.animation.y * VAR.pas) - 16)
        VAR.fenetre.blit(VAR.IMG[self.modele + self.animation.sprite], (posX, posY))

    def ajuste_trajectoire(self, collision, ancX, ancY, pas):
        oldAjustement = self.ancienAjustement

        if collision:
            tX = int(self.animation.x)
            tY = int(self.animation.y)

            leQuel = []
            sens = 0
            calcul = 0
            base_ANIMATION = 0
            base_ANC = 0
            coeff = 0

            #' //
            #' // ---> Tester Direction
            if self.animation.direction == ENUM_DIRECTION.BAS:
                base_ANIMATION = self.animation.x 
                coeff = +1 
                base_ANC = ancX
            elif self.animation.direction == ENUM_DIRECTION.HAUT:    
                base_ANIMATION = self.animation.x 
                coeff = -1 
                base_ANC = _ancX
            elif self.animation.direction == ENUM_DIRECTION.DROITE:    
                base_ANIMATION = self.animation.y 
                coeff = +1 
                base_ANC = ancY
            elif self.animation.direction == ENUM_DIRECTION.GAUCHE:    
                base_ANIMATION = self.animation.y 
                coeff = -1 
                base_ANC = ancY

            calcul = math.round(base_ANIMATION - int(base_ANIMATION), 2)

            #' //
            #' // ---> Ou sont les passages ?
            for no in range(-1, 1):
                noX = tX
                noY = tY

                if base_ANIMATION == self.animation.x:
                     noX += no 
                     noY += coeff 
                else:
                    noX += coeff
                    noY += no

                if not VAR._terrain.enDehors_Terrain(noX, noY) :
                    if VAR.terrain.zone(noX, noY).traversable :
                        self.leQuel.append(no)

            

            if len(self.leQuel) == 0: return 0

            #' //
            #' // ---> Calcul la direction du mouvement
            if len(self.leQuel) == 1 :
                if self.leQuel[0] == -1:
                    if calcul >= 0.5 and calcul <= 0.8 and int(base_ANC) < int(base_ANC):
                        sens = -1 
                        ancienAjustement = 6
                elif self.leQuel[0] == 0:
                        if calcul >= 0.1 and calcul <= 1 and int(base_ANC) == int(base_ANC):
                            sens = -1 
                            ancienAjustement = 1
                        if calcul >= 0.5 and calcul <= 1 and int(base_ANC) < int(base_ANC):
                            sens = 1 
                            ancienAjustement = 2
                elif self.leQuel[0] == 1:
                        if calcul >= 0.1 and calcul <= 0.5 and int(base_ANC) == int(base_ANC):
                            sens = 1
                            ancienAjustement = 7

            elif len(self.leQuel) == 2 :
                if self.leQuel(0) == -1 and self.leQuel(1) == 1:
                    if calcul >= 0.1 and calcul <= 0.5 and int(base_ANC) == int(base_ANC):
                        sens = 1
                        ancienAjustement = 3
                    if calcul >= 0.4 and calcul <= 0.9 and int(base_ANC) < int(base_ANC):
                        sens = -1 
                        ancienAjustement = 4


            #' //
            #' // ---> Fait glisser le joueur
            if base_ANIMATION == self.animation.x:
                if sens == -1:
                    if not VAR.terrain.collision_Decors(self.animation.x - pas - pas, ancY, Id = 0):
                        ancX = self.animation.x - pas - pas
                elif sens == 1: 
                    if not VAR.terrain.collision_Decors(self.animation.x + pas + pas, ancY, Id = 0):
                        _ancX = self.animation.x + pas + pas
            else:
                if sens == -1: 
                    if not VAR.terrain.collision_Decors(_ancX, self.animation.y - pas - pas, Id = 0):
                        ancY = self.animation.y - pas - pas
                elif sens == 1:  
                    if not VAR.terrain.collision_Decors(_ancX, self.animation.y + pas + pas, Id = 0):
                        ancY = self.animation.Y + pas + pas

            liste = ""
            for el in self.leQuel:
                if not liste == "": liste += ","
                liste += el

            print("Xint:" + str(int(_ancX)) + "- XCint:" + str(int(_ancX)) + " - CALCUL: " & str(math.round(calcul, 2)) + " - BLOCS: " + liste + " - CAS: " + str(ancienAjustement) + " (av: " + str(oldAjustement) + ")")

    def collision_autre_personnage(self):
        pas = VAR.pas
        for perso in VAR.personnages:
            if not perso.id == self.id:

                if FCT.collision(int(self.animation.x * pas), int(self.animation.y * pas), pas, pas, int(perso.animation.x * pas), int(perso.animation.y * pas), pas, pas):
                    return perso.id
                #'      If CInt(_perso._ANIMATION.X) = CInt(_ANIMATION.X) And CInt(_perso._ANIMATION.Y) = CInt(_ANIMATION.Y) Then Return _perso.Id


        return -1

    
            
                
            