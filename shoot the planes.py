# coding: utf-8
 
import pygame
import sys
import os
from random import randint
from pygame.locals import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))#test所在文件夹test，os.path.dirname(os.path.dirname(os.path.abspath(__file__)))是settings所在文件夹config
pygame.init()  # initialize the game
pygame.mixer.init()  # initialize the mixer
bg_size = 480, 852  # initialize the background size(width, height)


screen = pygame.display.set_mode(bg_size)  # set the background window
pygame.display.set_caption("shoot the plane")  # set the title 
background = pygame.image.load(os.path.join(BASE_DIR, "material/image/background.png"))  # load the background picture and set
 

 #------------music------------------------
# background music
pygame.mixer.music.load(os.path.join(BASE_DIR, "material/sound/game_music.wav"))
pygame.mixer.music.set_volume(0.2)

# bullet shooting sound
bullet_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/bullet.wav"))
bullet_sound.set_volume(0.2)

# me down sound
me_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/game_over.wav"))
me_down_sound.set_volume(0.2)

# enemy down sound
enemy1_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy1_down.wav"))
enemy1_down_sound.set_volume(0.2)

enemy2_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy2_down.wav"))
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy3_down.wav"))
enemy3_down_sound.set_volume(0.2)

button_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/button.wav"))
button_down_sound.set_volume(0.2)

level_up_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/achievement.wav"))
level_up_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/use_bomb.wav"))
bomb_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/get_bomb.wav"))
get_bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/get_double_laser.wav"))
get_bullet_sound.set_volume(0.2)

big_enemy_flying_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/big_spaceship_flying.wav"))
big_enemy_flying_sound.set_volume(0.2)


#------------Sprite------------------------
class OurPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(OurPlane, self).__init__()
        # set up our plane's picture (keep the two pictures switching, bringing a dynamic effect)
        self.image_one = pygame.image.load(os.path.join(BASE_DIR, "material/image/hero1.png"))
        self.image_two = pygame.image.load(os.path.join(BASE_DIR, "material/image/hero2.png"))
        # get the location of our plane
        self.rect = self.image_one.get_rect()
        # localize the size of the background picture
        self.width, self.height = bg_size[0], bg_size[1]
        # capture the mask of the plane image for more accurate collision detection
        self.mask = pygame.mask.from_surface(self.image_one)
        # define the plane's initialization position with 60 pixels reserved at the bottom
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)
        # Set the speed of the plane
        self.speed = 10
        # set the plane's survival status (true to survive, false to death)
        self.active = True
        # loading the plane's damage pictures
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load(os.path.join(BASE_DIR, "material/image/hero_blowup_n1.png")),
                pygame.image.load(os.path.join(BASE_DIR, "material/image/hero_blowup_n2.png")),
                pygame.image.load(os.path.join(BASE_DIR, "material/image/hero_blowup_n3.png")),
                pygame.image.load(os.path.join(BASE_DIR, "material/image/hero_blowup_n4.png")),
            ]
        )

    def move_up(self):
        """
        the operation function of the plane moving upward
        """
        if self.rect.top > 0:  # if the plane has not moved out of the background area
            self.rect.top -= self.speed
        else:  # if the plane is about to move out of the background area, correct it as a background edge position
            self.rect.top = 0

    def move_down(self):
        """
        our plane moved down
        """
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        """
        our plane moved left
        """
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        """
        our plane moved right
        """
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        # initialize the plane(when the plane dies, put it to the original position)
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)
        # reset the plane's survival status
        self.active = True

		
class SmallEnemy(pygame.sprite.Sprite):
    """
    define small enemy planes
    """
    energy = 1

    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy1.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.mask = pygame.mask.from_surface(self.image)  
        self.speed = 2
        self.energy = SmallEnemy.energy
        # define where the enemy planes appear to ensure that they do not appear immediately before the game has started
        self.rect.left, self.rect.top = (
            randint(0, self.width - self.rect.width),  randint(-5 * self.rect.height, -5),
        )
        self.active = True
        # loading plane's damage pictures
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load("material/image/enemy1_down1.png"),
                pygame.image.load("material/image/enemy1_down2.png"),
                pygame.image.load("material/image/enemy1_down3.png"),
                pygame.image.load("material/image/enemy1_down4.png")
            ]
        )

    def move(self):
        """
        define the movement function of enemy planes

        """
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        """
        When the enemy planes move down the screen and the plane needs to appear randomly, and the enemy planes die,

        """
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width), randint(-5 * self.rect.height, 0))
        self.active = True


