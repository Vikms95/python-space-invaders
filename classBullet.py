import pygame
from pygame.sprite import Sprite

class Bullet (Sprite):

    ''' Clase que controla los proyectiles y su comportamiento'''
    
    def __init__(self, ai_settings, screen, ship):
        
        # Crea un rectángulo en la actual posición de la nave
        super(Bullet, self).__init__()
        self.screen = screen

        # Crea unas coordenadas rectangulares en (0,0) y coloca el rectangulo justo en la parte superior de la nave
        self.rect = pygame.Rect(0,0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Almacena la posición del proyectil como valor decimal
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update (self):

        # Actualiza el rectángulo en pantalla en decimales. Si la bala sube a través de la pantalla, el valor Y de la nave disminuye
        self.y -= self.speed_factor
        # Actualiza la posición de la nave de acuerdo con la del rectangulo 
        self.rect.y = self.y
    
    def draw_bullet(self):

        # Dibuja el proyectil en pantalla
        pygame.draw.rect(self.screen, self.color, self.rect)