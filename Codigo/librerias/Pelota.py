import pygame
from pygame.locals import *
import os
import sys
import Jugador.py

RADIO_BALL = 20
ball_pos = [WIDTH // 2, HEIGHT // 2] #  uso una matriz ya que debo dar la posicion de x e y
ball_vel = [50, 40] #  Uso una matriz ya que tengo que dar la velocidad de x e y

class Pelota(pygame.sprite.Sprite): 
 	# clase que hereda de la clase Sprite en donde "pygame.sprite" especifica 
 	# la biblioteca y el paquete
 	"""Clase para los jugadores"""
 	def __init__(self):  # constructor
 		self.vertical = None  # puedo usarlo para la velocidad en Y y el lado (si es negativo para arriba y si es positivo para abajo)
 		self.horizontal = None

 		def inicializarPelota(lado):
		#True = derecha, False = Izquierda
		if lado:
		#  si el lado era derecho(true) lo paso a izquierdo
			lado = False
 
		#  si el lado era izquierdo(false) lo paso a derecho
		lado = True
	

def moverPelota():
return booleano

def dibujarPelota():
    return img

def chocarPelota():
    return booleano

def cambiarVelocidad():
    return booleano