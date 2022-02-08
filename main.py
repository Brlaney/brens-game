import pygame
from sys import exit
from random import randint, choice

class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        duck_walk_1 = pygame.image.load(
            'assets/graphics/duck/duck_walk_r1.png').convert_alpha()
        duck_walk_2 = pygame.image.load(
            'assets/graphics/duck/duck_walk_r2.png').convert_alpha()
        self.duck_walk = [duck_walk_1, duck_walk_2]
        self.duck_index = 0
        self.duck_jump = pygame.image.load(
            'assets/graphics/duck/duck_jump_r.png').convert_alpha()

        self.image = self.duck_walk[self.duck_index]
        self.rect = self.image.get_rect(midbottom=(80, 470))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def duck_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 470:
            self.gravity = -30
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 470:
            self.rect.bottom = 470

    def animation_state(self):
        if self.rect.bottom < 470:
            self.image = self.duck_jump
        else:
            self.duck_index += 0.1
            if self.duck_index >= len(self.duck_walk):
                self.duck_index = 0
            self.image = self.duck_walk[int(self.duck_index)]

    def update(self):
        self.duck_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load(
                'assets/graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load(
                'assets/graphics/fly/Fly1.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 320
        else:
            snail_1 = pygame.image.load(
                'assets/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'assets/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 460

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, ('#FC9301'))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(duck.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def duck_animation():
    global duck_surf, duck_index

    if duck_rect.bottom < 460:
        duck = duck_jump

    else:
        duck_index += 0.1
        if duck_index >= len(duck_walk1):
            duck_index = 0
        duck_surf = duck_walk1[int(duck_index)]


# Initialize, settings, config
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Chick Bad')
clock = pygame.time.Clock()
test_font = pygame.font.Font('assets/font/JosefinSans-Regular.ttf', 44)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('assets/audio/music.wav')
bg_music.play(loops=-1)

# Groups
duck = pygame.sprite.GroupSingle()
duck.add(Duck())
obstacle_group = pygame.sprite.Group()

# Background & foreground
sky_surf = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

# Intro screen
duck_stand = pygame.image.load(
    'assets/graphics/duck_intro.png').convert_alpha()
duck_stand = pygame.transform.rotozoom(duck_stand, 0, 1)
duck_stand_rect = duck_stand.get_rect(center=(400, 400))

game_name = test_font.render('My Chick Bad', False, ('#FFB903'))
game_name_rect = game_name.get_rect(center=(400, 175))

game_message = test_font.render('Press space to start', False, ('#FC9301'))
game_message_rect = game_message.get_rect(center=(400, 250))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# Function that will trigger constant rendering
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 460))
        score = display_score()

        duck.draw(screen)
        duck.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill(('#FBF9F9'))
        screen.blit(duck_stand, duck_stand_rect)

        score_message = test_font.render(
            f'Your score: {score}', False, ('#FC9301'))
        score_message_rect = score_message.get_rect(center=(400, 250))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
