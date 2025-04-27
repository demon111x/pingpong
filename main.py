import pygame as pg

from random import randint
import time

class Base_sprite(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, speed_x=0, speed_y=0):
        super().__init__()
        self.picture = pg.transform.scale(
            pg.image.load(pic).convert_alpha(), (w, h)
        )
        self.image = self.picture
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        
                
    def draw(self):
        mw.blit(self.picture, (self.rect.x, self.rect.y))


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Player_left(Base_sprite):
    def update(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_a] and self.rect.x >= 5:
        #     self.rect.x -= self.speed_x
            
        # if keys[pg.K_d] and self.rect.x <= win_w - self.rect.width:            
        #     self.rect.x += self.speed_x 
            
        if keys[pg.K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed_y 
              
        if keys[pg.K_s] and self.rect.y <= win_h - self.rect.height:            
            self.rect.y += self.speed_y


class Player_right(Base_sprite):
    def update(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_LEFT] and self.rect.x >= 5:
        #     self.rect.x -= self.speed_x
            
        # if keys[pg.K_RIGHT] and self.rect.x <= win_w - self.rect.width:            
        #     self.rect.x += self.speed_x 
            
        if keys[pg.K_UP] and self.rect.y >= 5:
            self.rect.y -= self.speed_y 
              
        if keys[pg.K_DOWN] and self.rect.y <= win_h - self.rect.height:            
            self.rect.y += self.speed_y

# class Ball(Base_sprite):
#     def update(self):
#         if self.rect.x <= 0 or self.rect.x >= win_w - self.rect.width:
#             self.speed_x *= -1

#         if self.rect.y <= 0 or self.rect.y >= win_h - self.rect.height:
#             self.speed_y *= -1

#         if self.rect.x <= win_w and self.rect.x >= 0:
#             self.rect.x += self.speed_x

#         if self.rect.y <= win_h and self.rect.y >= 0:
#             self.rect.y += self.speed_y
        
        

class Ball(Base_sprite):
    def update(self):
        global right_missed
        global left_missed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x < 0:
            ball_bouncing.play()
            self.speed_x *= -1
            self.rect.x = 0  

        if self.rect.x + self.rect.width > win_w:
            ball_bouncing.play()
            self.speed_x *= -1
            self.rect.x = win_w - self.rect.width 

        if self.rect.y < 0:
            ball_bouncing.play()
            self.speed_y *= -1
            self.rect.y = 0
        
        if self.rect.y + self.rect.height > win_h:
            ball_bouncing.play()
            self.speed_y *= -1
            self.rect.y = win_h - self.rect.height

        if self.rect.x <= 0:
            left_missed += 1
            self.rect.x = 725
            self.rect.y = 375
            self.speed_x = 7
            self.speed_y = 7

        if self.rect.x >= win_w - self.rect.width:
            right_missed += 1
            self.rect.x = 725
            self.rect.y = 375
            self.speed_x = 7
            self.speed_y = 7
            self.speed_x *= -1
            self.speed_y *= -1
            
            




pg.font.init()
font1 = pg.font.Font(None, 100)
# font2 = font.Font(None, 20)

win_w = 1500
win_h = 800
win_size = (win_w, win_h)
x, y =0, 1

# mw = pg.display.set_mode((win_w, win_h), pg.FULLSCREEN)
mw = pg.display.set_mode(win_size)
pg.display.set_caption("Ping Pong")
clock = pg.time.Clock()

pg.mixer.init()
#pg.mixer.music.play()
ball_bouncing = pg.mixer.Sound('sounds\\0427.ogg')

players = pg.sprite.Group()
balls = pg.sprite.Group()
all_sprite = pg.sprite.Group()

# fon = pg.transform.scale(
#     pg.image.load("cosmos_background.jpg"), win_size)
# fon_go = pg.transform.scale(
#     pg.image.load("cosmos_background.jpg"), win_size)


play = True
win = False
game = True
ticks = 1
left_missed = 0
right_missed = 0
BLUE = (0, 114, 255)

player_left = Player_left('images\ping_rocket1.png', win_w*0.07, (win_h-220)/2, 40, 220, 7, 7)
player_right = Player_right('images\ping_rocket2.png', win_w*0.9, (win_h-220)/2, 40, 220, 7, 7)
ball = Ball('images\\ball2.png', (win_w-50)/2, (win_h-50)/2, 50, 50, 7, 7)
all_sprite.add(player_left)
all_sprite.add(player_right)
all_sprite.add(ball)
players.add(player_left)
players.add(player_right)
balls.add(ball)

def set_text(text, x, y, color=(255,255,200)):
    mw.blit(
        font1.render(text, True, color),(x,y)
    )


while play:
    if ticks % 100 == 0:
        if ball.speed_x >= 150:
            ball.speed_x = 7
        else:
            ball.speed_x *= 1.1
            ball.speed_y *= 1.1
    for e in pg.event.get():
        if e.type == pg.QUIT or \
                    (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                play  = False

    if game:
        mw.fill(BLUE)  
        all_sprite.update()      
        all_sprite.draw(mw)      
        
        if pg.sprite.groupcollide(players, balls, False, False):
            ball_bouncing.play()
            ball.speed_x *= -1
            ball.speed_y *= -1
       
 
    
        set_text(f"{right_missed}:{left_missed}", win_w/2-50, 20)

       

    else:
        # mw.blit(fon_go, (0, 0))
        mw.fill(BLUE)

    
    pg.display.update()
    clock.tick(60)
    ticks += 1

