#coding:gbk
class GameStats():
    '''������Ϸ��ͳ����Ϣ'''
    
    def __init__(self,ai_settings):
        '''��ʼ��ͳ����Ϣ'''
        self.ai_settings = ai_settings
        self.reset_stats()
        #��Ϸ������ʱ����fei�״̬
        self.game_active = False
    
    def reset_stats(self):
        '''��ʼ������Ϸ����ʱ���ܱ仯��ͳ����Ϣ'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        
