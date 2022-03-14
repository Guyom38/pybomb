from curses import KEY_DOWN
import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT


class CControle():
    class Touche:
        touche_Haut = 0
        touche_Bas = 0
        touche_Gauche = 0
        touche_Droite = 0
        touche_Action_1 = 0
        touche_Action_2 = 0

    def __init__(self, perso, idConfig):
        self.perso = perso
        self.id_config = idConfig
        if idConfig == 0:
            touche_Haut, touche_Bas, touche_Gauche, touche_Droite, touche_Action_1, touche_Action_2 = K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_SHIFT

    def pression_Clavier(_jol = ""):
        bouge = False
        sync = ""

        
