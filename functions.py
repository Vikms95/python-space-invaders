import sys
from time import sleep
import pygame
import random
from pygame import mixer
#
from classBullet import Bullet
from classMetroid import Metroid



def check_keydown_events(event, ai_settings, screen, ship, bullets):
    
    #Reacciona a pulsaciones de botones
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, ship, screen, bullets)
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    
    # Reacciona a botones soltándose
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, metroids, bullets, mouse_x, mouse_y):

    # Empieza un nuevo juego cuando el jugador clicka el botón "Play"
    if play_button.screen_rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.screen_rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Resetea las estadísticas de juego
            stats.reset_stats()
            ai_settings.initialize_dynamic_settings()
            stats.game_active = True

            # Esconde el cursor del ratón
            pygame.mouse.set_visible(False)

            #Reinicia la imagen de la tabla de puntuaciones
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Vacía la lista de metroids y balas
            metroids.empty()
            bullets.empty()

            # Crea una nueva flota y centra la nave
            create_fleet(ai_settings, screen, ship, metroids)
            ship.center_ship()

def check_events(ai_settings, screen, stats, sb, play_button, ship, metroids, bullets):
    
     # Controla cualquier comando ejecutado desde teclado/ratón
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, metroids, bullets, mouse_x, mouse_y)

def check_bullet_metroid_collisions(ai_settings, screen, stats, sb,  ship, metroids, bullets):
    
    # Comprueba si alguna bala ha golpeado un metroid
    collisions = pygame.sprite.groupcollide(bullets, metroids, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.metroid_points + len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    # Comprueba si todavía quedan metroids en la flota después del último que desaparece, para repoblar la flota y aumentar la velocidad del juego
    if len(metroids) == 0:

        # Si la flota entera es destruida, empieza un nuevo nivel
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen , ship , metroids)

        # Incrementa el nivel
        stats.level += 1
        sb.prep_level()

def check_metroids_bottom(ai_settings, screen, sb, stats, ship, metroids, bullets):
    
    # Controla si algún metroid ha llegado al borde inferior de la pantalla
    screen_rect = screen.get_rect()
    for metroid in metroids.sprites():
        if metroid.rect.bottom >= screen_rect.bottom:

            # Un metroid que toca la parte inferior es tratado igual a un alien tocando la nave
            ship_hit(ai_settings, stats, screen, sb, ship, metroids, bullets)
            break

def check_high_score(stats,sb):

    # Comprueba si hay una nueva puntuación máxima
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

#

def update_screen(ai_settings, screen, stats, sb, ship, bullets, metroids, play_button):
    
    # Pasa el color de fondo y dibuja la nave para cada pase de bucle
    screen.fill(ai_settings.bg_color)
    
    # Crea el patrón de estrellas para cada pase de bucle
    #create_star_pattern(ai_settings, screen)

    # Redibuja los proyectiles de la nave detrás de la nave y los metroid
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Dibuja los sprites en pantalla
    ship.blitme()
    metroids.draw(screen)

    # Dibuja la tabla de puntuaciones
    sb.show_score()
    
    # Dibuja el botón de Play si el juego está inactivo
    if not stats.game_active:
        play_button.draw_button()

def update_bullets(ai_settings, screen, stats, sb, ship, metroids, bullets):
    bullets.update()
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    
    check_bullet_metroid_collisions(ai_settings, screen, stats, sb, ship, metroids, bullets)
    
def update_metroids(ai_settings, screen, stats, sb, ship, metroids, bullets):

    # Comprueba si la flota está en el borde y después, actualiza la posición de todos los aliens en la flota
    check_fleet_edges(ai_settings, metroids)
    metroids.update()

    # Comprueba colisiones entre metroids-nave
    if pygame.sprite.spritecollideany(ship, metroids):
        ship_hit(ai_settings, stats, screen, sb, ship, metroids, bullets)

    # Comprueba si hay metroids golpeando el borde inferior
    check_metroids_bottom(ai_settings, screen, stats, sb, ship, metroids, bullets)

