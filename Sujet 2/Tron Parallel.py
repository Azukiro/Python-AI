import tkinter as tk
import random
import time
import numpy as np


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

#############################################################
#
#  affichage en mode texte


def AffGrilles(G,X,Y):
    nbG, larg , haut = G.shape
    for y in range(haut-1,-1,-1) :
        for i in range(nbG) :
            for x in range(larg) :
               g = G[i]
               c = ' '
               if G[i,x,y] == 1 : c = 'M'  # mur
               if G[i,x,y] == 2 : c = 'O'  # trace
               if (X[i],Y[i]) == (x,y) : c ='X'  # joueur
               print(c,sep='', end = '')
            print(" ",sep='', end = '') # espace entre les grilles
        print("") # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

# nb de parties
nb = 5 

# mode débug
Debug = False


def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties
    G      = np.tile(Game.Grille,(nb,1,1))      # grille  (x,y) pour chaque partie
    X      = np.tile(Game.PlayerX,nb)           # playerX (x)   pour chaque partie
    Y      = np.tile(Game.PlayerY,nb)           # playerY (y)   pour chaque partie
    S      = np.tile(Game.Score,nb)             # score   (s)   pour chaque partie
    I      = np.arange(nb)                      # 0,1,2,3,...,nb-1

    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI

    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2

        # direction aléatoire
        R = np.random.randint(4,size=nb)

        # tous les déplacements possibles
        LPossibles = np.zeros((nb, 4),dtype=np.int32)
        for i in range(4):
            LPossibles[I,i] = np.where(G[I, X+dx[i+1], Y+dy[i+1]] == 0,i+1,0)

        Indices = np.zeros(nb,dtype=np.int32)
        Indices = np.count_nonzero(LPossibles != 0, axis=1)
      
        Indices[Indices == 0] = 1
        Position = LPossibles[I,R%Indices[I]]
        S[I] += Position[I]!=0
        nb0 =  np.count_nonzero(Position == 0 )
        print(nb0)
        if(nb0==nb):
            boucle = False
        DX = dx[Position]
        DY = dy[Position]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY


        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)
    print(S)
    print("Scores : ",np.mean(S))



Simulate(GameInit)

