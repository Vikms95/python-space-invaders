import pygame
from pygame.sprite import Sprite

class Metroid(Sprite):
   
    '''Clase que controla un metroid y su posición'''
    
    def __init__(self, ai_settings, screen):
        
        #Crea el metroid y su poción de inicio
        super(Metroid, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # Carga la imagen del alien y le atribuye un rectángulo
        self.image = pygame.image.load("C:/Python/Practicas/spaceinvaderspractica/imagenes/metroidLarva.bmp")
        self.image = pygame.transform.scale(self.image,(120,90))
        self.rect = self.image.get_rect()
        
        # Coloca cada metroid en la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posición del metroid en decimales
        self.x = float(self.rect.x)
    def update(self):
        
        #Mueve el metroid hacia la derecha o izquierda
        self.x += (self.ai_settings.metroid_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):

        # Dibuja al metroid en la localización del rectángulo
        self.screen.blit(self.image,self.rect)

    def check_edges (self):

         # Devuelve 'True' si el metroid está en el borde de la pantalla 
        screen_rect = self.screen.get_rect()
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
