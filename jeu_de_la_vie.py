"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    LE JEU DE LA VIE
    coded by Saihttamu
    
    principe (de ce dont je me souviens): un ensemble de cellules va 'prendre
    vie', à chaque nouvelle etape (après une seconde par exemple) les cellules
    vont devenir soit mortes soit vivantes.
    
    On commence avec un nombre défini de cellules qu'il faut fixer à 
        
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import random, pygame, math, time, sys
from pygame.locals import *




# Variables principales

#COULEURS
#         R    G    B
BLANC  = (255, 255, 255)
NOIR   = (  0,   0,   0)
GRIS   = (160, 160, 160)
ROUGE  = (255,   0,   0)
VERT   = (  0, 255,   0)
BLEU   = (  0,   0, 255)
JAUNE  = (255, 255,   0)
VIOLET = (255,   0, 255)
CYAN   = (  0, 255, 255)

ALLCOLORS = (BLANC,NOIR,ROUGE,VERT,BLEU,JAUNE,VIOLET,CYAN)
COULEUR_fond = BLANC
COULEUR_tableau = (BLANC,NOIR)


#TEMPS
FPS = 5


#DIMENSIONS

LARG = 1500 # en pixels (fenêtre)
HAUT = 800 # en pixels (fenêtre)

bordure = 75

SURFutile = (LARG-2*bordure,HAUT-2*bordure) # dimensions du rectangle de la surface utile
BOARDSIZE = (30,50) # en elements par ligne et colonne
totalcells = BOARDSIZE[0]*BOARDSIZE[1]
CELLGAP = 4 # en pixels
CELLSIZE = 0 # on calculera sa valeur plus tard

gapFromBoard = 50

#JEU

started = False
stoped = False
cleared = False
nexted = False

#SURFACES

iterations = 0
popu = 0


#SOURIS

mousex = 0
mousey = 0
cellnumber = 0

#FONCTIONS

def get_cellsize(): # définit la taille d'une cellule en fonction du nombre de cellules
    return (int((SURFutile[1]-(min(BOARDSIZE)+1)*CELLGAP)/min(BOARDSIZE)))


def drawBoard(BOARDSIZE): # dessine le tableau de cellules
    DISPSURF.fill(BLANC)
    for lin in range(min(BOARDSIZE)+1):
        pygame.draw.line(DISPSURF, GRIS, (bordure,bordure+(CELLSIZE+CELLGAP)*lin), (bordure+max(BOARDSIZE)*(CELLGAP+CELLSIZE), bordure+(CELLSIZE+CELLGAP)*lin),CELLGAP) # horizontal
        pygame.draw.line(DISPSURF, GRIS, (bordure+(CELLSIZE+CELLGAP)*lin,bordure), (bordure+(CELLSIZE+CELLGAP)*lin,bordure+min(BOARDSIZE)*(CELLGAP+CELLSIZE)), CELLGAP) # vertical
        # arguments du draw : (Surface de travail, couleur du trait, point de départ, point d'arrivée, épaisseur)
        
    if BOARDSIZE[0] == BOARDSIZE[1]:
        return
    else:
        for col in range(max(BOARDSIZE)-min(BOARDSIZE)):
            pygame.draw.line(DISPSURF, GRIS, (bordure+(min(BOARDSIZE)+col+1)*(CELLSIZE+CELLGAP),bordure), (bordure+(min(BOARDSIZE)+col+1)*(CELLSIZE+CELLGAP),bordure+min(BOARDSIZE)*(CELLGAP+CELLSIZE)), CELLGAP)
        return

def getcells(): #renvoie une liste de toutes les cellules
    allcells = [] # cellule = ((numéro), alive, (pos))
    num = (0,0) # coordonnées de la cellule dans le tableau
    alive = False
    pos = (0,0) # en pixels, coordonées absolues du coin supérieur gauche de la cellule
    
    for y in range(min(BOARDSIZE)):
        for x in range(max(BOARDSIZE)):
            num = (x,y)
            pos = ((bordure+CELLGAP) + x*(CELLSIZE+CELLGAP), (bordure+CELLGAP) + y*(CELLSIZE+CELLGAP))
            allcells.append((num, alive, pos))
    
    return allcells
            

