#coding:gbk

import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
        play_button):
    '''更新屏幕上的图像并切换到新屏幕'''
    #每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
     #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    #绘制PLAY按钮
    if not stats.game_active:
        play_button.draw_button()
    #让绘制的屏幕可见
    pygame.display.flip()
    

    
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,
        bullets):
    '''响应按键和鼠标事件'''
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
    '''更新子弹设置并删除已经消失的子弹'''
    #更新子弹的位置
    bullets.update()
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    #删除已经消失的子弹
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果还没有到达限制就发射一颗子弹'''
    #创建新子弹并将其加入到bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        
def get_number_aliens_x(ai_settings,alien_width):
    '''计算一行可以容纳多少个外星人'''
    avaiable_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(avaiable_space_x/(2*alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #创建一行外星人
     alien = Alien(ai_settings,screen)
     alien_width = alien.rect.width
     alien.x = alien_width + 2*alien_width*alien_number
     alien.rect.x = alien.x
     alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
     aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,
        alien.rect.height)
    #创建外星人
    for row_number in range(number_rows - 2):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,
                row_number)
    
def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可以容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height -
                    (3*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows
    
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    '''更新外星人中所有的外星人位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
def check_fleet_edges(ai_settings,aliens):
    '''有外星人到达屏幕边缘时采取相应措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
            
def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,ship,aliens,bullets):
    '''响应外星人撞到飞船'''
    if stats.ships_left > 0:
        stats.ships_left -=1
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人并放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    '''检查有没有外星人到达屏幕底部'''
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
    
    
