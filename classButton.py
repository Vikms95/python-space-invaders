import pygame.font

class Button():
    
    "Clase que controla los botones que aparecen en pantalla"
   
    def __init__ (self, ai_settings, screen, msg):
        
        # Inicia los atributos de la clase Button
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Marca las dimensiones y propiedades de Button
        self.width, self.height = 375,150
        self.button_color = (0,0,255)
        self.text_color = (255,255,170)
        self.font = pygame.font.SysFont(None, 48)

        # Construye el rectángulo del boton y lo centra
        self.rect = pygame.Rect(0, 0 ,self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prepara el mensaje del botón
        self.prep_msg(msg)
    
    def prep_msg(self,msg):
        
        # Convierte el mensaje en imagen y la centra en el rectángulo del botón
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):

        # Dibuja el botón y el mensaje
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        #self.draw_rect(self.screen, 15, 20, self.rect)
    
    '''def draw_rect(screen, fill_color, outline_color, rect, border= 1):
        screen.fill(outline_color, rect)
        screen.fill(fill_color, rect.inflate(-border*2, -border*2))'''