def startClicked():
    return (startbuttonRectObj.left <= mousex <=startbuttonRectObj.right) and (startbuttonRectObj.top <= mousey <= startbuttonRectObj.bottom)

def stopClicked():
    return (stopbuttonRectObj.left <= mousex <= stopbuttonRectObj.right) and (stopbuttonRectObj.top <= mousey <= stopbuttonRectObj.bottom)

def clearClicked():
    return (clearbuttonRectObj.left <= mousex <= clearbuttonRectObj.right) and (clearbuttonRectObj.top <= mousey <= clearbuttonRectObj.bottom)

def nextClicked():
    return (nextbuttonRectObj.left <= mousex <= nextbuttonRectObj.right) and (nextbuttonRectObj.top <= mousey <= nextbuttonRectObj.bottom)



def cellClicked(allcells):
    i = 0
    for y in range(min(BOARDSIZE)):
        for x in range(max(BOARDSIZE)):
            cellx = allcells[i][2][0]
            celly = allcells[i][2][1]
            if (cellx <= mousex <= cellx + CELLSIZE) and (celly <= mousey <= celly + CELLSIZE):
                allcells[i] = (allcells[i][0],not allcells[i][1],allcells[i][2])
                return allcells
            i += 1
    return allcells


def voisins(i,allcells): # i = indice de la cellule de allcells
    X = max(BOARDSIZE)
    Y = min(BOARDSIZE)
    voiz = 0
    
    if allcells[i][0][1] == 0: #cas particulier: bord supérieur
        if i == 0: # cas particulier: coin supérieur gauche
            for j in (1, X, X+1):
                if allcells[i+j][1] == True:
                   voiz += 1
        elif i == X-1: # cas particulier: coin supérieur droit
            for j in (-1, X-1, X):
                if allcells[i+j][1] == True:
                    voiz += 1
        else: # reste du bord supérieur
            for j in (X-1, X, X+1):
                if allcells[i+j][1] == True:
                    voiz += 1
    
    elif allcells[i][0][1] == Y-1: # cas particulier: bord inférieur
        if allcells[i][0] == (0, Y-1): # coin inférieur gauche
            for j in (-X, -X+1, +1):
                if allcells[i][1] == True:
                    voiz += 1
        elif allcells[i][0] == (X-1, Y-1): # coin inférieur droit
            for j in (-X-1, -X, -1):
                if allcells[i][1] == True:
                    voiz += 1
        else: # reste du bord inférieur
            for j in (-X-1, -X, -X+1):
                if allcells[i][1] == True:
                    voiz += 1
        
    elif allcells[i][0][0] == 0 and allcells[i][0] != (0,0) and allcells[i][0] != (0,Y-1): # cas particulier: bord gauche
        for j in (-X+1, 1, X+1):
            if allcells[i+j][1] == True:
                voiz += 1
    
    elif allcells[i][0][0] == X-1 and allcells[i][0] != (X-1,0) and allcells[i][0] != (X-1,Y-1): # cas particulier: bord droit
        for j in (-X-1, -1, X-1):
            if allcells[i+j][1] == True:
                voiz += 1
    
    else: # reste du tableau
        for j in (-X-1,-X,-X+1,-1,+1,X-1,X,X+1):
            if allcells[i+j][1] == True:
                voiz += 1
    
    return voiz
        
    

def nextstep(allcells):
    if (started == False and nexted == False) or stoped == True:
        return allcells
    else:
        nextallcells = []
        i = 0
        for y in range(min(BOARDSIZE)):
            for x in range(max(BOARDSIZE)):
                
                if allcells[i][1] == False: # si la cellule est morte elle devient vivante si elle a trois voisines vivantes
                    if voisins(i,allcells) == 3:
                        nextallcells.append((allcells[i][0],True,allcells[i][2]))
                    else:
                        nextallcells.append(allcells[i])
                        
                else:
                    if voisins(i,allcells) <= 1 or voisins(i,allcells) >= 4:
                        nextallcells.append((allcells[i][0],False,allcells[i][2]))
                    else:
                        nextallcells.append(allcells[i])
                i += 1
        return nextallcells
                    
                
            