class MidEnemy(pygame.sprite.Sprite):

    def __init__(self):
        super(MidEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy2.png")


class BigEnemy(pygame.sprite.Sprite):

    def __init__(self):
        super(BigEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy3.png")
		
class Bullet(pygame.sprite.Sprite):

    def __init__(self, position):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("material/image/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 30
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """
        the bullets are set to die if they move beyond the screen range

        """
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self, position):
        """
        reset function

        """
        self.rect.left, self.rect.top = position
        self.active = True

		
		
#-------------display---------------------
def add_small_enemies(group1, group2, num):
    """
    add small enemy planes
    specify an enemy plane object to add to the sprite Group (sprite.group)
    """
    for i in range(num):
        small_enemy = SmallEnemy(bg_size)
        group1.add(small_enemy)
        group2.add(small_enemy)
		
		
# set the blood groove color
color_black = (0, 0, 0)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_white = (255, 255, 255)

# get our plane
our_plane = OurPlane(bg_size)

def main():
    # music
    pygame.mixer.music.play(-1)  # -1 represents an infinite loop
    running = True
    switch_image = False  # give the plane a jet effect
    delay = 60  # delay some effects for better results

    enemies = pygame.sprite.Group()  # generate an enemy planes group
    small_enemies = pygame.sprite.Group()  # set an enemy small planes group 

    add_small_enemies(small_enemies, enemies, 6)  # generate a number of enemy small planes

    # define the destruction image index of bullets, all kinds of enemy planes and our plane
    bullet_index = 0
    e1_destroy_index = 0
    me_destroy_index = 0

    # define the number of instantiated bullets
    bullet1 = []
    bullet_num = 6
    for i in range(bullet_num):
        bullet1.append(Bullet(our_plane.rect.midtop))

    while running:

        # set the background
        screen.blit(background, (0, 0))

        # set the number of frames
        clock = pygame.time.Clock()
        clock.tick(60)

        # set two different forms of our plane
        if not delay % 3:
            switch_image = not switch_image

        for each in small_enemies:
            if each.active:
                # randomly and continuously output small enemy planes
                each.move()
                screen.blit(each.image, each.rect)

                pygame.draw.line(screen, color_black,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                energy_remain = each.energy / SmallEnemy.energy
                if energy_remain > 0.2:  # it is green if the blood volume is over 20%, otherwise it is red
                    energy_color = color_green
                else:
                    energy_color = color_red
                pygame.draw.line(screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                 2)
            else:
                if e1_destroy_index == 0:
                    enemy1_down_sound.play()
                screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                e1_destroy_index = (e1_destroy_index + 1) % 4
                if e1_destroy_index == 0:
                    each.reset()

        # when our plane survives, normally display the plane images
        if our_plane.active:
            if switch_image:
                screen.blit(our_plane.image_one, our_plane.rect)
            else:
                screen.blit(our_plane.image_two, our_plane.rect)

            # the plane can only fire bullets when it survives
            if not (delay % 10):  # a moving bullet is fired every 10 frames
                bullet_sound.play()
                bullets = bullet1
                bullets[bullet_index].reset(our_plane.rect.midtop)
                bullet_index = (bullet_index + 1) % bullet_num

            for b in bullets:
                if b.active:  # only activated bullets could hit enemy planes
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:  #  if the bullet hits the plane
                        b.active = False  #  the bullet is damaged
                        for e in enemies_hit:
                            e.active = False  # the small enemy plane damaged

        # draw the scene of the explosion
        else:
            if not (delay % 3):
                screen.blit(our_plane.destroy_images[me_destroy_index], our_plane.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    me_down_sound.play()
                    our_plane.reset()

		# call spritecollide, the collision method, if our plane collides with enemy planes, change the survival status
        enemies_down = pygame.sprite.spritecollide(our_plane, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            our_plane.active = False
            for row in enemies:
                row.active = False

        # respond to player actions
        for event in pygame.event.get():
            if event.type == 12:  #  if the player presses the close button on the screen, trigger the quit event, the program exits
                pygame.quit()
                sys.exit()

        if delay == 0:
            delay = 60
        delay -= 1

        #  get the keyboard inputs from the player
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            our_plane.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            our_plane.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            our_plane.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            our_plane.move_right()

        # Draw the image and output it to the screen
        pygame.display.flip() 

main()