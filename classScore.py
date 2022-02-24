import pygame.font
from classShip import Ship
from pygame.sprite import Group


class Scoreboard:
    
    " Clase que controla la información relacionada con la puntuación de las partidas"
    
    def __init__(self, ai_settings, screen, stats):
        
        # Inicia los atributos que guardan las puntuaciones
        self.screen = screen
        self.screen_rect  = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Fuente de las puntuaciones
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara la imagen de la puntuación
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):

        # Convierte la puntuación en una imagen renderizada
        score_str = str(self.stats.score)

        rounded_score = int(round(self.stats.score, - 1))
        score_str = "{:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Coloca la puntuación en la parte superior-derecha de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 10
        self.score_rect.top = 20
    
    def prep_high_score(self):

        # Convierte la puntuación más alta en una imagen renderizada
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Centra la puntuación más alta en la parte superior de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):

        # Convierte el número del nivel en una imagen renderizada
        self.level_image = self.font.render("Fase " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Coloca la imagen del nivel debajo de la puntuación
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 1090
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):

        # Enseña cuantas naves quedan
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = ship.imageIcon
            ship.rect.x = 950 + ship_number * (ship.rect.width - 80)
            ship.rect.y = 20
            self.ships.add(ship)

    def show_score(self):

        # Muestra la puntuación en pantalla
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Dibuja los iconos de vidas de la nave
        self.ships.draw(self.screen)