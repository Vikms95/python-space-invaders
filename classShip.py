import pygame
import functions as f
from pygame.sprite import Sprite

class Ship(Sprite):

    '''Clase que controla la nave y su posición'''
    
    def __init__(self,ai_settings,screen):
        
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Carga la imagen de la nave y determina sus dimensiones
        self.image = pygame.image.load("C:/Python/Practicas/spaceinvaderspractica/imagenes/samusShip.bmp")
        self.image = pygame.transform.scale(self.image,(150,80))
        self.imageIcon = pygame.transform.scale(self.image, (60,35))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Coloca cada nave nueva en la parte inferior del centro de la pantalla
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = (self.screen_rect.bottom-25)
        
        # Pasa los valores de self.center a float
        self.center = float(self.rect.centerx)

        # Determina hacia donde se mueve la nave
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme (self):
        
        # Dibuja la nave en su actual posición
        self.screen.blit(self.image, self.rect)
    
    def blit_icon(self):

        # Dibuja la nave en tamaño icono
        self.screen.blit(self.imageIcon, self.rect)
    
    def update (self):
        
        # Pone la nave en estado de movimiento y limita la movilidad de la nave hasta bordes
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_up and self.rect.top > 0:
            self.rect.centery -= 0.5
        elif self.moving_down and self.rect.bottom < (self.screen_rect.bottom-25):
            self.rect.centery += 1

        # Actualiza la posición de la nave basado en puntos de movimiento
        self.rect.centerx = self.center
    
    def center_ship(self):

        # Center the ship on the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = (self.screen_rect.bottom-25)