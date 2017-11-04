import pygame
from pygame.locals import *
import os
import sys
from librerias import ImagenDinamica


pygame.init()
#ventana
ANCHO = 1366
ALTO = 768
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Battle Front")
fondoMenu = pygame.image.load("Imagenes/fondoMenu.jpg")

#Musica
REBOTE_TRASERO = "Music/efectos/reboteTrasero.wav" 
REBOTE_DELANTERO = "Music/efectos/reboteDelantero.wav"
DRAW = "Music/efectos/draw.wav"
WIN = "Music/efectos/win.wav"
RIP_VIDA = "Music/efectos/ripVida.wav"
MUSIC_FONDO = (	"Music/fondos/fondo-ViolentPornography.wav",
				"Music/fondos/fondo-shots.wav",
				"Music/fondos/MusicGame.wav",
				"Music/fondos/fondo-africa.wav",
				"Music/fondos/fondo-the_fox.wav")

draw = pygame.mixer.Sound(DRAW)
win = pygame.mixer.Sound(WIN)
reboteDelantero = pygame.mixer.Sound(REBOTE_DELANTERO)
reboteTrasero = pygame.mixer.Sound(REBOTE_TRASERO)
ripVida = pygame.mixer.Sound(RIP_VIDA)

#colors:
WHITE = (255, 255, 255)
ORANGE = (200, 60, 8)
GREEN = (00, 255, 00)

#Fuentes y textos
pixelFuenteY = 56 
FuenteArial = pygame.font.SysFont("Arial", pixelFuenteY)
FuenteArial2 = pygame.font.SysFont("Arial", 40)

textStartOrange = FuenteArial.render('Start', 0, ORANGE)
textStartGreen = FuenteArial.render('Start', 0, GREEN)

textScoresOrange = FuenteArial.render('Scores', 0, ORANGE)
textScoresGreen = FuenteArial.render('Scores', 0, GREEN)

textExitOrange = FuenteArial.render('Exit', 0, ORANGE)
textExitGreen = FuenteArial.render('Exit', 0, GREEN)

#Archivo de texto
fileScores = 'Scores.txt' # nombre del archivo principal para guardar los scores
fileScores2 = 'Scores2.txt' # nombre del archivo auxiliar para hacer operaciones
#Zona de menu
#0-Start, 1-Scores, 2-Exit
textos = ((textStartOrange, textScoresOrange, textExitOrange),
	(textStartGreen, textScoresGreen, textExitGreen))
