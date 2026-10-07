import pygame
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 75

screen_weight, screen_height = 864, 936
screen = pygame.display.set_mode((screen_weight, screen_height))

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_time = 1500
last_pipe = pygame.time.get_ticks() - pipe_time
score = 0 
pass_pipe = False
font = pygame.font.SysFont('Bauhaus 93', 60)

button_img = pygame.image.load('img/restart.png')
bg_image = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0 
    return score 


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.space_pressed = False

    def update(self):
        self.counter += 1
        flap_cooldown = 10
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 760:
                self.rect.y += int(self.vel)
        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.space_pressed:
                self.space_pressed = True
                self.vel = -10
            if not keys[pygame.K_SPACE]:
                self.space_pressed = False

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - int(pipe_gap / 2))
        if position == -1:
            self.rect.topleft = (x, y + int(pipe_gap / 2))
            
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
            

class Button:
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x , self.rect.y))

        return action




button = Button(screen_weight // 2 - 50, screen_height // 2 - 100, button_img)
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:
    clock.tick(FPS)
    pipe_gap = random.choice([150, 200, 250])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    screen.blit(bg_image, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, screen_height - 168))

    if len(pipe_group) > 0:
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
            and pass_pipe == False
        ):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1 
                pass_pipe = False

    draw_text(str(score), font, (255, 255, 240), int(screen_weight / 2), 20 )
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <0:
        game_over = True





    if not game_over and flying:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_time:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_weight, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_weight, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom > 760:
        game_over = True
        flying = False

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    pygame.display.update()

pygame.quit()