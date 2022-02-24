'''
    - Mejorar Button()
    - Fondo con estrellas generadas con patrón aleatorio aleatoriamente(#)
    - Añadir WASD
    - Añadir más sonidos (pygame.mixer)
    - Powerups para cambiar velocidad de nave
    - Hacer metroids animados (GIF?)
    - Ordenar y poner la misma palabra en el mismo tipo de funciones

'''
  
#---------------

import pygame
from pygame.sprite import Group
from pygame import mixer
import random

#

from settings import Settings
from classGameStats import GameStats
from classShip import Ship
from classMetroid import Metroid
from classButton import Button
from classScore import Scoreboard

#

import functions as f

#---------------

def run_game():

    # Crea la ventana e inicia el juego
    
    pygame.init()
    
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Pirates by Víctor Martín")
    icon = pygame.image.load("C:\Python\Practicas\practicaspaveinvaders\imagenes\game_icon.png")
    pygame.display.set_icon(icon)
    
    stats = GameStats (ai_settings) # Almacena estadísticas de juego
    sb = Scoreboard(ai_settings, screen, stats) # Crea una instancia para almacenar estadísticas de juego y mostrarlas en una tabla
    ship = Ship(ai_settings,screen) # Dibuja la nave una vez
    metroid = Metroid(ai_settings, screen) # Crea una instancia de la clase Metroid
    play_button = Button(ai_settings, screen, "Empieza la misión") # Crea el botón "Empieza la misión"
    
    # Crea un grupo de proyectiles y de metroids
    bullets = Group() 
    metroids = Group()
    
    f.create_star_pattern(ai_settings,screen)
    f.create_fleet(ai_settings, screen, ship, metroids)

    # Inicia la música de fondo en bucle

    pygame.mixer.Channel(0).play(pygame.mixer.Sound("C:\Python\Practicas\practicaspaveinvaders\sonidos\itemroom.mp3"))

    while True: # Inicia el bucle para el juego
        
        f.check_events(ai_settings, screen, stats, sb, play_button, ship, metroids, bullets) # Comprueba input del jugador
        
        if stats.game_active: 
            ship.update() # Actualiza de la nave
            f.update_bullets(ai_settings, screen, stats, sb, ship, metroids,bullets) # Actualiza la posición de los proyectiles
            f.update_metroids(ai_settings, screen, stats, sb, ship, metroids, bullets) # Actualiza la posición de los metroids
        
        f.update_screen(ai_settings, screen, stats, sb, ship, bullets, metroids, play_button) # Actualiza con nuevos datos la pantalla
        pygame.display.flip() # Hace que la ventana creada más recientemente sea visible y esconde la anterior


run_game()