def ship_hit(ai_settings, stats, screen, sb, ship, metroids, bullets):

    if stats.ships_left > 0:    

        # Reacciona a la nave siendo golpeado, quitándole un valor a ship_hit
        stats.ships_left -= 1

        # Actualiza la tabla de puntuaciones
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        metroids.empty()
        bullets.empty()

        # Crea una nueva flota y centra la nave
        create_fleet(ai_settings,screen, ship, metroids)
        ship.center_ship()

        # Reproduce el sonido de la nave destruyéndose
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("C:/Python/Practicas/spaceinvaderspractica/sonidos/naveexplosion.mp3"))

        
        # Da tiempo al jugador para reincorporarse
        sleep(1.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

#

def fire_bullet(ai_settings, ship, screen, bullets):
    if len(bullets) < ai_settings.bullets_allowed:        
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("C:/Python/Practicas/spaceinvaderspractica/sonidos/blastsound.mp3"))

#

def get_number_metroid_x(ai_settings, metroid_width):
   
    # Encuentra el numero de metroids en una fila
    # El espaciado entre metroids es igual a la mitad de la anchura de su rectángulo (.rect)
    available_space_x = ai_settings.screen_width - (metroid_width)
    number_metroid_x = int(available_space_x / (metroid_width))
    return number_metroid_x

def get_number_rows(ai_settings, ship_height, metroid_height):

    # Determina el número de filas que caben en la pantalla
    available_space_y = (ai_settings.screen_height - (3 * metroid_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * metroid_height))
    return number_rows

#

def create_metroid (ai_settings, screen, metroids, metroid_unit, row_number):
    
    # Crea un metroid y lo coloca en la fila
    metroid = Metroid(ai_settings,screen)
    metroid_width = (metroid.rect.width / 2)
    metroid.x = metroid_width + 2 * metroid_width * metroid_unit
    metroid.rect.x = metroid.x
    metroid.rect.y = metroid.rect.height + metroid.rect.height * row_number
    metroids.add(metroid)

def create_fleet(ai_settings, screen, ship, metroids):

    # Crea una flota entera de metroids
    metroid = Metroid(ai_settings, screen)
    number_metroids_x = get_number_metroid_x(ai_settings, metroid.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, metroid.rect.height)

    # Crea la primera fila de metroids
    for row_number in range(number_rows):    
        for metroid_unit in range (number_metroids_x):   
            create_metroid(ai_settings, screen, metroids, metroid_unit,row_number)    

def check_fleet_edges(ai_settings, metroids):
    
    # Responde apropiadamente si algún metroid está tocando el borde
    for metroid_unit in metroids.sprites():
        if metroid_unit.check_edges():
            change_fleet_direction(ai_settings,metroids)
            break

def change_fleet_direction(ai_settings, metroids):

    # La flota entera baja una fila y cambia de dirección
    for metroid_unit in metroids.sprites():
        metroid_unit.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def create_star_pattern(ai_settings, screen):
    
    # Define las localizaciones de las estrellas
    star_field_slow = []
    star_field_medium = []
    star_field_fast = []

    clock = pygame.time.Clock()

    for slow_stars in range (50):
        star_loc_x = random.randrange(0 , ai_settings.screen_width)
        star_loc_y = random.randrange(0, ai_settings.screen_height)
        star_field_slow.append([star_loc_x, star_loc_y])


    for medium_stars in range (35):
        star_loc_x = random.randrange(0, ai_settings.screen_width)
        star_loc_y = random.randrange(0, ai_settings.screen_height)
        star_field_medium.append([star_loc_x, star_loc_y])


    for fast_stars in range(15):
        star_loc_x = random.randrange(0, ai_settings.screen_width)
        star_loc_y = random.randrange(0, ai_settings.screen_height)
        star_field_fast.append([star_loc_x, star_loc_y])


        for star in star_field_slow:
            star[1] += 1
            if star[1] > ai_settings.screen_height:
                star[0] = random.randrange(0, ai_settings.screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, (255,255,255), star, 3)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > ai_settings.screen_height:
                star[0] = random.randrange(0, ai_settings.screen_width)
                star[1] = random.randrange(-20,-5)
            pygame.draw.circle(screen, (255,255,255), star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > ai_settings.screen_height:
                star[0] = random.randrange(0,ai_settings.screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, (255,255,255), star, 1)



