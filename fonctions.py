import pygame
from pygame.locals import *

def iif(condition, vrai, faux):
    if condition == True:
        return vrai
    else:
        return faux
    
def image_vide(dimx, dimy):
    return pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)

def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
    tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
    tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                        
    # --- Colle le decors 
    if dimxZ != -1 and dimyZ != -1:   
        tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
    return tmp

def GenereMat2D(xDim, yDim, valeurDefaut):
    return [[valeurDefaut for x in range(yDim)] for i in range(xDim)]

def Generer_SpritesTexte_A_Partir_Image(fichier, id, dimX, dimY):
    imageTmp = pygame.image.load(fichier).convert_alpha() 
    listeTmp = {}

    for y in range(0, int(imageTmp.get_height() / dimY)):
        for x in range(0, int(imageTmp.get_width() / dimX)):
            tmp = pygame.Surface((dimX, dimY),pygame.SRCALPHA,32)
            tmp.blit(imageTmp, (0,0), (int(x) * dimX, int(y) * dimY, dimX, dimY))   
            listeTmp[id] = imageTmp
            id+=1

    return listeTmp

def image_vide(dimX, dimY):
    return pygame.Surface((dimX, dimY),pygame.SRCALPHA,32)

def Collision(x1, y1, dX1, dY1, x2, y2, dX2, dY2):
        return not ((x2 >= x1 + dX1) or (x2 + dX2 <= x1) or (y2 >= y1 + dY1) or (y2 + dY2 <= y1))
        
