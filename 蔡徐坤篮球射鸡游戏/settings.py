#coding:gbk

class Settings():
    '''存储外星人入侵设置的所有的类'''
    
    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color=(230,230,230)
        #飞船的设置
        self.ship_speed_factor = 1
        self.ship_limit = 2
        #子弹设置
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5
        #外星人设置
        self.alien_speed_factor = 0.8
        self.fleet_drop_speed = 7
        
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
        
    def  initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #fleet_direction为1表示右移，为-1表示左移
        self.fleet_direction = 1 
        self.alien_points = 10
   

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
