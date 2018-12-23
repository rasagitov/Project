import pygame
import os
import random
pygame.init()

pos_x = 1366/2 - 768/2 
pos_y =  1366 - 768
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'

win =pygame.display.set_mode((800,600))
pygame.display.set_caption("SpaceWar")
clock = pygame.time.Clock()
bg = pygame.image.load('bg4.jpg')

def paused():
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render("PAUSE",True,(255,255,255)), (400,570))
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        pygame.display.update()
        clock.tick(15)
    return

def crushed():
    win.blit(pygame.font.SysFont("Courier New",50, 'bold').render("GAME OVER",True,(255,0,0)), (200,250))
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render("Press N to start new game",True,(255,0,0)), (200,300))
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    pause = False
        pygame.display.update()
        clock.tick(15)
    return

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 760)
        self.rect.y = 0
        self.speed = 10
        self.movey = 1
    def move(self):
        self.rect.y += self.movey*self.speed
enemies = []
class Bullet():
    def __init__(self):
        self.image = pygame.image.load('Bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x+10
        self.rect.y = player.rect.y+30
        self.movey=-1
    def dist(self, count):
        if count == 0:
            self.rect.x += 68
            
class PlayerActive():
    def __init__(self):
       self.image = pygame.image.load('ship4.png')
       self.rect = self.image.get_rect()
       self.rect.x = 250
       self.rect.y = 470
       self.speed = 4
       self.ammo = []
    def move(self, xdir):
        self.rect.x += xdir*self.speed
    def spawnAmmo(self, count):
        bullet = Bullet()
        bullet.dist(count)
        self.ammo.append(bullet)
    def moveAmmo(self):
        for obj in self.ammo:
            obj.rect.y +=obj.movey
            
player = PlayerActive()
k=0
FPS = 60


def draw_window(score,hp):
    
    win.blit(bg, (0, 0))
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render("Score",True,(255,255,0)), (0,570))
    scoreWRITE=str(score)
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render(scoreWRITE,True,(255,255,0)), (150,570))
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render("HP",True,(255,0,0)), (200,570))
    hpWRITE=str(hp)
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render(hpWRITE,True,(255,0,0)), (250,570))
    win.blit(player.image, player.rect)
    for obj in player.ammo:
        win.blit(obj.image, obj.rect)
    for obj in enemies:
        win.blit(obj.image, obj.rect)
    pygame.display.update()
    clock.tick(FPS)
try:
    f = open("savegame.txt")
except IOError:
    f = open("savegame.txt", "w")
    f.write('0')
    f.write('\n')
    f.write('10')
    f.close()
f = open("savegame.txt", "rb")
scoreREAD = f.readline()
hpREAD = f.readline()
if scoreREAD == '':
    score = 0
else:
    score = int(scoreREAD)
if hpREAD == '':
    hp = 10
else:
    hp = int(hpREAD)
f.close()
    
def save(score,hp):
    f = open("savegame.txt", "w")
    scoreWRITE=str(score)
    hpWRITE = str(hp)
    f.write(scoreWRITE)
    f.write('\n')
    f.write(hpWRITE)
    f.close()
    print('Saved')
    win.blit(pygame.font.SysFont("Courier New",30, 'bold').render("SAVED",True,(255,255,0)), (500,570))
    pygame.display.update()
    clock.tick(1)
    
gameActive = True
while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save(score,hp)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if len(player.ammo) < 15:
                    if k==0:
                        player.spawnAmmo(0)
                        k+=1
                    else:
                        player.spawnAmmo(1)
                        k-=1
    activeKey =pygame.key.get_pressed()
    player.moveAmmo()
    if activeKey[pygame.K_LEFT]:
        if player.rect.x > 0:
            player.move(-1)
    if activeKey[pygame.K_RIGHT]:
        if player.rect.x < 704:
            player.move(1)
    
            
    for bullet in player.ammo:
        if bullet.rect.y < 0:
            player.ammo.pop(player.ammo.index(bullet))
            
    if len(enemies) < 10:
        enemies.append(Enemy())
    for obj in enemies:
        if obj.rect.y >520:
            enemies.pop(enemies.index(obj))
            hp -=1
        obj.rect.y +=obj.movey
    
    for enemy in enemies:
        for bullet in player.ammo:
            if (enemy.rect.y+15 >= bullet.rect.y >= enemy.rect.y-15):
                if (enemy.rect.x + 40 >= bullet.rect.x  >= enemy.rect.x - 8):
                    enemies.pop(enemies.index(enemy))
                    player.ammo.pop(player.ammo.index(bullet))
                    score +=1
    
    draw_window(score,hp)
    if hp <= 0:
        while enemies != []:
            enemies.pop()
        while player.ammo != []:
            player.ammo.pop()
        crushed()
        hp = 10
        score = 0
        save(score,hp)
pygame.quit()
