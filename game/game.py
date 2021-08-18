import pygame
from game.controller import GameControl
from game.model import GameModel
from game.view import GameView
from settings import FPS
import os


class Game:
    def __init__(self,player:int) -> None:
        #print('build game')
        #print(player)
        self.game_model = GameModel(player)  # core of the game (database, game logic...)
        self.game_view = GameView(player)  # render everything
        self.keep_going = False
        self.all_pass = False
        self.player = player
        self.fail = False
        self.quit_game = False
        self.occur1 = True      #第一次動畫
        self.occur2 = False     #突發事件動畫
        self.message1 = None       #第一次的文字提示
        self.message2 = None       #突發事件文字提示
        self.message = None
        self.continue_game = None
        self.sound = None
        pass
    def run(self):
        # initialization
        pygame.init()
        game_control = GameControl(self.game_model, self.game_view)  # deal with the game flow and user request
        self.keep_going = False
        while (not self.quit_game) and (not self.keep_going) and not self.all_pass and not self.fail:
            pygame.time.Clock().tick(FPS)  # control the frame rate
            if game_control.model.enemies.count2 == game_control.model.occur_time and not game_control.model.had_occur: #產生第X隻怪物時發生突發事件
                self.occur2 = True
                self.occur1 = False
                game_control.model.had_occur = True
            # 第一次的動畫
            if self.occur1:
                game_control.model.had_occur = False
                game_control.model.pause = True             # 倒數暫停
                self.message = self.message1
                game_control.model.add_value = game_control.model.add_1
            # 突發事件發生的動畫
            if self.occur2:
                if self.sound is None:
                    if not game_control.model.mute:
                        self.sound = pygame.mixer.Sound(os.path.join("music", "warning_se.wav"))
                        self.sound.play()
                game_control.model.pause = True
                self.message = self.message2
                game_control.model.add_value = game_control.model.add_2
            
            game_control.receive_user_input()  # receive user input
            game_control.update_model()  # update the model
            game_control.model.put_message(self.message)
            if game_control.update_view():
                self.message = None
                self.occur1 = False
                self.occur2 = False
                #print(self.message)
                game_control.model.pause = False            # 倒數開始

            pygame.display.update()
            self.keep_going = game_control.keep_going
            self.fail = game_control.fail
            self.quit_game = game_control.quit_game
        if self.quit_game:
            pass
        elif self.fail:
            self.keep_going = False
        elif self.keep_going :
            self.sound = None
            self.game_model.seller.update(self.game_model)
            if self.game_model.stage == 5:
                self.all_pass = True
                self.keep_going = False
            else:
                pass
        #print(self.keep_going,self.fail,self.all_pass,self.quit_game)
        return self.quit_game
    def mute(self,mute:bool):
        self.game_model.mute = mute

