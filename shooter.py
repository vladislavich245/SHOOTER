from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None,  80)
win = font1.render( 'YOU WIN!',True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))
font2 = font.Font(None,36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_meteor = 'asteroid.png'

score = 0
goal = 30
lost = 0
max_lost = 3
cooldown = 500

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back),  (win_width, win_height))

ship = Player(img_hero,  350, win_height - 100, 50, 100, 10 )

meteors = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80, win_width - 80),-40, 80,  50, randint(1,5))
    monsters.add(monster)
finish = False
bullets = sprite.Group()
a = randint(1,200)

if a == 1:
    meteor = Meteor(img_meteor,randint(80, win_width - 80),-40, 100,  100, randint(3,7))
    meteors.add(meteor)
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and cooldown > 8:

                ship.fire()
                cooldown = 0
    if not finish:

        window.blit(background,  (0,0))

        if a == 1:
            meteor = Meteor(img_meteor, randint(80, win_width - 80), -40, 70, 70, randint(1, 5))
            meteors.add(meteor)
        text = font2.render("Рахунок: " + str(score),1,(255,255,255))
        window.blit(text,  (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost),  1,  (255 ,255, 255))
        window.blit(text_lose,  (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        meteors.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteors.draw(window)

        collides = sprite.groupcollide(monsters,bullets, True, True)
        collides2 = sprite.groupcollide(monsters,meteors, True, False)
        for c in collides:
            score +=1
            monster = Enemy(img_enemy,randint( 80,win_width - 80,), -40,80,50,randint(1,5))
            monsters.add(monster)

        for c in collides2:
            monster = Enemy(img_enemy,randint( 80,win_width - 80,), -40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost or sprite.spritecollide(ship,meteors,False):
            finish = True
            print ('loose')
            window.blit(lose, (200,200))
        if a == 1:
            print('yay')
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        display.update()
        cooldown+=1
        a = randint(1, 200)
    time.delay(50)