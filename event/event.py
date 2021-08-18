from __future__ import annotations
from color_settings import BLUE
from event.event_gov import set_gov
from event.event_wfh import set_wfh
import random
from event.player import *
from event.event_setting import *
from game.game import Game
from pygame import mixer



dict_temp = {}
# 打开文本文件
file = open('dict.txt','r')
# 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
for line in file.readlines():
    line = line.strip()
    k = line.split(' ')[0]
    v = line.split(' ')[1]
    dict_temp[k] = v
# 依旧是关闭文件
file.close()

class Events:
    def __init__(self) :
        self.players=Players(dict_temp['gov'],dict_temp['wfh'])
        self.start_image = START_IMAGE
        self.start_round = START_ROUND
        self.using_player = 0
        self.player = 0
        self.event = None
        self.event_list = []
        
        self.num = 0
        self.buttons = [Buttons('mute',MUTE_IMAGE_BLACK,965,60),Buttons('sound',SOUND_IMAGE_BLACK,965,60),Buttons('play',PLAY_IMAGE_BLACK,920,60)
                        ,Buttons('pause',PAUSE_IMAGE_BLACK,920,60),Buttons('last_page',LAST_PAGE_IMAGE_BLACK,40,520)]
        self.buttons_white = [Buttons('mute',MUTE_IMAGE,965,60),Buttons('sound',SOUND_IMAGE,965,60),Buttons('play',PLAY_IMAGE,920,60)
                        ,Buttons('pause',PAUSE_IMAGE,920,60)]
        self.mute = False
        self.pause = False
        self.using_event=None
        #self.num=random.randint(1, 5)
        self.chosen = []
        self.chosen2 = []
        self.next=0
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.notify = None
        self.notify2 = None
        self.last_page = False
        self.read = False
        self.decision_txt = None
        self.message1 = None
        self.message2 = None
        self.dont_play = False
        pygame.mixer.init() 
        self.sound = pygame.mixer.Sound(os.path.join("music", "Choosing.wav"))
        self.win_sound = pygame.mixer.Sound(os.path.join("music", "win_se.wav"))
        self.lose_sound = pygame.mixer.Sound(os.path.join("music", "lose2.wav"))
        #self.sound = pygame.mixer.Sound(os.path.join("music", "Choosing.wav"))
        pass
    def run(self):
        clock = pygame.time.Clock()
        self.win.blit(BACKGROUND_IMAGE_CHOOSE_PLAYER,(0,0))
        run = True
        while run:
            clock.tick(FPS)
            self.win.blit(BACKGROUND_IMAGE_CHOOSE_PLAYER,(0,0))
            if self.last_page: #上一頁
                return True
            if self.using_player == 0:
                self.dont_play = False
                run = self.choose_player()
                self.read = False
                self.using_event = None
                self.num = 0
                self.next = 0
            else:
                while not self.read:
                    quit,last = self.message_page_show()
                    if quit: #press X in message_page
                        return False
                    if last:    #last page
                        self.using_player = 0
                        self.last_page = False
                        run2 = False
                        break
                    else:   #next page
                        run2 = True
                game = Game(self.using_player-1)
                
                
                while run2 :
                    run2 = self.event_happen()
                    if self.next == 1:
                        self.dont_play = False
                        if not self.mute:
                            pygame.mixer.music.unpause()
                        self.sound.stop()

                        self.impact_model(game)
                        self.using_event=None
                        game.mute(self.mute)
                        quit=game.run()
                        self.mute = game.game_model.mute
                        if quit:
                            return False
                        elif game.all_pass:
                            quit = self.all_pass(game)
                            if quit:
                                return False
                            else:
                                run2 = False
                                run = True
                        elif game.keep_going:
                            
                            quit,exit = self.keep_going(game)
                            if quit:
                                return False
                            else:
                                run2 = True
                                if exit:
                                    self.using_player = 0
                                    run2 = False
                                    run = True
                        elif game.fail:
                            quit = self.game_fail(game)
                            if quit:
                                return False
                            else:
                                run2 = False
                                run = True
                    else:
                        run = False
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    return False
            pygame.display.update()
    def choose_player(self):
        run = True
        self.draw_choose_player()
        self.draw_player_frame()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.get_click_choose_player(x,y)
                self.button_clicked(x,y)
            if event.type == pygame.QUIT:
                    run = False
        return run
    def get_click_choose_player(self,x:int,y:int):
        
        if self.start_image_rect.collidepoint(x,y) and self.player != 0:
            self.using_player = self.player
            if self.using_player == 1:
                self.event_list = [1,2,3,4,5]
            elif self.using_player == 2:
                self.event_list = [1,2,3,4,5,6]
            random.shuffle(self.event_list)
            #print(self.event_list)
        get = 0
        for player in self.players.player_btn:
            if player.buy_rect.collidepoint(x,y) and player.show_buy:
                
                if int(dict_temp['money']) - player.cost >= 0:
                    dict_temp['money'] = str( int(dict_temp['money']) - player.cost)
                    dict_temp[player.name] = str(1)
                    player.unlock = True
                    player.show_buy = False
                    #print(dict_temp)
                    file = open('dict.txt', 'w') 
                    for k,v in dict_temp.items():
                        file.write(str(k)+' '+str(v)+'\n')
                    file.close()
            if (player.icon_image_rect.collidepoint(x,y) or player.word_image_rect.collidepoint(x,y)) and player.unlock:
                player.selected = True
                self.player = player.num
                get = player.num
            elif (player.icon_image_rect.collidepoint(x,y) or player.word_image_rect.collidepoint(x,y)) and not player.unlock:
                player.show_buy = True
            else :
                player.show_buy = False
                player.selected = False
            
        if get == 0:
            self.player = 0
    def button_clicked(self,x:int,y:int):
        button_name = ''
        for btn in self.buttons:
            if btn.image_rect.collidepoint(x,y):
                button_name = btn.name
        if button_name == 'sound':
            self.mute = not self.mute
        if button_name =='pause':
            self.pause = not self.pause
        if button_name == 'last_page':
            self.last_page = True

    def draw_choose_player(self):
        self.win.blit(BACKGROUND_IMAGE_CHOOSE_PLAYER,(0,0))
        #icon of player
        for player in self.players.player_btn:
            self.win.blit(player.word_image,player.word_image_rect)
            if player.unlock:
                self.win.blit(player.icon_image, player.icon_image_rect)     #show gov
            else:
                self.win.blit(player.lock_image, player.lock_image_rect)
                show_text(self.win,'$ ' + str(player.cost),20,player.lock_image_rect.centerx-40,player.lock_image_rect.centery+5)
        for player in self.players.player_btn:
            if player.show_buy:
                self.win.blit(player.buy_message,player.buy_message_rect)
                self.win.blit(player.buy,player.buy_rect)
            
        #start button
        self.start_image_rect = self.start_image.get_rect() 
        self.start_image_rect.center = (512,500)
        self.win.blit(self.start_image,self.start_image_rect)
        #back money
        bank_image = BACK_MENU
        self.win.blit(bank_image,(20,25))
        
        show_text(self.win,'$ ' + str(dict_temp['money']),22,130,75)
        
        self.draw_button_black()
    def message_page_show(self):
        self.win.blit(BACKGROUND_IMAGE_MESSAGE[self.using_player-1],(0,0))
        self.draw_button_black()
        if self.using_player == 1:
            read_button = Buttons('read',NEXT_BUTTON,925+10,485+10)
            self.win.blit(NEXT_BUTTON,(925,485))
        elif self.using_player == 2:
            read_button = Buttons('read',NEXT_BUTTON,925+10-300,485+10)
            self.win.blit(NEXT_BUTTON,(925-300,485))

        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                return True, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.button_clicked(x, y)
                if read_button.image_rect.collidepoint(x, y):
                    self.read = True
                for btn in self.buttons:
                    if btn.image_rect.collidepoint(x, y):
                        button_name = btn.name
                        if button_name == 'last_page':
                            return False, True
        pygame.display.update()
        return False,False
    def draw_player_frame(self):
        for btn in self.players.player_btn:
            if btn.selected :
                pygame.draw.rect(self.win, (150, 150, 150), btn.frame, 10)
    def event_happen(self):
        
        run2 = True
        if self.using_event == None:
            self.set_using_event()
            if self.mute:
                pass
            else:
                self.dont_play = True
                pygame.mixer.music.pause()
                self.sound.play(loops=10)
                self.sound.set_volume(0.5)
        self.events_draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.make_decision(x,y)
                self.button_clicked(x,y)
            if event.type == pygame.QUIT:
                    run2 = False
        return run2
    def events_draw(self):
        self.win.blit(BACKGROUND_IMAGE_EVENT[self.using_player-1],(0,0)) #色碼,X點、Y點、寬、高
        self.win.blit(self.using_event.question.image, self.using_event.question.image_rect)     #show choose player
        
        self.start_round_rect = self.start_round.get_rect()
        self.start_round_rect.center = (365,520)
        x, y = pygame.mouse.get_pos()

        if self.using_event.select1.image_rect.collidepoint(x,y):
            self.win.blit(self.using_event.select1.hint_back,self.using_event.select1.hint_back_rect)
            self.win.blit(self.using_event.select1.hint,self.using_event.select1.hint_rect)
            self.using_event.select2.hint_back_rect.centerx = 165+250
            self.using_event.select3.hint_back_rect.centerx = 165+250
            self.using_event.select2.hint_rect.left = 165+250+20-150
            self.using_event.select3.hint_rect.left = 165+250+20-150
            self.using_event.select2.move_count = 0
            self.using_event.select3.move_count = 0
            if self.using_event.select1.move_count < self.using_event.select1.move_max:
                self.using_event.select1.hint_back_rect.centerx += 20
                self.using_event.select1.hint_rect.centerx += 20
                self.using_event.select1.move_count += 1
  
        if self.using_event.select2.image_rect.collidepoint(x,y):
            self.win.blit(self.using_event.select2.hint_back,self.using_event.select2.hint_back_rect)
            self.win.blit(self.using_event.select2.hint,self.using_event.select2.hint_rect)
            self.using_event.select1.hint_back_rect.centerx = 165+250
            self.using_event.select3.hint_back_rect.centerx = 165+250
            self.using_event.select1.hint_rect.left = 165+250+20-150
            self.using_event.select3.hint_rect.left = 165+250+20-150
            self.using_event.select1.move_count = 0
            self.using_event.select3.move_count = 0
            if self.using_event.select2.move_count < self.using_event.select2.move_max:
                self.using_event.select2.hint_back_rect.centerx += 20
                self.using_event.select2.hint_rect.centerx += 20
                self.using_event.select2.move_count += 1

     
        if self.using_event.select3.image_rect.collidepoint(x,y):
            self.win.blit(self.using_event.select3.hint_back,self.using_event.select3.hint_back_rect)
            self.win.blit(self.using_event.select3.hint,self.using_event.select3.hint_rect)
            self.using_event.select2.hint_back_rect.centerx = 165+250
            self.using_event.select1.hint_back_rect.centerx = 165+250
            self.using_event.select2.hint_rect.left = 165+250+20-150
            self.using_event.select1.hint_rect.left = 165+250+20-150
            self.using_event.select2.move_count = 0
            self.using_event.select1.move_count = 0
            if self.using_event.select3.move_count < self.using_event.select3.move_max:
                self.using_event.select3.hint_back_rect.centerx += 20
                self.using_event.select3.hint_rect.centerx += 20
                self.using_event.select3.move_count += 1

        self.win.blit(self.using_event.select1.image, self.using_event.select1.image_rect)     #show gov
        self.win.blit(self.using_event.select2.image, self.using_event.select2.image_rect)     #show wfh
        self.win.blit(self.using_event.select3.image, self.using_event.select3.image_rect)     #show wfh
        
        
        self.win.blit(self.start_round,self.start_round_rect)
        self.draw_event_frame()
        level_image_rect = LEVEL1.get_rect()
        level_image_rect.center= (105,50)
        if self.num == 1:
            level_image = LEVEL1
        elif self.num == 2:
            level_image = LEVEL2
        elif self.num == 3:
            level_image = LEVEL3
        elif self.num == 4:
            level_image = LEVEL4
        elif self.num == 5:
            level_image = LEVEL5
        self.win.blit(level_image,level_image_rect)
        self.draw_button_white()
        pygame.display.update()
        pass
    def draw_event_frame(self):
        
        if self.using_event.select1.selected:
            pygame.draw.rect(self.win, BLACK, self.using_event.select1.frame, 6)
        if self.using_event.select2.selected:
            pygame.draw.rect(self.win, BLACK, self.using_event.select2.frame, 6)
        if self.using_event.select3.selected:
            pygame.draw.rect(self.win, BLACK, self.using_event.select3.frame, 6)
    def set_using_event(self):
        
        self.using_event=get_using_event(self.using_player,self.event_list[self.num])
        #
        self.chosen = []
        self.num += 1
    def make_decision(self,x:int,y:int):
        if self.start_round_rect.collidepoint(x,y) and self.chosen != []:
            self.next=1
            self.using_event.select1.selected = False
            self.using_event.select2.selected = False
            self.using_event.select3.selected = False
            return
        if self.using_event.select1.image_rect.collidepoint(x,y):
            self.using_event.select1.selected = True
            self.using_event.select2.selected = False
            self.using_event.select3.selected = False
            self.notify = self.using_event.select1.notify
            self.chosen = self.using_event.select1.impact
            self.notify2 = self.using_event.select1.notify2
            self.chosen2 = self.using_event.select1.impact2
            self.text = self.using_event.select1.text
            self.message1 = self.using_event.select1.message1
            self.message2 = self.using_event.select1.message2
        elif self.using_event.select2.image_rect.collidepoint(x,y):
            self.using_event.select1.selected = False
            self.using_event.select2.selected = True
            self.using_event.select3.selected = False
            self.notify = self.using_event.select2.notify
            self.chosen = self.using_event.select2.impact
            self.notify2 = self.using_event.select2.notify2
            self.chosen2 = self.using_event.select2.impact2
            self.decision_txt = self.using_event.select2.image
            self.text = self.using_event.select1.text
            self.message1 = self.using_event.select2.message1
            self.message2 = self.using_event.select2.message2
        elif self.using_event.select3.image_rect.collidepoint(x,y):
            self.using_event.select1.selected = False
            self.using_event.select2.selected = False
            self.using_event.select3.selected = True
            self.chosen = self.using_event.select3.impact
            self.notify = self.using_event.select3.notify
            self.chosen2 = self.using_event.select3.impact2
            self.notify2 = self.using_event.select3.notify2
            self.decision_txt = self.using_event.select3.image
            self.text = self.using_event.select1.text
            self.message1 = self.using_event.select3.message1
            self.message2 = self.using_event.select3.message2
        else:
            self.using_event.select1.selected = False
            self.using_event.select2.selected = False
            self.using_event.select3.selected = False
            self.chosen = []
    def draw_button_black(self):
        self.win.blit(self.buttons[4].image,self.buttons[4].image_rect)
        if self.mute:
            self.win.blit(self.buttons[0].image,self.buttons[0].image_rect)
            pygame.mixer.music.pause()
            self.sound.stop()
        else:
            if not self.dont_play:
                self.win.blit(self.buttons[1].image,self.buttons[1].image_rect)
                pygame.mixer.music.unpause()
    def draw_button_white(self):
        if self.mute:
            self.win.blit(self.buttons_white[0].image,self.buttons_white[0].image_rect)
            pygame.mixer.music.pause()
            self.sound.stop()
        else:
            self.win.blit(self.buttons_white[1].image,self.buttons_white[1].image_rect)
            if not self.dont_play:
                pygame.mixer.music.unpause()

    def impact_model(self,game:Game):
        game.player = self.using_player-1
        money_get = 0
        blood_get = 0
        tower_upgrade = 0
        money_get2 = 0
        blood_get2 = 0
        tower_upgrade2 = 0
        if self.chosen[1]!=self.chosen[0]:
            money_get = random.randint(self.chosen[1],self.chosen[0])
        if self.chosen[3]!=self.chosen[2]:
            blood_get = random.randint(self.chosen[3],self.chosen[2])
        if self.chosen[5]!=self.chosen[4]:
            tower_upgrade = random.randint(self.chosen[5],self.chosen[4])
        if self.chosen2[1]!=self.chosen2[0]:
            money_get2 = random.randint(self.chosen2[1],self.chosen2[0])
        if self.chosen2[3]!=self.chosen2[2]:
            blood_get2 = random.randint(self.chosen2[3],self.chosen2[2])
        if self.chosen2[5]!=self.chosen2[4]:
            tower_upgrade2 = random.randint(self.chosen2[5],self.chosen2[4])

        game.game_model.money += 20
        game.game_model.tower_money += 10

       	game.game_model.add_1[0] = blood_get
        game.game_model.add_1[1] = tower_upgrade
        game.game_model.add_1[2] = money_get
        game.game_model.add_2[0] = blood_get2
        game.game_model.add_2[1] = tower_upgrade2
        game.game_model.add_2[2] = money_get2

        #print(game.game_model.add_1)
        #print(game.game_model.add_2)


        game.game_model.notify = self.notify
        game.game_model.notify2 = self.notify2
        game.message1 = self.message1
        game.message2 = self.message2
        game.game_model.occur_time = random.randint(5,9)
        game.occur1 = True
        game.occur2 = False
        
    def keep_going(self,game:Game):
        
        if self.mute:
            pass
        else:
            self.dont_play = True
            pygame.mixer.music.pause()
            self.win_sound.play()
        self.next = 0
        self.chosen = []
        percentage = [0,10,20,40,60,100]
        while True:
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 10
            pygame.draw.rect(surface, (150, 150, 150, transparency), (0,0,WIN_WIDTH, WIN_HEIGHT))
            self.win.blit(surface, (0, 0))
            self.win.blit(WIN_STAGE_BG[self.using_player-1],(0,0))
            text = '* ' + str(game.game_model.tower_money) #塔防幣
            show_text(self.win,text,23,616,473)
            text = '# ' + str(game.game_model.money) #金錢
            show_text(self.win,text,23,767,473)
            text = str(int(game.game_model.money * percentage[game.game_model.stage] / 100))
            show_text(self.win,text,50,510,332) #中間遊戲幣
            text = str( percentage[game.game_model.stage])+'%'
            show_text(self.win,text,30,248,95,(99, 78, 66))#左上目前%數
            text = str( percentage[game.game_model.stage+1])+'%'
            show_text(self.win,text,30,574,400,(64, 155, 163))#下一關%數
            draw_hp(self.win, game.game_model.hp,game.game_model.max_hp)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 86<x<86+186 and 379<y<379+55:
                        
                        dict_temp['money'] = str(int(dict_temp['money'])+int(game.game_model.money * percentage[game.game_model.stage]/100))
                        file = open('dict.txt', 'w') 
                        for k,v in dict_temp.items():
	                        file.write(str(k)+' '+str(v)+'\n')
                        file.close()
                        return False,True
                    elif 750<x<750+186 and 379<y<379+55:
                        return False,False
                if event.type == pygame.QUIT:
                    return True,True
    def all_pass(self,game:Game):
        
        if self.mute:
            pass
        else:
            self.dont_play = True
            pygame.mixer.music.pause()
            self.win_sound.play()
        while True:
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 10
            pygame.draw.rect(surface, (122, 122, 122, transparency), (0,0,WIN_WIDTH, WIN_HEIGHT))
            self.win.blit(surface, (0, 0))
            self.win.blit(ALL_PASS_BG[self.using_player-1],(0,0))
            text = '* ' + str(game.game_model.tower_money)#塔防幣
            show_text(self.win,text,23,610,473)
            text = '# ' + str(game.game_model.money)#金錢
            show_text(self.win,text,23,767,473)
            text = str(int(game.game_model.money))#中間遊戲幣
            show_text(self.win,text,50,510,337)
            draw_hp(self.win, game.game_model.hp,game.game_model.max_hp)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 750<x<750+186 and 364<y<364+55:
                        dict_temp['money'] = str(int(dict_temp['money'])+int(game.game_model.money))
                        file = open('dict.txt', 'w') 
                        for k,v in dict_temp.items():
	                        file.write(str(k)+' '+str(v)+'\n')
                        file.close()
                        self.using_player=0
                        return False              
    def game_fail(self,game:Game):
        if self.mute:
            pass
        else:
            self.dont_play = True
            pygame.mixer.music.pause()
            self.lose_sound.play()
        
        percentage = [0,10,20,40,60,100]
        while True:
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 10
            pygame.draw.rect(surface, (122, 122, 122, transparency), (0,0,WIN_WIDTH, WIN_HEIGHT))
            self.win.blit(surface, (0, 0))

            self.win.blit(FAIL_BG[self.using_player-1],(0,0))
            text = '* ' + str(game.game_model.tower_money)#塔防幣
            show_text(self.win,text,23,610,473)
            text = '# ' + str(game.game_model.money) #金錢
            show_text(self.win,text,23,767,473)
            text = str(int(game.game_model.money * percentage[game.game_model.stage-1] / 100))
            show_text(self.win,text,50,510,345)#中間遊戲幣
            #fail_sound = pygame.mixer.Sound('music','lose_se') #音樂
            #fail_sound.play()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 750<x<750+186 and 379<y<379+55:
                        dict_temp['money'] = str(int(dict_temp['money'])+int(game.game_model.money * percentage[game.game_model.stage-1]/100))
                        file = open('dict.txt', 'w') 
                        for k,v in dict_temp.items():
	                        file.write(str(k)+' '+str(v)+'\n')
                        file.close()
                        self.using_player=0
                        return False
                if event.type == pygame.QUIT:
                    self.using_player=0
                    return True
def get_using_event(player:int,num:int):
    if player == 1:
        return set_gov(num)
    if player == 2:
        return set_wfh(num)
    pass
def show_text(win:pygame.Surface,text:str,size:int,x:int,y:int,color:tuple = BROWNGRAY):
    font = pygame.font.Font(FONT, size)
    text = font.render(text, True, color)
    
    win.blit(text, (x, y))
def draw_hp(win:pygame.Surface, hp:int,max_hp:int):
    # draw_lives
 
    hp_image_rect = HEART_FULL_IMAGE.get_rect()
    for i in range(1, 16, 2):
        hp_image_rect.center = (200 + ((i - 1) / 2) * (HEART_WIDTH + 13), 480 + (HEART_HEIGHT / 2))
        if i < hp:
            win.blit(HEART_FULL_IMAGE, hp_image_rect)
        elif i == hp:
            if hp == 0:
                win.blit(HEART_EMPTY_IMAGE, hp_image_rect)
            else:
                win.blit(HEART_HALF_IMAGE, hp_image_rect)
        else:
            win.blit(HEART_EMPTY_IMAGE, hp_image_rect)

