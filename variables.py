import enum

class ENUM_CONTROLEPAR(enum):
    JOUEUR = 0
    JOUEUR_INTERNET = 1
    ORDINATEUR = 2
    
class ENUM_DIRECTION(enum):
    HAUT = 0
    BAS = 1
    GAUCHE = 2
    DROITE = 3

class ENUM_TYPE(enum):
    BRICK_CASSEE = -1
    AUCUN = 0
    MUR = 1
    BRICK = 2
    
class ENUM_CHOIX(enum):
    PERSO = 0
    BOMBE = 1
    OBJET = 2
    SURFACE = 3
    
class ENUM_OBJET(enum):
    AUCUN = 0
    FLAMME = 1
    ROLLER = 2
    BOMBE = 3
    COUP_PIED = 4
    COUP_POING = 5
    COEUR = 6
    GANT = 7
    TATANE = 8

    MALADIE_DIAHREE = 9
    MALADIE_INVERSEE = 10

terrain = None

fenetre = None
clock = None

ecranX, ecranY = 1024, 800
boucle_jeu = True
nombreImagesSeconde = 40

animation = 0

dimensionX, dimensionY = 10, 10
offSetX, offSetY = 0, 30
pas = 32

nbPersonnages = 0

IMG = {}