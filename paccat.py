# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 18:20:01 2021

@author: njani
"""
import pygame as pg
import random as r
import sys
from math import floor

pg.init()
pg.font.init()
pg.mixer.init()

clock = pg.time.Clock()

# FONTS

FONT = pg.font.Font("assets/8-BIT WONDER.ttf", 27)
TITLE_FONT = pg.font.Font("assets/8-BIT WONDER.ttf", 54)
FONT2 = pg.font.Font("assets/m5x7.ttf", 36)

# MUSIC
pg.mixer.music.load("assets/music.mp3")
pg.mixer.music.set_volume(0.1)

# farby
BLACK = (0, 3, 0)
WHITE = (255, 254, 255)
ORANGE_YELLOW = (245, 187, 0)

sprites = pg.sprite.Group()

# screen
WIDTH = 720
HEIGHT = 600
fps = 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PAC-CAT')

icon = pg.image.load('assets/cat_logo.png')
pg.display.set_icon(icon)

gameOver_img = pg.image.load('assets/gameover.png')

player_name = ''

# PLAYER

life_img = pg.image.load('assets/corazon.png')

walk_right = [pg.transform.scale(pg.image.load('assets/cat_walk1.png'), (35, 35)),
              pg.transform.scale(pg.image.load('assets/cat_walk2.png'), (35, 35))]
walk_left = [pg.transform.scale(pg.image.load('assets/cat_walk1l.png'), (35, 35)),
             pg.transform.scale(pg.image.load('assets/cat_walk2l.png'), (35, 35))]
walk_up = [pg.transform.scale(pg.image.load('assets/walk_up1.png'), (35, 35)),
           pg.transform.scale(pg.image.load('assets/walk_up2.png'), (35, 35))]
walk_down = [pg.transform.scale(pg.image.load('assets/walk_down1.png'), (35, 35)),
             pg.transform.scale(pg.image.load('assets/walk_down2.png'), (35, 35))]
idle = [pg.transform.scale(pg.image.load('assets/cat_idler.png'), (35, 35)),
        pg.transform.scale(pg.image.load('assets/cat_idlel.png'), (35, 35))]


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = idle[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35
        self.speed = 4
        self.score = 0
        self.lives = 3
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.idle = True
        self.facing_right = True
        self.walk_count = 0
        self.shots = 0

    def collision_check(self, sprites):
        if pg.sprite.spritecollideany(self, sprites):
            return True


player = Player(340, 240)
sprites.add(player)

# MAP
map_list = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1,
             1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1,
             1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1,
             1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1,
             1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
             1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# map_list = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
#             1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
#             1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,
#             1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,
#             1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,
#             1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,0,1,
#             1,1,1,1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,
#             1,0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0,1,
#             1,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,1,
#             1,0,1,1,0,1,1,0,0,0,0,1,1,0,1,1,0,1,
#             1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,
#             1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,
#             1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
#             1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

map_w = 18
map_h = 14
tile = pg.image.load('assets/tiles.png')

wall_list = []

walls = pg.sprite.Group()


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('assets/tiles.png')
        self.width = 40
        self.height = 40
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


def setupwalls():
    global wall_list, walls
    for a in wall_list:
        wall = Wall(a[0], a[1])
        walls.add(wall)

    return walls


walls = setupwalls()

# COINS

coins = pg.sprite.Group()

free_list = []


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('assets/coin.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

    def collision(self, player):
        if self.rect.colliderect(player):
            player.score += 1
            player.shots += 5
            self.kill()


def create_coins():
    amount = r.randint(3, 8)
    for i in range(amount):
        xy = free_list[r.randint(0, len(free_list) - 1)]
        coin = Coin(xy[0] + 12, xy[1] + 12)
        coins.add(coin)
    return coins


# MONSTA
monsters = pg.sprite.Group()

mon_right = [pg.transform.scale(pg.image.load('assets/mon1r.png'), (30, 30))]


class Monster(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = mon_right[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        self.count = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.facing_right = True
        # self.walk_count = 0
        self.prevxy = [(self.x, self.y), self.x, self.y]

    def collision_player(self, player):
        if self.rect.colliderect(player):
            player.lives -= 1
            player.x, player.y = 340, 240
            player.rect.topleft = (player.x, player.y)

    def collision_shot(self, shots):
        if pg.sprite.spritecollideany(self, shots):
            player.score += 5
            self.kill()
            for s in shots:
                s.kill()

    def collision_wall(self, walls):
        if pg.sprite.spritecollideany(self, walls):
            return True

    def move(self, player, walls, free_list):
        if not self.collision_wall(walls):
            new_x, new_y = self.x + 40 - 5, self.y + 40 - 5
            new_x1, new_y1 = self.x - 40 - 5, self.y - 40 - 5
            possible_move = [(self.x - 5, new_y1), (self.x - 5, new_y),
                             (new_x, self.y - 5), (new_x1, self.y - 5)]
            r.shuffle(possible_move)
            for m in possible_move:
                if m in free_list and m != self.prevxy[0]:
                    self.prevxy = [(self.x, self.y), self.x, self.y]
                    self.x, self.y = m[0] + 5, m[1] + 5
                    self.rect.topleft = (self.x, self.y)
                    break
        else:
            self.dir = 0
            self.rect.topleft, self.x, self.y = self.prevxy[0], self.prevxy[1], self.prevxy[2]


def create_monsters():
    n = r.randint(4, 10)
    for i in range(n):
        xy = free_list[r.randint(0, len(free_list) - 1)]
        mon = Monster(xy[0] + 5, xy[1] + 5)
        monsters.add(mon)
    return monsters


# SHOT
shots = pg.sprite.Group()

shot_r = pg.transform.scale(pg.image.load('assets/shotr.png'), (20, 20))
shot_l = pg.transform.scale(pg.image.load('assets/shotl.png'), (20, 20))
shot_u = pg.transform.scale(pg.image.load('assets/shotu.png'), (20, 20))
shot_d = pg.transform.scale(pg.image.load('assets/shotd.png'), (20, 20))


class Shot(pg.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pg.sprite.Sprite.__init__(self)
        self.image = shot_r
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.orientation = orientation
        self.speed = 7

    def change_img(self):
        if self.orientation == 'left':
            self.image = shot_l
        elif self.orientation == 'up':
            self.image = shot_u
        elif self.orientation == 'down':
            self.image = shot_d

    def collision_wall(self, walls):
        if pg.sprite.spritecollideany(self, walls):
            self.kill()

    def move(self, walls):
        self.collision_wall(walls)
        if self.orientation == 'left':
            self.x -= self.speed
            self.rect.center = (self.x, self.y)
        elif self.orientation == 'right':
            self.x += self.speed
            self.rect.center = (self.x, self.y)
        elif self.orientation == 'up':
            self.y -= self.speed
            self.rect.center = (self.x, self.y)
        elif self.orientation == 'down':
            self.y += self.speed
            self.rect.center = (self.x, self.y)


gameOver = False

click = False


def main():
    pg.mixer.music.play(-1)
    menu()


# MAIN MENU

def menu_text():
    text_menu = TITLE_FONT.render("PAC CAT", 1, WHITE)
    text_start = FONT.render("Start", 1, WHITE)
    text_how = FONT.render("How to play", 1, WHITE)
    text_score = FONT.render("Leaderboard", 1, WHITE)
    text_settings = FONT.render("Settings", 1, WHITE)
    text_leave = FONT.render('Exit', 1, WHITE)

    screen.blit(text_menu, (WIDTH / 2 - 170, 100))
    screen.blit(text_start, (WIDTH / 2 - 67.5, 250))
    screen.blit(text_how, (WIDTH / 2 - 148.5, 320))
    screen.blit(text_score, (WIDTH / 2 - 155, 390))
    screen.blit(text_leave, (WIDTH / 2 - 50, 530))
    screen.blit(text_settings, (WIDTH / 2 - 110, 460))


def menu():
    global clock, click, running, gameOver, player, sprites
    while True:
        screen.fill(BLACK)

        cat_logo = pg.transform.scale(icon, (100, 100))

        screen.blit(cat_logo, (WIDTH / 2 - 50, 100))

        menu_text()

        mx, my = pg.mouse.get_pos()

        btn1 = pg.Rect(WIDTH / 2 - 110, 238.5, 200, 50)
        btn2 = pg.Rect(WIDTH / 2 - 170, 308.5, 320, 50)
        btn3 = pg.Rect(WIDTH / 2 - 175, 378.5, 330, 50)
        btn4 = pg.Rect(WIDTH / 2 - 137, 448.5, 250, 50)
        btn_end = pg.Rect(WIDTH / 2 - 110, 518.5, 200, 50)

        if btn1.collidepoint((mx, my)):
            if click:
                enter_name()
                main_game()
                if gameOver:
                    player = Player(340, 240)
                    sprites.add(player)
                    gameOver = False
        if btn2.collidepoint((mx, my)):
            if click:
                how_to()
        if btn3.collidepoint((mx, my)):
            if click:
                leaderboard()
        if btn4.collidepoint((mx, my)):
            if click:
                settings()
        if btn_end.collidepoint((mx, my)):
            if click:
                running = False
                pg.quit()
                sys.exit()

        pg.draw.rect(screen, WHITE, btn1, 4)
        pg.draw.rect(screen, WHITE, btn2, 4)
        pg.draw.rect(screen, WHITE, btn3, 4)
        pg.draw.rect(screen, WHITE, btn_end, 4)
        pg.draw.rect(screen, WHITE, btn4, 4)

        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pg.display.update()
        clock.tick(fps)


# HOW TO PLAY

def how_to():
    running = True
    btn_back = pg.Rect(WIDTH / 2 - 110, HEIGHT - 100, 220, 50)
    text_back = FONT2.render('Back', 1, WHITE)
    click = False
    while running:
        screen.fill(BLACK)
        clock.tick(fps)

        coin_img = pg.image.load('assets/coin.png')

        title = TITLE_FONT.render("How to play", 1, WHITE)
        move = FONT2.render("Movement: W,A,S,D", 1, WHITE)
        shoot = FONT2.render("Shooting: SPACEBAR", 1, WHITE)
        shoot2 = FONT2.render('To be able to shoot you need to collect coins', 1, WHITE)
        back = FONT2.render("Back to main menu: ESC", 1, WHITE)

        screen.blit(title, (WIDTH / 2 - 300, 50))
        screen.blit(move, (40, 150))
        screen.blit(shoot, (40, 200))
        screen.blit(back, (40, 250))
        screen.blit(shoot2, (40, 300))
        screen.blit(coin_img, (600, 309))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pg.mouse.get_pos()

        if btn_back.collidepoint((mx, my)):
            if click:
                running = False

        click = False

        pg.draw.rect(screen, WHITE, btn_back, 4)
        screen.blit(text_back, (WIDTH / 2 - 25, HEIGHT - 91))
        pg.display.update()


# LEADERBOARD
def leaderboard():
    running = True
    click = False
    btn_back = pg.Rect(WIDTH / 2 - 110, HEIGHT - 100, 220, 50)
    text_back = FONT2.render('Back', 1, WHITE)
    cat_fight = pg.transform.scale(pg.image.load('assets/cat_fight.png'), (100, 100))
    mon_scared = pg.transform.scale(pg.image.load('assets/mon_scared.png'), (100, 100))
    while running:
        screen.fill(BLACK)
        clock.tick(fps)

        title = TITLE_FONT.render("LEADERBOARD", 1, WHITE)

        screen.blit(title, (WIDTH / 2 - 297, 40))

        with open('leaderboard.txt', 'r') as f:
            for i, line in enumerate(f):
                if i == 10:
                    break
                score = FONT2.render(str(i + 1) + '. ' + line.strip(), 1, WHITE)
                screen.blit(score, (50, 130 + i * 36))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pg.mouse.get_pos()

        if btn_back.collidepoint((mx, my)):
            if click:
                running = False

        click = False

        pg.draw.rect(screen, WHITE, btn_back, 4)
        screen.blit(text_back, (WIDTH / 2 - 25, HEIGHT - 91))
        screen.blit(mon_scared, (WIDTH - 300, HEIGHT / 2 + 5))
        screen.blit(cat_fight, (WIDTH - 200, HEIGHT / 2))
        pg.display.update()


# SETTINGS


def creds():
    text_code = FONT2.render("Programming: Nikola Janickova", 1, WHITE)
    text_art = FONT2.render("Art: dogchicken, Nikola Janickova, Mapachana", 1, WHITE)
    text_music = FONT2.render("Music: Enemy Attacks By HeatleyBros", 1, WHITE)
    text_cred = FONT.render("CREDITS", 1, WHITE)

    screen.blit(text_cred, (50, 300))
    screen.blit(text_code, (50, 350))
    screen.blit(text_art, (50, 400))
    screen.blit(text_music, (50, 450))


def settings():
    running = True
    btn_back = pg.Rect(WIDTH / 2 - 110, HEIGHT - 100, 220, 50)
    text_back = FONT2.render('Back', 1, WHITE)
    click = False
    btn_imgr = pg.image.load('assets/triangle.png')
    btn_imgl = pg.image.load('assets/triangle_l.png')
    btn_up = btn_imgr.get_rect()
    btn_down = btn_imgl.get_rect()
    btn_up.topleft = (WIDTH / 2 + 50, 150)
    btn_down.topleft = (WIDTH / 2 - 50, 150)
    while running:
        screen.fill(BLACK)
        clock.tick(fps)

        title = TITLE_FONT.render("SETTINGS", 1, WHITE)
        volume = FONT2.render("Background music:", 1, WHITE)
        volume_num = FONT2.render(str(round(pg.mixer.music.get_volume(), 1)), 1, WHITE)

        screen.blit(title, (WIDTH / 2 - 312, 50))
        screen.blit(volume, (50, 150))
        screen.blit(volume_num, (WIDTH / 2, 150))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pg.mouse.get_pos()

        if btn_back.collidepoint((mx, my)):
            if click:
                running = False
        if btn_up.collidepoint((mx, my)):
            if click:
                vol = pg.mixer.music.get_volume()
                pg.mixer.music.set_volume(vol + 0.1)
        if btn_down.collidepoint((mx, my)):
            if click:
                vol = pg.mixer.music.get_volume()
                pg.mixer.music.set_volume(vol - 0.1)

        click = False

        pg.draw.rect(screen, WHITE, btn_back, 4)
        pg.draw.rect(screen, BLACK, btn_up)
        pg.draw.rect(screen, BLACK, btn_down)
        screen.blit(text_back, (WIDTH / 2 - 25, HEIGHT - 91))
        screen.blit(btn_imgl, (WIDTH / 2 - 50, 150))
        screen.blit(btn_imgr, (WIDTH / 2 + 50, 150))
        creds()
        pg.display.update()


# GAME

def main_game():
    global clock, gameOver, player
    running = True
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        change_state('idle')
        if gameOver:
            running = False
            game_over()
        inputs()
        logic()
        graphics()


prevxy = [(player.x, player.y), player.x, player.y]

orient = 'right'


def inputs():
    global WIDTH, HEIGHT, walls, prevxy, orient
    keys = pg.key.get_pressed()
    if not player.collision_check(walls):
        if keys[pg.K_a] and player.x > player.width:
            prevxy = [(player.x, player.y), player.x, player.y]
            player.x -= player.speed
            change_state('left')
            orient = 'left'
            player.rect.topleft = (player.x, player.y)
        elif keys[pg.K_d] and player.x < WIDTH - (2 * player.width):
            prevxy = [(player.x, player.y), player.x, player.y]
            player.x += player.speed
            change_state('right')
            orient = 'right'
            player.rect.topleft = (player.x, player.y)
        elif keys[pg.K_w] and player.y > player.height:
            prevxy = [(player.x, player.y), player.x, player.y]
            player.y -= player.speed
            change_state('up')
            orient = 'up'
            player.rect.topleft = (player.x, player.y)
        elif keys[pg.K_s] and player.y < HEIGHT - (3 * player.width):
            prevxy = [(player.x, player.y), player.x, player.y]
            player.y += player.speed
            change_state('down')
            orient = 'down'
            player.rect.topleft = (player.x, player.y)
    else:
        player.rect.topleft = prevxy[0]
        player.x = prevxy[1]
        player.y = prevxy[2]

    if keys[pg.K_SPACE] and player.shots > 0:
        shot = Shot((floor(player.x / 10) * 10) + 15, (floor(player.y / 10) * 10) + 15, orient)
        shot.change_img()
        shots.add(shot)
        player.shots -= 1


def logic():
    global player, walls, free_list, gameOver, shots, coins, monsters
    for coin in coins:
        coin.collision(player)
    for mon in monsters:
        if mon.count == 30:
            mon.move(player, walls, free_list)
            mon.count = 0
        mon.collision_player(player)
        mon.collision_shot(shots)
        mon.count += 1
    for s in shots:
        s.move(walls)
    if len(coins) == 0:
        coins = create_coins()
    if len(monsters) == 0:
        monsters = create_monsters()

    if player.lives <= 0:
        gameOver = True
        player.kill()


def graphics():
    global coins, walls, monsters
    screen.fill(BLACK)
    cat_anim()
    sprites.draw(screen)
    walls.draw(screen)
    coins.draw(screen)
    monsters.draw(screen)
    shots.draw(screen)
    for i in range(player.lives):
        screen.blit(life_img, (WIDTH - (i + 1) * 30, HEIGHT - 40))
    text_score = FONT2.render("Score: " + str(player.score), 1, WHITE)
    text_shots = FONT2.render("Shots: " + str(float(player.shots)), 1, WHITE)
    screen.blit(text_score, (10, HEIGHT - 40))
    screen.blit(text_shots, (WIDTH / 2 - 50, HEIGHT - 40))
    pg.display.update()


def gameOver_graphics():
    global gameOver_img
    screen.fill(BLACK)
    gameOver_img = pg.transform.scale(gameOver_img, (100, 100))

    screen.blit(gameOver_img, (WIDTH / 2 - 50, 100))

    text1 = TITLE_FONT.render("Game over", 1, WHITE)
    text2 = FONT2.render("Score: " + str(player.score), 1, WHITE)
    play_again = FONT2.render('Play again', 1, WHITE)
    leave = FONT2.render('Exit', 1, WHITE)
    screen.blit(text1, (WIDTH / 2 - 243, HEIGHT / 2 - 108))
    screen.blit(text2, (WIDTH / 2 - 50, HEIGHT / 2 - 10))
    screen.blit(play_again, (WIDTH / 2 - 60, 349))
    screen.blit(leave, (WIDTH / 2 - 25, 409))


def write_score():
    global player, player_name
    with open('leaderboard.txt', 'r+') as f:
        score_list = []
        for line in f:
            score_list.append(line.strip().split('-'))
        score_list.append([player_name, player.score])
        score_list.sort(key=lambda x: int(x[1]), reverse=True)
        f.truncate(0)
        f.seek(0)
        for s in score_list:
            f.write(s[0] + "-" + str(s[1]) + '\n')


def game_over():
    global player
    write_score()
    btn_again = pg.Rect(WIDTH / 2 - 110, 340, 220, 50)
    btn_end = pg.Rect(WIDTH / 2 - 110, 400, 220, 50)
    click = False
    running = True
    while running:
        gameOver_graphics()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        mx, my = pg.mouse.get_pos()

        if btn_end.collidepoint((mx, my)):
            if click:
                running = False
                pg.quit()
                sys.exit()
        if btn_again.collidepoint((mx, my)):
            if click:
                running = False
                player.kill()

        click = False
        pg.draw.rect(screen, WHITE, btn_again, 4)
        pg.draw.rect(screen, WHITE, btn_end, 4)
        pg.display.update()


def change_state(state):
    player.idle = True
    player.left = False
    player.right = False
    player.up = False
    player.down = False
    if state == 'left':
        player.left = True
        player.facing_right = False
        player.idle = False
    elif state == 'right':
        player.right = True
        player.facing_right = True
        player.idle = False
    elif state == 'up':
        player.up = True
        player.idle = False
    elif state == 'down':
        player.down = True
        player.idle = False
    else:
        player.idle = True


def cat_anim():
    if player.walk_count + 1 >= 6:
        player.walk_count = 0

    if not (player.idle):
        if player.left:
            player.image = walk_left[player.walk_count // 3]
            player.walk_count += 1
            player.facing_right = False
        elif player.right:
            player.image = walk_right[player.walk_count // 3]
            player.walk_count += 1
        elif player.up:
            player.image = walk_up[player.walk_count // 3]
            player.walk_count += 1
        elif player.down:
            player.image = walk_down[player.walk_count // 3]
            player.walk_count += 1
    else:
        if player.facing_right:
            player.image = idle[0]
        else:
            player.image = idle[1]


def enter_name():
    global player_name
    running = True
    player_name = ''
    mon_icon = pg.image.load('assets/mon_icon.png')
    mon_icon = pg.transform.scale(mon_icon, (100, 100))
    input_field = pg.Rect(WIDTH / 2 - 110, 300, 200, 50)
    submit = pg.Rect(WIDTH / 2 - 120, 380, 220, 50)
    warning = FONT2.render('Please enter your name', True, ORANGE_YELLOW)
    warn = False
    click = False
    input_field_border = 4
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pg.K_RETURN:
                    if player_name == '':
                        warn = True
                    else:
                        running = False
                else:
                    player_name += event.unicode
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.fill(BLACK)

        mx, my = pg.mouse.get_pos()

        if submit.collidepoint((mx, my)):
            if click:
                if player_name == '':
                    warn = True
                else:
                    running = False
        if input_field.collidepoint((mx, my)):
            if click:
                input_field_border = 6

        click = False

        screen.blit(mon_icon, (WIDTH / 2 - 50, 50))

        pg.draw.rect(screen, WHITE, input_field, input_field_border)
        pg.draw.rect(screen, WHITE, submit, 4)

        title = FONT.render('Enter your name', True, WHITE)
        text = FONT2.render(player_name, True, WHITE)
        submit_text = FONT2.render('CONFIRM NAME', True, WHITE)
        screen.blit(title, (WIDTH / 2 - 202.5, HEIGHT / 2 - 120))
        screen.blit(text, (input_field.x + 10, input_field.y + 7))
        screen.blit(submit_text, (WIDTH / 2 - 94.5, 390))
        if warn:
            screen.blit(warning, (WIDTH / 2 - 150, 250))
        pg.display.update()


def wall_xy(map_list, wall_list, free_list):
    mx = 0
    my = 0
    n = r.randint(0, len(map_list) - 1)
    for i in range(0, map_w * map_h):
        if map_list[n][mx + (my * map_w)] == 1:
            wall_list.append((mx * 40, my * 40))
        else:
            free_list.append((mx * 40, my * 40))
        mx += 1
        if mx > map_w - 1:
            mx = 0
            my += 1
    remove_list = [(360, 240), (400, 240), (440, 240), (320, 240), (280, 240)]
    for item in remove_list:
        free_list.remove(item)


wall_xy(map_list, wall_list, free_list)

coins = create_coins()
walls = setupwalls()
monsters = create_monsters()

main()
