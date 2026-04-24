from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > -15:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def ogon(self):
        pulka = Pulya('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 3)
        puli.add(pulka)

loss = 0
schot = 0
num_fire = 0
rel_time = False
shotchik = 5

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0, 650)
            self.rect.y = 0
            global loss
            loss = loss + 1

class Pulya(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -20:
            self.rect.y = 0
            self.kill()

vragi = sprite.Group() 
for i in range(5):
    vrag = Enemy('ufo.png', randint(0, 650), 0, 100, 65, randint(1, 2))
    vragi.add(vrag)

asteroidi = sprite.Group()
for i in range(1):
    asteroid = Enemy('asteroid.png', randint(0, 650), 0, 80, 80, 3)
    asteroidi.add(asteroid)

puli = sprite.Group()

vertoletik = Player('rocket.png', 320, 370, 75, 120, 7)

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 60

font.init()
font1 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font = font.Font(None, 70)

game = True
finsh = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                if num_fire < 7 and rel_time == False:
                    vertoletik.ogon()
                    fire.play()
                    num_fire += 1
                if num_fire >= 7 and rel_time == False:
                    rel_time = True
                    secynda = timer()


    if finsh == False:
    

#! xsvbfxdsdgasgfs
#TODO fsddscv
#? sdfrf
# fgff
#* dsfesdf
#// werdfewfd


        window.blit(background, (0, 0))
        text_lose = font1.render('Пропущено: ' + str(loss), True, (255, 255, 255))
        window.blit(text_lose, (10, 70))
        vin = font1.render('YOU VIN!', True, (0, 225, 0))
        nevin = font1.render('YOU NE VIN!', True, (255, 0, 0))
        vertoletik.update()
        vertoletik.reset()
        vragi.update()
        vragi.draw(window)
        asteroidi.update()
        asteroidi.draw(window)
        puli.update()
        puli.draw(window)

        if rel_time == True:
            secynda2 = timer()
            if secynda2 - secynda < 1:
                text_perezoriadki = font1.render('Перезарядка...', True, (255, 255, 255))
                window.blit(text_perezoriadki, (10, 450))
            else:
                num_fire = 0
                rel_time = False

        list1 = sprite.groupcollide(vragi, puli, True, True)
        for i in list1:
            schot += 1
            vrag = Enemy('ufo.png', randint(0, 650), 0, 100, 65, randint(1, 2))
            vragi.add(vrag)

        if schot >= 50:
            finsh = True
            window.blit(vin, (300, 250))

        text_core = font1.render('Счёт: ' + str(schot), True, (255, 255, 255))
        window.blit(text_core, (10, 35))

        jizny = font1.render(str(shotchik), True, (255, 0, 0))
        window.blit(jizny, (600, 35))

        if sprite.spritecollide(vertoletik, vragi, False) or loss >= 3:
            finsh = True
            window.blit(nevin, (290, 250))

        if sprite.spritecollide(vertoletik, asteroidi, False):
            finsh = True
            window.blit(nevin, (290, 250))




    display.update()
    clock.tick(FPS)