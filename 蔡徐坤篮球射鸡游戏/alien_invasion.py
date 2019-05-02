#coding:gbk

import sys
import pygame

from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from  scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    #��ʼ����Ϸ�����ò�����һ����Ļ����
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
    (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #����һ��ʵ�����ڴ洢ͳ����Ϣ
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    
    #����һ�ҷɴ�
    ship = Ship(ai_settings,screen)
    #����һ�����ڴ洢�ӵ��ı����һ�������˱���
    bullets = Group()
    aliens = Group()
    #����������Ⱥ
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    #���ñ���ɫ
    bg_color = (230,230,230)
    #������ʼ��ť
    play_button = Button(ai_settings,screen,"PLAY")
    
    #��ʼ��Ϸ����ѭ��
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,
            aliens,bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,aliens)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
            play_button)
run_game()
        
    
