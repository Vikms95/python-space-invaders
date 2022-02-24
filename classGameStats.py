class GameStats():
    
    # Controla las estadisticas del videojuego
    def __init__(self,ai_settings):

        # Inicia las estadísticas
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False


        # Variable para que la puntuación más alta nunca se resetee
        self.high_score = 0
    
    def reset_stats(self):
        
        # Inicia el recuento de estadísticas que pueden cambiar durante el proceso
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
