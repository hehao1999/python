#coding:gbk

class Settings():
    '''�洢�������������õ����е���'''
    
    def __init__(self):
        '''��ʼ����Ϸ������'''
        #��Ļ����
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color=(230,230,230)
        #�ɴ�������
        self.ship_speed_factor = 1
        self.ship_limit = 2
        #�ӵ�����
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5
        #����������
        self.alien_speed_factor = 0.8
        self.fleet_drop_speed = 7
        
        #��ʲô�����ٶȼӿ���Ϸ����
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
        
    def  initialize_dynamic_settings(self):
        '''��ʼ������Ϸ���ж��仯������'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #fleet_directionΪ1��ʾ���ƣ�Ϊ-1��ʾ����
        self.fleet_direction = 1 
        self.alien_points = 10
   

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
