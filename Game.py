import pygame
import random

import sys
pygame.init()
pygame.font.init()
windows = pygame.display.set_mode((626,417))
pygame.display.set_caption("Alien shooter")
bg = pygame.image.load("background.jpg")


class Settings:
    def __init__(self):
        self.sw = 626
        self.sh = 417


game = Settings()


class Player:
    def __init__(self):
        self.height = 65
        self.width = 60
        self.vel = 10
        self.x = game.sw/2-self.width/2
        self.y = game.sh-self.height
        self.player = pygame.image.load("shipsprite1.png")
        self.hitbox = (self.x, self.y, 60, 65)


ship = Player()


class Bullets:
    def __init__(self):
        self.x = ship.x+round(ship.width/2)
        self.y = ship.y
        self.width = 3
        self.height = 15

    def draw(self,windows):
        pygame.draw.rect(windows,(60,60,60),(self.x,self.y,self.width,self.height))


class Enemy:
    def __init__(self):
        self.width = 100
        self.height = 130
        self.x=random.randrange(game.sw-64)
        self.y = random.randrange(-400,-100)
        self.bg = pygame.image.load("enemy.png")
        self.x1=random.randrange(50,100)
        self.y2=random.randrange(50,100)
        self.hitbox = (self.x + 17, self.y + 2, self.x1, self.y2)

    def update(self):
        self.y += 10
        if self.y > game.sh+10:
            self.x = random.randint(0,game.sw-64)
            self.y = random.randint(-100,0)

    def draw(self,windows):
        windows.blit(pygame.transform.scale(self.bg,(self.x1,self.y2)),(self.x, self.y))
        self.hitbox = (self.x, self.y, self.x1,self.y2)


def gameoverscreen():
    music = pygame.mixer.music.load("music.wav")
    pygame.mixer.music.play(-1)
    gamefont = pygame.font.SysFont('consolas', 64, True)
    text3 = gamefont.render("Click Anywhere", 1, (166, 166, 166))
    gamefont1 = pygame.font.SysFont('consolas', 28, True)
    text4 = gamefont1.render("Use Arrow Keys to Move", 1, (166, 166, 166))
    gamefont2 = pygame.font.SysFont('consolas', 12, True)
    text5 = gamefont2.render("advanced players can use A & D", 1, (166, 166, 166))
    text6 = gamefont1.render("X or Space to shoot", 1, (166, 166, 166))
    text7=gamefont1.render("HIGH SCORE: "+str(max), 1, (166, 166, 166))
    windows.blit(bg,(0,0))
    windows.blit(text3,(70,game.sh-100))
    windows.blit(text4, (140, 40))
    windows.blit(text5, (205, 100))
    windows.blit(text6, (170, 130))
    windows.blit(text7,(210,220))
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting=False


def draw():
    pygame.font.get_fonts()
    gamefont = pygame.font.SysFont('comicsansms',30,True)
    text=gamefont.render("score: "+str(score), 1, (166, 166, 166))
    windows.blit(bg, (0, 0))
    windows.blit(ship.player, (ship.x, ship.y))
    ship.hitbox = (ship.x+10, ship.y, 40, 65)
    for bullet in bullets:
        bullet.draw(windows)
    for alien in aliens:
        alien.draw(windows)
    pygame.draw.rect(windows,(60,60,60),(game.sw/2-5, 25, 5, 20))
    text2=gamefont.render(str(100-bulletnumber),1,(166,166,166))
    windows.blit(text, (game.sw-200, 10))
    windows.blit(text2,(game.sw/2, 10))
    life=pygame.image.load("shipsprite1.png")
    if health==3:
        windows.blit(pygame.transform.scale(life,(30,30)),(10,10))
        windows.blit(pygame.transform.scale(life, (30, 30)), (10 + 30, 10))
        windows.blit(pygame.transform.scale(life, (30, 30)), (10 + 30 + 30, 10))
    if health==2:
        windows.blit(pygame.transform.scale(life, (30, 30)), (10, 10))
        windows.blit(pygame.transform.scale(life, (30, 30)), (10+30, 10))
    if health==1:
        windows.blit(pygame.transform.scale(life, (30, 30)), (10, 10))
    pygame.display.update()


# main game loop
clock = pygame.time.Clock()
shootloops = 0
run = True
max=0
gameover = True
pygame.time.set_timer(pygame.USEREVENT + 1, 3000)
pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
pygame.time.set_timer(pygame.USEREVENT + 3, 15000)

while run:
    if gameover:
        aliens = []
        bullets = []
        bulletnumber = 0
        speed = 30
        health = 3
        score = speed // 5 - 6
        gameoverscreen()
        gameover=False
    if health == 0:
        gameover=True
    if shootloops == 3:
        shootloops = 0
    if score>max:
        max = score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT + 1:
            speed += 1
        if event.type == pygame.USEREVENT+2:
            score += 1
        if event.type == pygame.USEREVENT+3:
            if bulletnumber > 0:
                bulletnumber = 0
            if health<3:
                health+=1
    if len(aliens) < random.randrange(5,8):
        aliens.append(Enemy())
    for alien in aliens:
        alien.update()
        if alien.y > game.sh+10:
            aliens.remove(alien)
    for alien in aliens:
        if ship.hitbox[1] < alien.hitbox[1] + alien.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > alien.hitbox[1]:
            if ship.hitbox[0] + ship.hitbox[2] > alien.hitbox[0] and ship.hitbox[0] < alien.hitbox[0] + alien.hitbox[2]:
                if len(aliens) != 0:
                    aliens.remove(alien)
                    health -= 1
                    windows.blit(pygame.transform.scale(pygame.image.load("explosion.png"),(150,150)),(ship.x-ship.width//2-10,ship.y-ship.height))
                    pygame.display.update()

        else:
            for bullet in bullets:
                if bullet.y  < alien.hitbox[1] + alien.hitbox[3] and bullet.y  > alien.hitbox[1]:
                    if bullet.x > alien.hitbox[0] and bullet.x  < alien.hitbox[0] + alien.hitbox[2]:
                        bullets.remove(bullet)
                        score=score+3
                        if bullet.y < alien.hitbox[1] + alien.hitbox[3] and bullet.y > alien.hitbox[1]:
                            if bullet.x > alien.hitbox[0] and bullet.x < alien.hitbox[0] + alien.hitbox[2]:
                                if len(aliens) != 0:
                                    aliens.remove(alien)
    for bullet in bullets:
        if bullet.y > 0 and bullet.y < game.sw:
                bullet.y -= ship.vel*2
        else:
            bullets.remove(bullet)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.x > 0 or keys[pygame.K_a] and ship.x > 0:
        ship.x -= ship.vel

    if keys[pygame.K_RIGHT] and ship.x+ship.width<game.sw or keys[pygame.K_d] and ship.x+ship.width<game.sw:
        ship.x += ship.vel

    if keys[pygame.K_x] and bulletnumber<100 and shootloops == 0 or keys[pygame.K_SPACE] and bulletnumber<100 and shootloops == 0:
        bullets.append(Bullets())
        bulletnumber += 1
    shootloops += 1
    clock.tick(speed)
    draw()
pygame.quit()