def drawCells(allcells):
    
    for i in range(totalcells):
        if allcells[i][1] == True:
            pygame.draw.rect(DISPSURF, NOIR, (allcells[i][2][0], allcells[i][2][1], CELLSIZE, CELLSIZE))
        else:
            pygame.draw.rect(DISPSURF, BLANC, (allcells[i][2][0], allcells[i][2][1], CELLSIZE, CELLSIZE))
                
    


# MAIN GAME LOOP

#def main():

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPSURF = pygame.display.set_mode((LARG, HAUT), 0, 32)
pygame.display.set_caption('JEU DE LA VIE')

CELLSIZE = get_cellsize()
BOARDSURF = (max(BOARDSIZE)*CELLSIZE+(max(BOARDSIZE)+1)*CELLGAP,SURFutile[1])


allcells2 = getcells()


assert len(allcells2) == min(BOARDSIZE)*max(BOARDSIZE), "Les cellulles n'ont pas été initialisées correctement"


startbuttonObj = pygame.font.Font('freesansbold.ttf', 40) # fixe (boutton)
startbuttonSurfObj = startbuttonObj.render('START', False, NOIR, BLANC)
startbuttonRectObj = startbuttonSurfObj.get_rect()
startbuttonRectObj.topleft = (bordure+BOARDSURF[0]+gapFromBoard, 2*bordure)

stopbuttonObj = pygame.font.Font('freesansbold.ttf', 40)
stopbuttonSurfObj = stopbuttonObj.render('STOP', False, NOIR, BLANC)
stopbuttonRectObj = stopbuttonSurfObj.get_rect()
stopbuttonRectObj.topleft = (bordure+BOARDSURF[0]+gapFromBoard, startbuttonRectObj.bottom + int(bordure/2))

clearbuttonObj = pygame.font.Font('freesansbold.ttf', 40)
clearbuttonSurfObj = clearbuttonObj.render('CLEAR', False, NOIR, BLANC)
clearbuttonRectObj = clearbuttonSurfObj.get_rect()
clearbuttonRectObj.topleft = (stopbuttonRectObj.right + bordure, startbuttonRectObj.bottom + int(bordure/2))

nextbuttonObj = pygame.font.Font('freesansbold.ttf', 40)
nextbuttonSurfObj = nextbuttonObj.render('NEXT', False, NOIR, BLANC)
nextbuttonRectObj = nextbuttonSurfObj.get_rect()
nextbuttonRectObj.topleft = (startbuttonRectObj.right + bordure, startbuttonRectObj.top)


iteObj = pygame.font.Font('freesansbold.ttf', 40)



while True:
        
    iteSurfObj = iteObj.render('Iterations : '+str(iterations), False, NOIR, BLANC)
    iteRectObj = iteSurfObj.get_rect()
    iteRectObj.topleft = (bordure+BOARDSURF[0]+gapFromBoard, stopbuttonRectObj.bottom + int(bordure/2))  
    
    
    drawBoard(BOARDSIZE)
    DISPSURF.blit(startbuttonSurfObj, startbuttonRectObj)
    DISPSURF.blit(stopbuttonSurfObj,  stopbuttonRectObj)
    DISPSURF.blit(clearbuttonSurfObj, clearbuttonRectObj)
    DISPSURF.blit(nextbuttonSurfObj,  nextbuttonRectObj)
    DISPSURF.blit(iteSurfObj, iteRectObj)
    
    cleared = False
    nexted = False
    
    allcells1 = allcells2
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            allcells = cellClicked(allcells1)

        
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            
            if startClicked():
                started = True
                stopped = False
                
            
            elif stopClicked():
                started = False
                stopped = True
            
            elif clearClicked():
                cleared = True
            
            elif nextClicked() and not started:
                nexted = True
                
        
        #elif event.type == MOUSEBUTTONUP
    
    if started:
        iterations += 1
        allcells2 = nextstep(allcells1)
    elif cleared:
        allcells2 = getcells()
        iterations = 0
    elif nexted:
        iterations += 1
        allcells2 = nextstep(allcells1)
    
    drawCells(allcells2)
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    