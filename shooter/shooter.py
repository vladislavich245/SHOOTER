from pygame import *

mixer.init()
mixer.music.load('space.org')
mixer.music.play()
fire_sound = mixer.Sound('fire.org')

jmg_back = 'galaxy.jpg'
jmg_hero = 'rocket.png'

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), size: (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect = player_x
        self.rect = player_y

    def reset(self):
        window.blit(self.image, dest: (self.rect.x, self.rect.y))

class Player(GameSprite):