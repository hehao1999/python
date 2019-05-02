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
    #初始化游戏、设置并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
    (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #创建一个实例用于存储统计信息
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    
    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组和一个外星人编组
    bullets = Group()
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    #设置背景色
    bg_color = (230,230,230)
    #创建开始按钮
    play_button = Button(ai_settings,screen,"PLAY")
    
    #开始游戏的主循环
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
        
    
