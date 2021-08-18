import pygame
import os

# screen size
WIN_WIDTH = 1024
WIN_HEIGHT = 600
#choose PLAYER size
CHOOSE_PLAYER_ICON_WIDTH = 100
CHOOSE_PLAYER_ICON_HEIGHT = 100
CHOOSE_PLAYER_WORD_WIDTH = 180
CHOOSE_PLAYER_WORD_HEIGHT = 45

CHOOSE_BTN_WIDTH = 800
CHOOSE_BTN_HEIGHT = 130

#heart size
HEART_WIDTH = 28
HEART_HEIGHT = 28

# frame rate
FPS = 60
# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (147, 0, 147)
BROWNGRAY = (80, 61, 50)  # wenchi append
# enemy path
PATH1_gov = [(0, 420), (31, 418), (69, 415), (108, 412), (149, 413), (187, 415), (229, 414), 
        (265, 414), (299, 414), (333, 415), (369, 416), (407, 416), (446, 416), (479, 415), 
        (509, 412), (526, 394), (545, 359), (558, 321), (568, 286), (604, 270), (649, 273), 
        (689, 278), (726, 281), (760, 284), (792, 288), (823, 288), (858, 292), (891, 296), (926, 302)]
PATH2_gov = [(398, 5), (404, 32), (409, 64), (415, 96), (420, 128), (426, 158), (430, 190), (436, 222), 
        (441, 259), (477, 264), (516, 266), (557, 268), (594, 272), (637, 276), (677, 279), (721, 283),
         (760, 287), (794, 289), (824, 293), (860, 297), (890, 299)]             # wenchi append
PATH1_wfh =[(2, 236), (28, 236), (64, 237), (107, 238), (152, 239), (190, 244), (231, 247), (243, 279),
 (235, 317), (238, 356), (261, 375), (296, 385), (336, 392), (375, 398), (419, 405), (457, 413), (488, 420), 
 (514, 427), (544, 433), (568, 421), (560, 394), (551, 364), (551, 328), (557, 297), (559, 269), (559, 247), (559, 222)]
PATH2_wfh = [(1022, 358), (1000, 357), (971, 357), (937, 360), (903, 361), (876, 361), (849, 362), (818, 362), (790, 363), (760, 363), (732, 364), (707, 358), (674, 357), (651, 355), (624, 354), (598, 349), (576, 336), (555, 319), (554, 299), (557, 280), (559, 258), (559, 240), (562, 220), (561, 203)]
PATH1 = [PATH1_gov,PATH1_wfh]
PATH2 = [PATH2_gov,PATH2_wfh]
# base
BASE = [pygame.Rect(835, 192, 150, 150),pygame.Rect(483, 73, 160, 155)]
#tower position
TOWER_POSITION_gov = [(75,319),(221,466),(302,71),(374,317),(513,175),(627,330),(737,189)]
TOWER_POSITION_wfh = [(64,143),(124,308),(279,437),(430,312),(655,410),(832,415)]
TOWER_POSITION = [TOWER_POSITION_gov,TOWER_POSITION_wfh]
# image
BACKGROUND_IMAGE =  [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "road3.png")),(WIN_WIDTH,WIN_HEIGHT)),
                        pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "road_wfh.png")),(WIN_WIDTH,WIN_HEIGHT))]
HP_GRAY_IMAGE = pygame.transform.scale(pygame.image.load("images1/game_page/heart_empty.png"), (40, 40))
HP_IMAGE = pygame.transform.scale(pygame.image.load("images1/game_page/heart_full.png"), (40, 40))
MONEY_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "money_menu.png")), (160, 45))
HEART_FULL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "heart_full.png")), (HEART_WIDTH, HEART_HEIGHT))
HEART_HALF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "heart_half.png")), (HEART_WIDTH, HEART_HEIGHT))
HEART_EMPTY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "heart_empty.png")), (HEART_WIDTH, HEART_HEIGHT))
FONT = "OtsutomeFont.ttf"     # wenchi append
NOTIFY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "notify.png")), (200, 150))
PROGRESS_LINE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "progress_line.png")), (330, 27))
ENEMY_IMAGE1 = [pygame.image.load(os.path.join("images1/game_page", "enemy_lem1.png")),pygame.image.load(os.path.join("images1/game_page", "enemy_bill1.png"))]
TOWER_MONEY_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_money_menu.png")), (160, 45))

MESSAGE_CONTINUE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "special_event_continue.png")),(190, 21))

ALL_PASS_BG = [pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "ALL_PASS_BG_4.png")),(WIN_WIDTH,WIN_HEIGHT)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "ALL_PASS_BG_3.png")),(WIN_WIDTH,WIN_HEIGHT))]
WIN_STAGE_BG = [pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "WIN_BG_4.png")),(WIN_WIDTH,WIN_HEIGHT)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "WIN_BG_3.png")),(WIN_WIDTH,WIN_HEIGHT))]
FAIL_BG = [pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "LOSE_BG_4.png")),(WIN_WIDTH,WIN_HEIGHT)),
        pygame.transform.scale(pygame.image.load(os.path.join("images1/end_page", "LOSE_BG_3.png")),(WIN_WIDTH,WIN_HEIGHT))]
ABILITY_BTN_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "special_skill.png")), (95, 95))]
PRODUCER_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "producer.png")),(WIN_WIDTH,WIN_HEIGHT))
INTRO_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images1/start_page", "Game_Intro.png")),(WIN_WIDTH,WIN_HEIGHT))
SHRINK_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images1/notify_message', "click_to_shrink.png")), (129, 11))