"""Matriz de Texto
[0,0][0,1][0,2]
[1,0][1,1][1,2]
"""
posTexto = (((ANCHO // 2)-50, (ALTO // 2) + 105),
	((ANCHO // 2)-73, (ALTO // 2) + 170),
	((ANCHO // 2)-40, (ALTO // 2) + 235))

seleccionado = 0  # marco cual va a ser el boton de menu actualmente seleccionado
salir1 = False; salirMenuInicial = False
while not salir1:
	while not salirMenuInicial:
		ventana.blit(fondoMenu, (0,0))
		#seccion seleccionar menu	
		for x in range(len(posTexto)):
			if x == seleccionado:
				ventana.blit(textos[1][x], posTexto[x])  # dibujoel texto de menu en verde
			else:
				ventana.blit(textos[0][x], posTexto[x])  # dibujo el texto de menu en naranja

		for evento in pygame.event.get():  # Hay un evento?
				if evento.type == KEYDOWN:
					if evento.key == K_ESCAPE:
						pygame.quit()  
						sys.exit()

					if evento.key == K_DOWN:
						# muevo el menu seleccionado, si llego al final del menu, reseteo y vuelvo al principio
						if seleccionado == len(posTexto)-1:
							seleccionado = 0
						else:
							seleccionado += 1

					if evento.key == K_UP:
						# muevo el menu seleccionado, si llego al principio del menu, reseteo y vuelvo al final
						if seleccionado == 0:
							seleccionado = len(posTexto)-1
						else:
							seleccionado -= 1
					if evento.key == 13:  # 13 equivale a apretar ENTER
						salirMenuInicial = True
		pygame.display.update()

	if seleccionado == 0:
		#jugadores
		velocidadJugador = 8
		velocidadBola = 10
		jugador1 = ImagenDinamica.ImagenDinamica("Imagenes/jugador1.png",ventana, velocidadJugador)  # ruta, display, velocidad de movimiento
		j1Colision = ImagenDinamica.ImagenDinamica("Imagenes/j1Colision.png",ventana, velocidadJugador) 

		jugador2 = ImagenDinamica.ImagenDinamica("Imagenes/jugador2.png",ventana, velocidadJugador)
		j2Colision = ImagenDinamica.ImagenDinamica("Imagenes/j2Colision.png",ventana, velocidadJugador)  

		bola = ImagenDinamica.ImagenDinamica("Imagenes/bolaBillar.png", ventana, velocidadBola)
		fondo = pygame.image.load("Imagenes/fondo.jpg")

		jugador1.cambiarTamanioImg(71,150)
		j1Colision.cambiarTamanioImg(71,150)

		jugador2.cambiarTamanioImg(71,150)
		j2Colision.cambiarTamanioImg(71,150)

		bola.cambiarTamanioImg(64,64)

		jugador1.setTopes(135, (ANCHO//2)-jugador1.getPixels()[0], 133, ALTO-jugador1.getPixels()[1]-60)  # defino los limites a los que se puede mover la imagen
		jugador2.setTopes((ANCHO//2), ANCHO-jugador2.getPixels()[0]-135, 133, ALTO-jugador2.getPixels()[1]-60)
		bola.setTopes(37, ANCHO-bola.getPixels()[0]-37, 135, ALTO-bola.getPixels()[1]-60)

		#SECCION VIDAS:
		pixelsVida = 50
		cantVidas = 6
		#creo 12 objetos o imagenes de vidas
		LstVidas = []
		for i in range(cantVidas*2):
			LstVidas.append(pygame.image.load("Imagenes/vida.png"))

		#Obtengo los rectangulos de cada imagen de la vida, esto me sirve para las colisiones
		LstRectVidas = []
		x = 0
		for img in LstVidas:
			LstRectVidas.append(LstVidas[x].get_rect())
			x += 1

		#POS_VIDAS ME SIRVE PARA ALINEAR LAS VIDAS EN LA PANTALLA DE FORMA HORIZONTAL y VERTICAL(x;y)
		zonaSuperior = 120
		zonaInferior = 50
		zona_juego = ALTO-zonaSuperior-zonaInferior  # esos numeros dependen del fondo que le ponga
		espacioBlanco = (zona_juego - (pixelsVida*cantVidas)) // (cantVidas+1)

		POS_VIDAS_VERTICAL = []
		for x in range(cantVidas):
			POS_VIDAS_VERTICAL.append(zonaSuperior + (espacioBlanco * (x + 1)) + (pixelsVida * x))

		POS_VIDAS_HORIZONTAL = (57, ANCHO-105)

		#CREO UNA LISTA PARA GUARDAR EL RECTANGULO DE CADA IMG DE LA VIDA 
		for x in range(cantVidas):
			LstRectVidas[x].left, LstRectVidas[x].top = POS_VIDAS_HORIZONTAL[0], POS_VIDAS_VERTICAL[x]
		i = cantVidas

		#LO MISMO PERO CON LOS QUE FALTAN DEL OTRO JUGADOR
		for x in range(cantVidas):
			LstRectVidas[i].left, LstRectVidas[i].top = POS_VIDAS_HORIZONTAL[1], POS_VIDAS_VERTICAL[x]
			i += 1

		aux = 1; score1 = 0; score2 = 0; change = -1; salirJugar = False
		# bucle de fin de partida, cuando termina la partida empezara nuevamente otra partida a partir
		# de este blucle
		
		while not salirJugar:
			# despues de cada partida la posicion change indicara la cancion a seguir
			change += 1
			if change == 5: # el numero 5 quiere decir que tengo 5 canciones
				change = 0
				
			musicFondo = pygame.mixer.Sound(MUSIC_FONDO[change])
			musicFondo.play()

			#POSICIONO A LOS JUGADORES Y LA BOLA 
			jugador1.setPos(150, (ALTO//2)-(jugador1.getPixels()[0]//2))
			jugador2.setPos(ANCHO-jugador2.getPixels()[0]-150, (ALTO-jugador2.getPixels()[0])//2)	
			bola.setPos((ANCHO//2)-(bola.getPixels()[0]//2), (ALTO//2)-(bola.getPixels()[1]//2))
			
			#POSICIONO LOS RECTANGULOS DE LOS JUGADORES Y LA BOLA
			bola.getRectangulo().left, bola.getRectangulo().top = bola.getPos()
			jugador1.getRectangulo().left, jugador1.getRectangulo().top = jugador1.getPos()
			jugador2.getRectangulo().left, jugador2.getRectangulo().top = jugador2.getPos()

			bola.setVelocidad(velocidadBola)  # reseteo la velocidad de la bola
			#ME SIRVE PARA VERIFICAR SI LAS VIDAS SIGUEN EN JUEGO O NO
			vidasOn = []
			for x in range(cantVidas*2):
				vidasOn.append(True)

			#otros

			clock = pygame.time.Clock()

			#Otras variables
			tope = True
			listTeclas = []
			diccionario = [K_w, K_s, K_a, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE]
			inicializar = True
			direccionHorizontal = 'derecha'
			direccionVertical = 'subir'
			#Variables para medir tiempo
			maxTime = 10
			initialTime = 88
			aux = int(pygame.time.get_ticks()/1000) + 1
			# guardo el tiempo en un aux, esto me sirve para que cuando comienze la partida sepa cuanto
			# tiempo paso desde que inicio la pantalla de la aplicacion y de ahi poder medir tiempo.
			#game loop
			vivo1 = True; vivo2 = True; choque = 0; auxChoque = 0; colision1 = False; colision2 = False
			while vivo1 and vivo2 and not salirJugar:

				clock.tick(60)  #declaro 60fps

				#Mido el Tiempo
				Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
				if aux == Time:
					aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
					maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
				textoTime = FuenteArial.render(str(maxTime), 0, (200, 60, 8))  # guardo el tiempo en un texto arial
				
				#Verifico si hay eventos(QUIT, apretar y soltar teclas) y hago algo
				for evento in pygame.event.get():  # Hay un evento?
					if evento.type == QUIT:  # El evento es QUIT?
						pygame.quit()  
						sys.exit()
						
					elif evento.type == KEYUP and len(listTeclas)>0:  # El evento es KEYUP? y hay algo en la lista?
							if evento.key in listTeclas:
								listTeclas.remove(evento.key)  # como deje de apretar la tecla, la quito de la lista de teclas apretadas
					
					elif evento.type == KEYDOWN:  # El evento es KEYDOWN?
						if (evento.key in diccionario) and ((evento.key in listTeclas) == False):
							listTeclas.append(evento.key)  # si la tecla no estaba en la lista, la agrego
							
				#Mover jugadores
				w, a, s, d, arriba, abajo, izquierda, derecha = False, False, False, False, False, False, False, False
				cont1, cont2 = 0, 0
				#verifico cuantas teclas y cuales teclas hay en la lista pulsadas por cada jugador
				for elemento in listTeclas:
					if elemento == K_ESCAPE: salirJugar = True; salirMenuInicial = False; musicFondo.stop()
					elif elemento == K_w: w = True; cont1+=1  # aumento el contador de teclas apretadas del jugador 1
					elif elemento == K_s: s = True; cont1+=1
					elif elemento == K_a: a = True; cont1+=1
					elif elemento == K_d: d = True; cont1+=1
					elif elemento == K_LEFT: izquierda = True; cont2+=1
					elif elemento == K_RIGHT: derecha = True; cont2+=1
					elif elemento == K_UP: arriba = True; cont2+=1
					elif elemento == K_DOWN: abajo = True; cont2+=1
				
				#si el jugador 1 apreto 3 o menos teclas quiere decir que se podra mover, sino no
				if cont1<=3:
					if w and s:  # si apreto arriba y abajo tengo que decidir a donde moverme:
						for elemento in listTeclas:  # busco en la lista el elemento mas viejo y le doy preferencia al nuevo
							if elemento == K_w:
								# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
					 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
					 			jugador1.moverAbajo()
					 			break
							if elemento == K_s:
								jugador1.moverArriba()
								break
					if a and d :  # si apreto izquierda y derecha tengo que decidir a donde moverme:
						for elemento in listTeclas:
							if elemento == K_a:
								# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
					 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
					 			jugador1.moverDer()
					 			break
							if elemento == K_d:
								jugador1.moverIzq()
								break
					if d: jugador1.moverDer()
					if s: jugador1.moverAbajo()
					if a: jugador1.moverIzq()
					if w: jugador1.moverArriba()
				

				#si el jugador 2 apreto 3 o menos teclas quiere decir que se podra mover, sino no
				if cont2<=3:
					if arriba and abajo :
						for elemento in listTeclas:
							if elemento == K_UP:
								# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
					 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
					 			jugador2.moverAbajo()
					 			break
							if elemento == K_DOWN:
								jugador2.moverArriba()
								break

					if izquierda and derecha:
						for elemento in listTeclas:
							if elemento == K_RIGHT:
								# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
					 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
					 			jugador2.moverIzq()
					 			break
							if elemento == K_LEFT:
								jugador2.moverDer()
								break
					if derecha: jugador2.moverDer()
					if abajo: jugador2.moverAbajo()
					if izquierda: jugador2.moverIzq()
					if arriba: jugador2.moverArriba()

				#Dibujo la bola y los jugadores y los rectangulos de colision
				
					if maxTime>= initialTime:
						#seguira al jugador hasta que el tiempo sea mayor a initialTime
						bola.setPosX(jugador1.getPosX()+jugador1.getPixels()[0])
						bola.setPosY(jugador1.getPosY()+jugador1.getPixels()[1]//4)
					
				#determino si choco la bola con el jugador 1, si choco, en la zona delantera del jugador
				#entonces se movera en diagonal hacia su derecha, si choco en la zona trasera, 
				#se movera en diagonal hacia su izquierda

				if bola.getRectangulo().colliderect(jugador1.getRectangulo()):
					choque += 1; colision1 = True
					if bola.getPosX() >= (jugador1.getPosX()+(jugador1.getPixels()[0]//2)):
						direccionHorizontal = 'derecha'
						reboteDelantero.play()
						if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador1.getPosY()+(jugador1.getPixels()[1]//2)))
						and (bola.getPosY()+bola.getPixels()[1]) >= jugador1.getPosY()):
							direccionVertical = 'subir'
						else:
							direccionVertical = 'bajar'
					else:
						reboteTrasero.play()
						direccionHorizontal = 'izquierda'
						if (bola.getPosY()+bola.getPixels()[1]//2) <= (jugador1.getPosY()+(jugador1.getPixels()[1]//2)):
							direccionVertical = 'subir'
						else:
							direccionVertical = 'bajar'

				#determino si choco la bola con el jugador 2, si choco, en la zona delantera del jugador
				#entonces se movera en diagonal hacia su izquierda, si choco en la zona trasera, 
				#se movera en diagonal hacia su derecha
				if bola.getRectangulo().colliderect(jugador2.getRectangulo()):
					choque += 1; colision2 = True
					if (bola.getPosX()+bola.getPixels()[0] >= jugador2.getPosX()
					and bola.getPosX()+bola.getPixels()[0] <= jugador2.getPosX()+jugador2.getPixels()[0]//2):
						reboteDelantero.play()
						direccionHorizontal = 'izquierda'
						if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador2.getPosY()+(jugador2.getPixels()[1]//2)))
						and (bola.getPosY()+bola.getPixels()[1]) >= jugador2.getPosY()):
							direccionVertical = 'subir'
						else:
							direccionVertical = 'bajar'
					else:
						reboteTrasero.play()
						direccionHorizontal = 'derecha'
						if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador2.getPosY()+(jugador2.getPixels()[1]//2)))
						and (bola.getPosY()+bola.getPixels()[1]) >= jugador2.getPosY()):
							direccionVertical = 'subir'
						else:
							direccionVertical = 'bajar'
				
				if bola.getPosY() <= bola.getTopeSuperior():
					direccionVertical = 'bajar'
				
				if bola.getPosY() >= bola.getTopeInferior():
					direccionVertical = 'subir'

				if bola.getPosX()>= bola.getTopeDerecho():
					direccionHorizontal = 'izquierda'
					#si la bola toco algun tope izquierdo o derecho, reseteo la velocidad a la inicial
					bola.setVelocidad(velocidadBola)
					choque = 0; auxChoque = 0

				if bola.getPosX() <= bola.getTopeIzquierdo():
					direccionHorizontal = 'derecha'
					#si la bola toco algun tope izquierdo o derecho, reseteo la velocidad a la inicial
					bola.setVelocidad(velocidadBola)
					choque = 0; auxChoque = 0

				if direccionHorizontal == 'derecha' and direccionVertical == 'bajar':
					bola.moverInfDerecho()
				elif direccionHorizontal == 'derecha' and direccionVertical == 'subir':
					bola.moverSupDerecho()
				elif direccionHorizontal == 'izquierda' and direccionVertical == 'bajar':
					bola.moverInfIzquierdo()
				elif direccionHorizontal == 'izquierda' and direccionVertical == 'subir':
					bola.moverSupIzquierdo()
				

				#Cuantos mas choques haga la bola con algun jugador, mas rapido ira la bola
				if choque != auxChoque:
					bola.setVelocidad(bola.getVelocidad()+ 0.1)
					auxChoque = choque

				#Verifico si hubo colisiones en alguna vida
				# y pongo la posicion de la vida en False si es que hubo alguna colision
				for x in range(cantVidas*2):
					if LstRectVidas[x].colliderect(bola.getRectangulo()):
						if vidasOn[x]:
							ripVida.play()
						vidasOn[x] = False

				cont1 = 0; cont2 = 0; x = 0 ; i = cantVidas
				for x in range(cantVidas*2):
					if x <= cantVidas-1 and vidasOn[x] == False:
						cont1 += 1
					if x > cantVidas-1 and vidasOn[x] == False:
						cont2 += 1

				#verifico si perdieron todas las vidas
				if cont1 == cantVidas: vivo1 = False;
				if cont2 == cantVidas: vivo2 = False;
			
				#Verifico si el tiempo llego a cero quien tiene mas vida y quien gano
				if maxTime == 0:
					if cont1 < cont2:
						vivo2 = False
					elif cont1 > cont2:
						vivo1 = False
					elif cont1 == cont2:
						vivo1 = False
						vivo2 = False

				#Dibujo el fondo
				ventana.blit(fondo, (0,0))  

				#Dibujo las vidas del jugador 1 y del jugador 2 si y solo si la vida esta presente
				i = 0; x = 0
				for vida in LstVidas:
					if i <= cantVidas-1 and vidasOn[i]: 
						ventana.blit(vida, (POS_VIDAS_HORIZONTAL[0],POS_VIDAS_VERTICAL[x]))
					if i > cantVidas-1 and vidasOn[i]:
						ventana.blit(vida, (POS_VIDAS_HORIZONTAL[1],POS_VIDAS_VERTICAL[x]))
					x += 1
					i += 1
					if x == cantVidas:
						x = 0

				#dibujo la bola
				bola.getRectangulo().left, bola.getRectangulo().top = bola.getPos()
				bola.dibujarImg(*bola.getPos())
				
				#dibujo los jugadores
				jugador1.getRectangulo().left, jugador1.getRectangulo().top = jugador1.getPos() 
				#verifico si el j1 colisiono para saber que img de j1 mostrar 
				if colision1:
					j1Colision.dibujarImg(*jugador1.getPos())  # Dibujo la img de colision
				else:
					jugador1.dibujarImg(*jugador1.getPos())  # Dibujo al jugador 1, uso un * ya que le paso una tupla
					
				jugador2.getRectangulo().left, jugador2.getRectangulo().top = jugador2.getPos()
				#verifico si el j2 colisiono para saber que img de j2 mostrar 
				if colision2:
					j2Colision.dibujarImg(*jugador2.getPos())  # Dibujo la img colision
				else:
					jugador2.dibujarImg(*jugador2.getPos())  # Dibujo al jugador 2

				colision2, colision1 = False, False
				

				#dibujo el tiempo
				ventana.blit(textoTime, ((ANCHO/2)-24, 55))  

				#genero los scores
				textoScore1 = FuenteArial2.render(str(score1), 0, ORANGE)  
				textoScore2 = FuenteArial2.render(str(score2), 0, ORANGE)   
				#dibujo los scores
				ventana.blit(textoScore1, (150, 60))  # imprimo el score1
				ventana.blit(textoScore2, ((ANCHO-170), 60))  # imprimo el score2
				
				#actualizo la pantalla
				pygame.display.update()

				#si perdio el jugador 1, esperare 3 segundos y mostrare un msj que gano el jugador2
				if vivo1 == False and vivo2:
					musicFondo.stop()
					win.play()
					score2 += 1
					#Mido el Tiempo
					maxTime = 3
					aux = int(pygame.time.get_ticks()/1000) + 1 
					textoGano = FuenteArial.render("Player 2 Win", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

					while maxTime!=0:
						Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
						ventana.blit(textoGano, ((ANCHO/2)-140, (ALTO//2)-30))  # imprimo el texto
						pygame.display.update()

						if aux == Time:
							aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
							maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
				#si perdio el jugador 2, esperare 3 segundos y mostrare un msj que gano el jugador1
				if vivo2 == False and vivo1:
					musicFondo.stop()
					win.play()
					score1 += 1
					#Mido el Tiempo
					maxTime = 3
					aux = int(pygame.time.get_ticks()/1000) + 1 
					textoGano = FuenteArial.render("Player 1 Win", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

					while maxTime!=0:
						Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
						ventana.blit(textoGano, ((ANCHO/2)-140, (ALTO//2)-30))  # imprimo el texto
						pygame.display.update()

						if aux == Time:
							aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
							maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
				if vivo2 == False and vivo1 == False:
					musicFondo.stop()
					draw.play()
					score1 += 1
					score2 += 1
					#Mido el Tiempo
					maxTime = 3
					aux = int(pygame.time.get_ticks()/1000) + 1 
					textoDraw = FuenteArial.render("Draw", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

					while maxTime!=0:
						Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
						ventana.blit(textoDraw, ((ANCHO/2)-50, (ALTO//2)-30))  # imprimo el texto
						pygame.display.update()

						if aux == Time:
							aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
							maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado

				#en cualquier caso que halla ganado alguien o sea draw, entrara aca
				if (not vivo2 and vivo1) or (vivo2 and not vivo1):
					textoIngreseNombre = FuenteArial.render('Ingrese su Nombre:', 0, (200, 60, 8)) 
					textoNombre = FuenteArial.render('', 0, (200, 60, 8)) 
					diccionario2 = [K_a, K_b, K_c, K_d, K_e, K_f, K_a, K_g, K_h, K_i, K_j, K_k, 
					K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_t, K_z, 8,
					32]
					nombre = ''
					salirRank = False 
					#mientras no ingrese su nombre o aprete escape imprimira todo el fondo
					#nuevamente a como estaba antes de ganar,o perder  esto me sirve para
					#poder mostrar el nombre del jugador a como valla apretando las teclas
					#sin perder el fondo del juego
					while not salirRank:
						#Dibujo el fondo
						ventana.blit(fondo, (0,0))  

						#Dibujo las vidas del jugador 1 y del jugador 2 si y solo si la vida esta presente
						i = 0; x = 0
						for vida in LstVidas:
							if i <= cantVidas-1 and vidasOn[i]: 
								ventana.blit(vida, (POS_VIDAS_HORIZONTAL[0],POS_VIDAS_VERTICAL[x]))
							if i > cantVidas-1 and vidasOn[i]:
								ventana.blit(vida, (POS_VIDAS_HORIZONTAL[1],POS_VIDAS_VERTICAL[x]))
							x += 1
							i += 1
							if x == cantVidas:
								x = 0

						#dibujo la bola
						bola.dibujarImg(*bola.getPos())
						
						#dibujo los jugadores
						jugador1.dibujarImg(*jugador1.getPos())  # Dibujo al jugador 1, uso un * ya que le paso una tupla
						jugador2.dibujarImg(*jugador2.getPos())  # Dibujo al jugador 2

						#dibujo el tiempo
						ventana.blit(textoTime, ((ANCHO/2)-24, 55))  

						#genero los scores
						textoScore1 = FuenteArial2.render(str(score1), 0, ORANGE)  
						textoScore2 = FuenteArial2.render(str(score2), 0, ORANGE)   
						
						#dibujo los scores
						ventana.blit(textoScore1, (150, 60))  # imprimo el score1
						ventana.blit(textoScore2, ((ANCHO-170), 60))  # imprimo el score2
						
						#imprimo 'Ingrese su Nombre'
						ventana.blit(textoIngreseNombre, ((ANCHO/2)-190, (ALTO//2)-70)) 

						#Pregunto si es que se apreto la tecla ESC para salir del menu
						for evento in pygame.event.get():  # Hay un evento?
							if evento.type == KEYDOWN:
								if evento.key == K_ESCAPE:
									salirRank = True
								if evento.key in diccionario2:
									if evento.key == K_BACKSPACE:  #retroceso
										#Esta sección elimina la ultima letra cuando se detecta un backspace,
										#mueve todos los caracteres de la cadena original excepto el ultimo a una
										#auxiliar y luego reemplaza la original por la auxiliar
										nombreAux = ""
										for j in range(0, len(nombre) - 1):
											nombreAux = nombreAux + nombre[j]
										nombre = nombreAux
									else:
										if(len(nombre)<20):  # 20 es el numero maximo del nombre
											nombre = nombre + chr(evento.key)  # chr pasa un numero ascii a su valor correspondiente en char
									textoNombre = FuenteArial.render(nombre, 0, (200, 60, 8))
								if evento.key == 13:  # 13 equivale a apretar ENTER
									#1-abrir el archivo1 como read y el archivo 2 como escritura
									#2-leer linea por linea el archivo1 y buscar si hay un nombre igual al ingresado
									#e ir pasando linea por linea al archivo Scores2.txt
									#3-si hay un nombre igual en una linea: omito esa linea, agarro el valor que tenia 
									#y le sumo uno, y lo sigo pasando al scores2.txt .
									#4-si no hay ningun nombre igual: guardar el nombre al final del archivo en conjunto 
									#con el puntaje total que sera 1 ya que es la primera ves que aparece
									#5-cierro el archivo scores y scores2.txt
									#6-elimino scores y renombro scores2.txt a scores
									punteroScores = open(fileScores, "a+")  # 1-fileScores esta declarado el inicio del programa
									punteroScores2 = open(fileScores2, 'w')
									eof = False; esta = False
									punteroScores.seek(0)
									while not eof:
										linea = punteroScores.readline()  #2-leo una linea
										lineaScore = ''; lineaNombre = ''; seccionNumero = False
										#aca separo la aprte de nombre de la parte del score de la linea leida
										for x in range (len(linea)):
											if linea[x] == '-':
												seccionNumero = True
												
											if seccionNumero:
												if linea[x].isdigit():
													lineaScore = lineaScore + linea[x]
											else:
												lineaNombre = lineaNombre + linea[x]

										if lineaNombre == nombre:
											esta = True  # el nombre ya estaba registrado
											lineaScore = str(int(lineaScore) + 1)  # al score que tenia le sumo 1

										#si llegue al final del archivo saldre
										if linea == '':  
											punteroScores.close()
											punteroScores2.close()
											os.remove("Scores.txt")
											os.rename("Scores2.txt", "Scores.txt")							
											eof = True
										else:
											linea = lineaNombre + '-' + lineaScore + '\n'
											punteroScores2.write(linea)  # Escribo en el archivo 2 la linea
									if not esta:
										punteroScores = open(fileScores, "a")  # 1-fileScores esta declarado el inicio del programa
										punteroScores.write(nombre + '-' + '1' + '\n')
										punteroScores.close()
									salirRank = True

						ventana.blit(textoNombre, ((ANCHO/2)-190, (ALTO//2)))  # imprimo 'Ingrese su Nombre'		
						pygame.display.update()
#-------------------------------------------------------------------------------------
	elif seleccionado == 1: # PARTE DEL MENU "SECCION SCORES"
		eof = False; menuScores = True; sumaPosTexto = 80; top = 10; cont = 0
		ventana.fill(WHITE)
		punteroScores = open(fileScores, "r")  # fileScores esta declarado el inicio del programa

		textoTitulo = FuenteArial2.render('TOP RANKINGS', 0, ORANGE)
		textoSubtitulo = FuenteArial2.render('#RANK    NOMBRE    SCORE', 0, ORANGE) 

		ventana.blit(textoTitulo, ((ANCHO//2)-90,20))
		ventana.blit(textoSubtitulo, ((ANCHO//2)-190,100))
		cont = 0
		while menuScores:  # mientras no aprete ESC no saldre del menu de Scores
			magnus = open('Scores.txt', 'r')
			posicionesMax = []
			top = 10
			nombreMax = ''; scoreMax = -1; 
			while cont < top:
				linea = magnus.readline() # lee la primera
				lineaScore = '0'; lineaNombre = ''; seccionNumero = False

				for x in range (len(linea)):
					if linea[x] == '-':
						seccionNumero = True

					if seccionNumero:
						if linea[x].isdigit():
							lineaScore = lineaScore + linea[x]
					else:
						lineaNombre = lineaNombre + linea[x]

				if (int(lineaScore) > scoreMax) and (lineaNombre not in posicionesMax):
					scoreMax = int(lineaScore)
					nombreMax = lineaNombre

				#si llegue al final del archivo saldre
				if linea == '':  
					posicionesMax.append(nombreMax)
					magnus.seek(0)
					cont += 1
					textoNombre = FuenteArial2.render(nombreMax, 0, ORANGE)
					textoScore = FuenteArial2.render(str(scoreMax), 0, ORANGE) 
					textoRank = FuenteArial2.render(str(cont), 0, ORANGE)
					scoreMax = -1

					sumaPosTexto += 50 # me sirve para posicionar el texto

					ventana.blit(textoNombre, ((ANCHO//2)-40, 50+sumaPosTexto))
					ventana.blit(textoScore, ((ANCHO//2)+180, 50+sumaPosTexto))
					ventana.blit(textoRank, ((ANCHO//2)-180, 50+sumaPosTexto))
			punteroScores.close()
			#Pregunto si es que se apreto la tecla ESC para salir del menu
			for evento in pygame.event.get():  # Hay un evento?
				if evento.type == KEYDOWN:
					if evento.key == K_ESCAPE:
						menuScores = False  
						salirMenuInicial = False  # lo pongo en false porque sino no pueo volver al menu inicial
			pygame.display.update()

	# SECCION MENU EXIT
	elif seleccionado == 2:
		pygame.quit()
		salir1 = True

