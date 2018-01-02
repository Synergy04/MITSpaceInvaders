# johanc
import sys
import pygame
from laser import Laser
from enemy import Enemy
from time import sleep


def check_events(ai_settings, screen, stats, sb, play_button, ship, enemies, lasers):
    """Listens for key and mouse events"""
    for event in pygame.event.get():
        # Game exit
        if event.type == pygame.QUIT:
            sys.exit()
        # Move right or left
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, lasers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemies, lasers, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemies, lasers, mouse_x, mouse_y):
    """Starts game when button clicked"""
    clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if clicked and not stats.game_active:
        stats.reset_stats()
        ai_settings.initialize_dynamic_settings()
        stats.game_active = True
        # Resets scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Hides mouse
        pygame.mouse.set_visible(False)
        enemies.empty()
        lasers.empty()

        create_fleet(ai_settings, screen, ship, enemies)
        ship.center_ship


def check_keydown_events(event, ai_settings, screen, ship, lasers):
    """Responds to key presses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_laser(ai_settings, screen, ship, lasers)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Key release listener"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_lasers(ai_settings, screen, stats, sb, ship, lasers, enemies):
    """Updates position and deletes old lasers"""
    lasers.update()
    for laser in lasers.copy():
        if laser.rect.bottom <= 0:
            lasers.remove(laser)
    check_laser_alien_collision(ai_settings, screen, stats, sb, ship, lasers, enemies)


def update_enemies(ai_settings, stats, screen, sb, ship, enemies, lasers):
    """Updates position of all enemies"""
    check_fleet_edges(ai_settings, enemies)
    enemies.update()

    # Check if the fleet collided with the ship
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(ai_settings, stats, sb, screen, ship, enemies, lasers)
        print("Houston we have a problem.")
    check_enemies_bottom(ai_settings, stats, screen, sb, ship, enemies, lasers)


def fire_laser(ai_settings, screen, ship, lasers):
    """Fires deadly lasers"""
    if len(lasers) < ai_settings.lasers_allowed:
        new_laser = Laser(ai_settings, screen, ship)
        lasers.add(new_laser)


def ship_hit(ai_settings, stats, sb, screen, ship, enemies, lasers):
    """Responds to ship being hit"""
    if stats.ships_left > 0:
        # Decreases ship count
        stats.ships_left -= 1
        # Update scoreboard
        sb.prep_ships()
        # Resets to beginning status
        enemies.empty()
        lasers.empty()

        # Creates fleet and resets ship
        create_fleet(ai_settings, screen, ship, enemies)
        ship.center_ship()

        # Breather
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def create_fleet(ai_settings, screen, ship, enemies):
    """Full fleet of enemies"""
    # Finds the number of enemies that can fit in the screen
    # One enemy width between enemies
    enemy = Enemy(ai_settings, screen)
    number_enemies_x = get_number_of_enemies_x(ai_settings, enemy.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, enemy.rect.height)

    # Creates fleet
    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(ai_settings, screen, enemies, enemy_number, row_number)


def get_number_of_enemies_x(ai_settings, enemy_width):
    """Finds number of enemies that fit in the screen per row"""
    space_available = ai_settings.screen_width - (2 * enemy_width)
    number_of_enemies = int(space_available / (2 * enemy_width))
    return number_of_enemies


def create_enemy(ai_settings, screen, enemies, enemy_number, row_number):
    """Create an enemy and add it to the row"""
    enemy = Enemy(ai_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)


def get_number_rows(ai_settings, ship_height, enemy_height):
    """Determines number of rows"""
    available_space_y = (ai_settings.screen_height - (3 * enemy_height) - ship_height)
    number_rows = int(available_space_y / (2 * enemy_height))
    return number_rows


def change_fleet_direction(ai_settings, enemies):
    """Drop vertically and change direction"""
    for enemy in enemies.sprites():
        enemy.rect.y += ai_settings.drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, enemies):
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(ai_settings, enemies)
            break


def check_laser_alien_collision(ai_settings, screen, stats, sb, ship, lasers, enemies):
    """Responds to collisions"""
    collisions = pygame.sprite.groupcollide(lasers, enemies, True, True)
    if collisions:
        for enemies in collisions.values():
            stats.score += ai_settings.enemy_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(enemies) == 0:
        # Destroy bullets, create new enemies. They're relentless. And faster. New level starts
        lasers.empty()
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, enemies)


def check_enemies_bottom(ai_settings, stats, screen, sb, ship, enemies, lasers):
    """Check if enemies hit the bottom, if so, you lose a ship"""
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, enemies, lasers)
            break


def check_high_score(stats, sb):
    """Check if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, enemies, lasers, play_button):
    """Refresh image and transition to new screen"""
    # Redraw with every loop
    screen.fill(ai_settings.bg_color)
    for laser in lasers.sprites():
        laser.draw_laser()
    ship.blitme()
    enemies.draw(screen)
    # Draw the play button and scoreboard
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
