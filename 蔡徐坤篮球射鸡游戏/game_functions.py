#coding:gbk

import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
        play_button):
    '''������Ļ�ϵ�ͼ���л�������Ļ'''
    #ÿ��ѭ�������»�����Ļ
    screen.fill(ai_settings.bg_color)
     #�ڷɴ��������˺����ػ������ӵ�
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    #����PLAY��ť
    if not stats.game_active:
        play_button.draw_button()
    #�û��Ƶ���Ļ�ɼ�
    pygame.display.flip()
    

    
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''��Ӧ����'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event,ship):
    '''��Ӧ�ɿ�'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,
        bullets):
    '''��Ӧ����������¼�'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,
                ship,aliens,bullets,mouse_x,mouse_y)
            
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''�����ӵ����ò�ɾ���Ѿ���ʧ���ӵ�'''
    #�����ӵ���λ��
    bullets.update()
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    #ɾ���Ѿ���ʧ���ӵ�
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    '''�����û�е������ƾͷ���һ���ӵ�'''
    #�������ӵ���������뵽bullets��
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        
def get_number_aliens_x(ai_settings,alien_width):
    '''����һ�п������ɶ��ٸ�������'''
    avaiable_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(avaiable_space_x/(2*alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #����һ��������
     alien = Alien(ai_settings,screen)
     alien_width = alien.rect.width
     alien.x = alien_width + 2*alien_width*alien_number
     alien.rect.x = alien.x
     alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
     aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    '''����������Ⱥ'''
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,
        alien.rect.height)
    #����������
    for row_number in range(number_rows - 2):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,
                row_number)
    
def get_number_rows(ai_settings,ship_height,alien_height):
    '''������Ļ�������ɶ�����������'''
    available_space_y = (ai_settings.screen_height -
                    (3*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows
    
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    '''���������������е�������λ��'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
def check_fleet_edges(ai_settings,aliens):
    '''�������˵�����Ļ��Եʱ��ȡ��Ӧ��ʩ'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
            
def change_fleet_direction(ai_settings,aliens):
    '''����Ⱥ���������Ʋ��ı����ǵķ���'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,ship,aliens,bullets):
    '''��Ӧ������ײ���ɴ�'''
    if stats.ships_left > 0:
        stats.ships_left -=1
        #����������б���ӵ��б�
        aliens.empty()
        bullets.empty()
        #����һȺ�µ������˲��ŵ���Ļ�׶�����
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #��ͣ
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    '''�����û�������˵�����Ļ�ײ�'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,ship,aliens,bullets)
            break

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,
        bullets,mouse_x,mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        aliens.empty()
        bullets.empty()
        
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens) 
    
    
