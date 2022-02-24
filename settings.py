class Settings():
    
    "Ajustes de juego estáticos"
    
    def __init__(self):
    
    # Ajustes de pantalla
        self.ship_speed_factor = 0
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,5)
        
    # Ajustes de proyectiles
        self.bullet_speed_factor = 0.8
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (180,255,0)
        self.bullets_allowed = 2
    
    # Ajustes de metroids
        self.metroid_speed_factor = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 = derecha; -1 = izquierda

    # Ajustes de nave
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

    # Ajustes de velocidad de juego
        self.speedup_scale = 1.05
    
    # Ajustes color estrellas
        '''self.WHITE = (255,255,255)
        self.GREY = (192,192,192)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)
        self.colorList = [(255,255,255),(192,192,192),(255,0,0),(0,0,255),(255,255,0)]'''
    
    # Ajustes de aumento de puntos otorgados por metroid
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        
        # Inicia los ajustes que cambiarán a lo largo de la partida
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1
        self.metroid_speed_factor = 0.1

        # 1= Derecha; -1 = Izquierda
        self.fleet_direction = 1

        # Valor puntuaciones
        self.metroid_points = 50
        
    def increase_speed(self):

        # Incrementa la configuración de velocidad y los puntos otorgados por metroid
        self.ship_speed_factor += 0.05
        self.bullet_speed_factor + 0.05
        self.metroid_speed_factor *= self.speedup_scale

        self.metroid_points = int(self.metroid_points * self.score_scale)