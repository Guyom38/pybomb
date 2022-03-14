from argparse import Action
import pygame
from pygame.locals import *

import variables as VAR
from variables import *

from Animation.animation import *
from Bombe.bombe import *


import fonctions as FCT

class CBombes():
    def __init__(self):
        print("CBombes")         
        self.bombes = []
        self.cycle = 0
        self.delais = 50

    def nombreBombes(self):
        return len(self.bombes)

    def Gestion_Explosion(self, n):
        
        if pygame.time.get_ticks() - VAR.bombes.bombes[n].delais > VAR.bombes.bombes[n].TempsAvantExplosion:
                if pygame.time.get_ticks() - self.cycle > self.delais:
                    if VAR.bombes.bombes[n].Explosion == VAR.bombes.bombes[n].Explosion_Force:
                        if VAR.bombes.bombes[n].delaisBombe_Effet_Timer == 0:
                             VAR.bombes.bombes[n].delaisBombe_Effet_Timer = pygame.time.get_ticks()

                        if pygame.time.get_ticks() - VAR.bombes.bombes[n].delaisBombe_Effet_Timer > VAR.bombes.bombes[n].delaisBombe_Effet:
                            VAR.bombes.bombes[n].animation.etat.Etat = False
                            VAR.bombes.bombes[n].persoPoseur.nbBombesPosees -= 1

                    else:
                        VAR.bombes.bombes[n].Explosion += 1

                    self.cycle = pygame.time.get_ticks()


    def poser(self, perso, x, y):
        if not perso.peutPoserBombe(): return 0

        
        trouverLibre = 0
        notStop = True
        while notStop:
            trouver = False
            if VAR.bombes.bombes[trouverLibre] == None:
                trouver = True
            else:
                if not VAR.bombes._bombes[trouverLibre].animation.etat:
                    trouver = True

            if trouver:
            #' //
            #' // ---> A-t-il déjà une bombe ?
                for n in range(0, len(VAR.bombes.bombes)):
                    if not VAR.bombes.bombes[n] == None:
                        if VAR.bombes.bombes[n].animation.etat:
                            if VAR.bombes.bombes[n].animation.x == int(x) and VAR.bombes.bombes[n].animation.y == int(y):
                                notStop = False
                    VAR.bombes.bombes[trouverLibre] = CBombe(trouverLibre, int(x), int(y), perso)
                    perso.nbBombesPosees += 1
                    notStop = False

                if trouverLibre < len(VAR.bombes.bombes):
                    trouverLibre += 1 
                else:
                    notStop = False




    def il_Y_a_Til_Collision(self, x, y):
        for n in range(0, self.nombreBombes):
            if not self.bombes[n] == None:
                    if self.bombes[n].animation.etat:
                        if int(x) == int(self.bombes[n].animation.x) and int(y) == int(self.bombes[n].animation.y):
                            return n
            return -1

    def afficher(self):
        for n in range(0, self.nombreBombes):
            if not self.bombes[n] == None:
                if self.bombes[n].animation.etat:
                    self.gestion_Explosion(n)
                    self.bombes[n].afficher()


