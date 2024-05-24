import random
import pygame
import time
from pygame.locals import(RLEACCEL,K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,K_RETURN)
pygame.init()
ADDENEMY= pygame.USEREVENT+2
pygame.time.set_timer(ADDENEMY,250)
screenwidth = 800
screenheight = 800
screen = pygame.display.set_mode((screenwidth,screenheight))
bg=pygame.image.load("space.png")
clock = pygame.time.Clock()
l=3
flag1=1
class Meteors(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteors, self).__init__()
        self.surf = pygame.image.load("meteors.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect(center=(random.randint(screenwidth+20,screenwidth+100),(random.randint(0,screenheight))))
        self.speed=random.randint(2,10)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect(center=(random.randint(screenwidth+20,screenwidth+100),(random.randint(100,screenheight))))
        self.speed=random.randint(2,10)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()

class Finishline(pygame.sprite.Sprite):
    def __init__(self):
        super(Finishline, self).__init__()
        self.surf = pygame.image.load("finishline.jpg").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect(center=(screenwidth+100000,300))
        self.speed=2
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right> screenwidth:
            self.rect.right=screenwidth
        if self.rect.top<=0:
            self.rect.top=0
        if self.rect.bottom>=screenheight:
            self.rect.bottom=screenheight

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies=pygame.sprite.Group()
meteors=pygame.sprite.Group()
finishline=pygame.sprite.Group()
f=Finishline()
all_sprites.add(f)
finishline.add(f)
running = True

while running:

    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.type == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type==ADDENEMY:
            new_enemy=Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


            new_meteors=Meteors()
            meteors.add(new_meteors)
            all_sprites.add(new_meteors)





    if flag1 ==1:
        col = pygame.sprite.spritecollideany(player, enemies or meteors)
        fcol=pygame.sprite.spritecollideany(player,finishline)

        player.update(pressed_keys)
        enemies.update()
        meteors.update()
        finishline.update()
        screen.fill((0, 0, 0))
        screen.blit(bg,(0,0))
        Font = pygame.font.SysFont("cosmicsansms", 50, True, True)
        hp = Font.render("HEALTH: " + str(l), True, (255, 255, 255))
        screen.blit(hp, (10, 10))

        if fcol:
            fcol.kill()
            l=0
            print("test")
        if col:
            col.kill()
            l = l - 1
        if l == 0:
            player.kill()
            flag1=0

        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)

    else:
        if pressed_keys[K_RETURN]:
            for s in all_sprites:
                s.kill()
            for e in enemies:
                e.kill()
            for m in meteors:
                m.kill()
            for fi in finishline:
                fi.kill()
            all_sprites.add(player)
            all_sprites.add(f)
            finishline.add(f)
            f.rect.x=1500
            l=3
            flag1=1
        else:
            screen.fill((0,0,0))
            go_font= pygame.font.SysFont("cosmicsansms",80,True,True)
            go =go_font.render("GAME OVER!", True,(255,255,255))
            text = pygame.font.SysFont("cosmicsansms", 50, True, True)
            txt = text.render("Press 'ENTER' to restart", True, (255, 255, 255))
            screen.blit(go,(50,100))
            screen.blit(txt,(50,200))
    clock.tick(120)
    pygame.display.flip()

