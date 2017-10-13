import pygame
from pygame.locals import *
import os
import sys

class ImagenDinamica(pygame.sprite.Sprite): 
 # clase que hereda de la clase Sprite en donde "pygame.sprite" especifica 
 # la biblioteca y el paquete
    """Clase para los jugadores"""

    def __init__(self, ruta, ventana, velocidad):  # constructor
        pygame.sprite.Sprite.__init__(self)
        self.ruta = ruta  # ruta de la img a abrir
        self.ventana = ventana  # objeto tipo ventana
        self.img = pygame.image.load(ruta)   # contiene la imagen cargada ya en la ventana
        self.posX = 0  
        self.posY = 0  
        self.topeSuperior = -5000  # tope superior en pixeles hasta donde se podra mover la imagen 
        self.topeInferior =  5000  # tope inferior en pixeles hasta donde se podra mover la imagen 
        self.topeIzquierdo =  -5000  # tope izquierdo en pixeles hasta donde se podra mover la imagen 
        self.topeDerecho = 5000  # tope derecho en pixeles hasta donde se podra mover la imagen 
        self.Pixels = ()
        self.velocidad = velocidad
        self.rectangulo = self.img.get_rect()  # me sirve para detectar colisiones


    #dibujo la imagen
    def dibujarImg(self, posX, posY):
        self.ventana.blit(self.img, (posX, posY))  # dibujo la imagen en la ventana

    def cambiarTamañoImg(self, pixelsX, pixelsY):
        self.img = pygame.transform.scale(self.img, (pixelsX, pixelsY))
        self.pixels = (pixelsX, pixelsY)
        self.rectangulo = self.img.get_rect()
        
    def moverIzq(self):
        if (self.posX - self.velocidad) >= self.topeIzquierdo:
            self.posX -= self.velocidad

    def moverDer(self):
        if (self.posX + self.velocidad) <= self.topeDerecho:
            self.posX += self.velocidad

    def moverAbajo(self):
        if (self.posY + self.velocidad) <= (self.topeInferior):
            self.posY += self.velocidad
    
    def moverArriba(self): 
        if (self.posY - self.velocidad) >= self.topeSuperior:

            self.posY -= self.velocidad
    
    def moverSupDerecho(self):
        if (self.posY - self.velocidad) >= self.topeSuperior-self.velocidad:
            self.posY -= self.velocidad
        if (self.posX + self.velocidad) <= self.topeDerecho+self.velocidad:
            self.posX += self.velocidad

    def moverSupIzquierdo(self):
        if (self.posY - self.velocidad) >= self.topeSuperior-self.velocidad:
            self.posY -= self.velocidad
        if (self.posX - self.velocidad) >= self.topeIzquierdo-self.velocidad:
            self.posX -= self.velocidad

    def moverInfDerecho(self):
        if (self.posY + self.velocidad) <= self.topeInferior+self.velocidad:
            self.posY += self.velocidad
        if (self.posX + self.velocidad) <= self.topeDerecho+self.velocidad:
            self.posX += self.velocidad

    def moverInfIzquierdo(self):
        if (self.posX - self.velocidad) >= self.topeIzquierdo-self.velocidad:
            self.posX -= self.velocidad
        if (self.posY + self.velocidad) <= self.topeInferior+self.velocidad:
            self.posY += self.velocidad 
    
    def setPos(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def setPosX(self, posX):
        self.posX = posX
    
    def setPosY(self, posY):
        self.posY = posY

    def getPosX(self):
        return self.posX
    
    def getPos(self):
        return (self.posX, self.posY)

    def getPosY(self):
        return self.posY

    def getImg(self):
        return self.img

    def getRectangulo(self):
        return self.rectangulo

    def setPixels(self, alto, ancho):
        self.pixels = (ancho, alto)

    def getPixels(self):
        return self.pixels

    def setTopes(self, topeIzquierdo, topeDerecho, topeSuperior, topeInferior):
        self.topeSuperior = topeSuperior
        self.topeInferior =  topeInferior 
        self.topeIzquierdo =  topeIzquierdo 
        self.topeDerecho = topeDerecho  

    def setVelocidad(self, velocidad):
        self.velocidad = velocidad

    def getVelocidad(self):
        return self.velocidad

    def getTopeSuperior(self):
        return self.topeSuperior

    def getTopeInferior(self):
        return self.topeInferior
    
    def getTopeDerecho(self):
        return self.topeDerecho

    def getTopeIzquierdo(self):
        return self.topeIzquierdo