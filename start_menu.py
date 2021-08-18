
import pygame
import os

from color_settings import *
from settings import *
from event.event import Events
pygame.init()
pygame.mixer.init()
START_BTN = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "btn_start.png")), (180, 65))
BTN_INTRO = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "btn_intro.png")), (160, 45))
BTN_PRODUCER = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "btn_producer.png")), (160, 45))


class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # background
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "welcome.png")), (WIN_WIDTH, WIN_HEIGHT))
        # button
        self.start_btn = Buttons(START_BTN,410, 280, 180, 65)  # x, y, width, height
        self.introduce_btn = Buttons(BTN_INTRO,425, 390, 160, 45)
        self.producer_btn = Buttons(BTN_PRODUCER,425,460,160, 45)
        #self.sound_btn = Buttons(725, 525, 90, 70)
        #self.mute_btn = Buttons(830, 525, 90, 70)
        self.buttons = [self.introduce_btn,
                        self.producer_btn,
                        self.start_btn]
        self.last_page_btn = Events().buttons[4]
        self.last_page_btn2 = Events().buttons[4].image
        self.last_page_btn2_rect = self.last_page_btn2.get_rect()
        self.last_page_btn2_rect.center = (50,540)
        # music and sound
        self.sound = pygame.mixer.Sound("./music/bg_music.wav")
        # page
        self.last_page = False
        self.producer_page = False

    def play_music(self):
        pygame.mixer.music.load("./music/bg_music.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.sound.set_volume(0.2)

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("疫起大作戰")
        self.play_music()
        while run:
            clock.tick(FPS)
            self.menu_win.blit(self.bg, (0, 0))
            
            x, y = pygame.mouse.get_pos()
            # while cursor is moving (not click)
            """(Q1.2) create button frame and draw"""
            # (hint) use a for loop to go through all the buttons, create the frame, and draw it.
            for btn in self.buttons:
                self.menu_win.blit(btn.image,btn.rect)
                btn.create_frame(x,y)
                btn.draw_frame(self.menu_win)

            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn
                    if self.start_btn.clicked(x, y):
                        events = Events()
                        run = events.run()
                    elif self.producer_btn.clicked(x, y):
                        run2 = True
                        while run2:
                            self.menu_win.blit(PRODUCER_BACKGROUND, (0, 0))
                            self.menu_win.blit(self.last_page_btn.image, self.last_page_btn.image_rect)
                            quit, last = self.producer_page_show()
                            if quit:
                                return False
                            if last:  # last page
                                run2 = False
                            else:  # producer page
                                run2 = True
                    elif self.introduce_btn.clicked(x, y):
                        run2 = True
                        while run2:
                            self.menu_win.blit(INTRO_BACKGROUND, (0, 0))
                            
                            self.menu_win.blit(self.last_page_btn2,self.last_page_btn2_rect)
                            quit, last = self.intro_page_show()
                            if quit:
                                return False
                            if last:  # last page
                                run2 = False
                            else:  # producer page
                                run2 = True
                        pygame.display.update()
                        
                    """(Q1.1) music on/off according to the button"""
                    # (hint) pygame.mixer.music.pause/unpause
                    #if self.mute_btn.clicked(x,y):
                    #    pygame.mixer.music.pause()
                    #if self.sound_btn.clicked(x,y):
                    #    pygame.mixer.music.unpause()

            pygame.display.update()
        pygame.quit()

    def producer_page_show(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.last_page_btn.image_rect.collidepoint(x, y):
                    return False, True
            if event.type == pygame.QUIT:
                return True, False
        pygame.display.update()
        return False, False
    def intro_page_show(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.last_page_btn2_rect.collidepoint(x, y):
                    return False, True
            if event.type == pygame.QUIT:
                return True, False
        pygame.display.update()
        return False, False

class Buttons:
    def __init__(self,image:pygame.Surface, x:int, y:int, width:int, height:int):
        self.rect = pygame.Rect(x, y, width, height)
        self.frame = None
        self.image = image
    def clicked(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        return False

    def create_frame(self, x: int, y: int):
        """if cursor position is on the button, create button frame"""
        if self.clicked(x, y):
            x, y, w, h = self.rect
            self.frame = pygame.Rect(x - 5, y - 5, w + 10, h + 10)
        else:
            self.frame = None

    def draw_frame(self, win:pygame.Surface):
        if self.frame is not None:
            pygame.draw.rect(win, BLACK, self.frame, 10)
