# we are importing essential libraries
import random
import time

import pygame

# built in pygame input macros
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Set Game MACROS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Class Declaration
class ElemHero(pygame.sprite.Sprite):

    # This is the class constructor
    def __init__(self, init_x, init_y, size):
        super(ElemHero, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.x = init_x
        self.y = init_y

# this is the funtion that moves the square on the screen.
    def move_hero(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

    # This set of if statements will make sure the player stays in bounds
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Enemy Class // when inheriting the class you are trying to inherit goes inside parenthesis
class Enemy(pygame.sprite.Sprite):

    def __init__(self,size):
        super(Enemy,self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(

            # this is simply going to spawn the enemy randomly in the scene
                    center=(
                        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                        random.randint(0, SCREEN_HEIGHT),
                    ))
        self.speed = random.randrange(-5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right <= 0:
            self.kill()



class Menu:

    def __init__(self):
        self.surf = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2
            )
        )
        self.menu_text = my_font.render('Click to Start', False, RED)

    def start_menu(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.menu_text, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))


# Initialize the audio mixer
pygame.mixer.init()

pygame.mixer.music.load("./Asssets/New_Project.mp3")
pygame.mixer.music.play(loops=-1)

# Initialize pygame
pygame.init()


# Create The Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Here we are creating user created events
# the +1 on this line just ensures that the userevent created has a unique id.
#  - as thats how events are stored in pygame (ENUM maybe?)
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

menu = Menu()


# creating the player
hero_x = 50
hero_y = 80
hero = ElemHero(hero_x, hero_y, 20)


# these sprite groups are being created to add collision detection
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# we need to add the created entities to the sprite groups
all_sprites.add(hero)

# Game loop bool
running = True
ismenu = True

# Establish the games framerate
clock = pygame.time.Clock()


# Game loop (where all the magic happens)
while running:
    if not ismenu:
        # The event.get will return a list of game events we need to iterate through to listen
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

                # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(random.randrange(25, 75))
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # This will store a Dictionary of pressed keys we can use as player input
        pressed_keys = pygame.key.get_pressed()

        # this just calls the function that moves the player
        hero.move_hero(pressed_keys)

        screen.fill(WHITE)

        # this will draw any entity added to the sprites array
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(hero, enemies):
            hero.kill()
            running = False
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        enemies.update()

        # this is needed so that we can continually display what we draw
        pygame.display.update()

    # This will display the menu screen
    elif ismenu:
        # The event.get will return a list of game events we need to iterate through to listen
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu.rect.collidepoint((mouse[0], mouse[1])):
                    ismenu = False

            screen.fill(WHITE)

            menu.start_menu(screen)
            mouse = pygame.mouse.get_pos()

            pygame.display.update()
    # this establishes the framerate at 30 fps
    clock.tick(60)

pygame.quit()
