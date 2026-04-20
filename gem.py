import pygame
import random
import os

pygame.init()

highScore = "highscore.txt"
screen = pygame.display.set_mode((500,600))
pygame.display.set_caption("寶石接接樂")
clock = pygame.time.Clock()

background_img = pygame.image.load(os.path.join("img","background.png")).convert()
background_img = pygame.transform.scale(background_img,(500,600))
bomb_img = pygame.image.load(os.path.join("img","bomb.png")).convert()
bomb_img.set_colorkey((0, 0, 0))

font_name = "font.ttf"

gem_imgs = []
for i in range(3):
    gem_img = pygame.image.load(os.path.join("img",f"gem{i+1}.png")).convert()
    gem_img.set_colorkey((0,0,0))
    gem_imgs.append(gem_img)

player_imgs = []
for i in range(4):
    player_img = pygame.image.load(os.path.join("img",f"player{i}.png")).convert()
    player_img.set_colorkey((0, 0, 0))
    player_imgs.append(player_img)

player_mini_img = pygame.transform.scale(player_imgs[0],(25, 19))
player_mini_img.set_colorkey((0, 0, 0))
pygame.display.set_icon(player_mini_img)

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,(0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def load_score():
    if os.path.exists(highScore):
        try:
            with open(highScore,"r",encoding="utf-8") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_score(score):
    with open(highScore,"w",encoding="utf-8") as f:
        f.write(str(score))

def draw_init(high_score):
    screen.blit(background_img,(0, 0))
    draw_text(screen,"寶石接接樂",42,250,60)
    draw_text(screen,"左右鍵移動角色接寶石",24,250,140)
    draw_text(screen,"白寶石 +10",24,250,200)
    draw_text(screen,"粉寶石 +20",24,250,240)
    draw_text(screen,"藍寶石 +30",24,250,280)
    draw_text(screen,"炸彈 -15",24,250,320)
    draw_text(screen,"越接近結束時間，掉越快",22,250,380)
    draw_text(screen,f"歷史最高分：{high_score}",24,250,430)
    draw_text(screen,"按任意鍵開始",24,250,490)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                return False

def game_over(score, high_score):
    screen.blit(background_img,(0,0))
    draw_text(screen,"時間到！",48,250,180)
    draw_text(screen,f"本次分數：{score}",30,250,280)
    draw_text(screen,f"歷史最高分：{high_score}",30,250,330)
    draw_text(screen,"按 R 重新開始",24,250,430)
    draw_text(screen,"按 ESC 離開",24,250,470)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.run_right = [
            pygame.transform.scale(player_imgs[0],(95,95)),
            pygame.transform.scale(player_imgs[1],(95,95))
        ]
        self.run_left = [
            pygame.transform.scale(player_imgs[2],(95,95)),
            pygame.transform.scale(player_imgs[3],(95,95))
        ]

        for img in self.run_right + self.run_left:
            img.set_colorkey((0,0,0))

        self.way = "right"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120
        self.image = self.run_right[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = 250
        self.rect.bottom = 520
        self.speedx = 7
        self.radius = int(self.rect.width * 0.4)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        moving = False

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            self.way = "right"
            moving = True

        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            self.way = "left"
            moving = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500

        now = pygame.time.get_ticks()

        if moving:
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame >= 2:
                    self.frame = 0

                bottom = self.rect.bottom
                centerx = self.rect.centerx

                if self.way == "right":
                    self.image = self.run_right[self.frame]
                else:
                    self.image = self.run_left[self.frame]

                self.rect = self.image.get_rect()
                self.rect.centerx = centerx
                self.rect.bottom = bottom
        else:
            bottom = self.rect.bottom
            centerx = self.rect.centerx

            if self.way == "right":
                self.image = self.run_right[0]
            else:
                self.image = self.run_left[0]

            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.bottom = bottom

class Fall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.reset()

    def reset(self):
        self.type = random.choices(["gem1", "gem2", "gem3", "bomb"],[45, 28, 15, 12],k=1)[0]

        if self.type == "gem1":
            self.image = pygame.transform.scale(gem_imgs[0],(42,42))
            self.score = 10
            self.speed = 3
        elif self.type == "gem2":
            self.image = pygame.transform.scale(gem_imgs[1],(48,48))
            self.score = 20
            self.speed = 4
        elif self.type == "gem3":
            self.image = pygame.transform.scale(gem_imgs[2],(54,54))
            self.score = 30
            self.speed = 5
        else:
            self.image = pygame.transform.scale(bomb_img,(46,46))
            self.score = -15
            self.speed = 4

        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,500 - self.rect.width)
        self.rect.y = random.randrange(-150,-40)
        self.radius = int(self.rect.width * 0.4)

    def update(self,degree):
        speed_extra = degree * 5
        self.rect.y += self.speed + speed_extra

        if self.rect.top > 600:
            self.reset()

def draw_information(score,high_score,time_left):
    draw_text(screen,f"分數：{score}",20,60,10)
    draw_text(screen,f"歷史分數：{high_score}",20,410,10)
    draw_text(screen,f"時間：{time_left}",20,250,10)

high_score = load_score()
show_init = True
running = True

while running:
    if show_init:
        close = draw_init(high_score)
        if close:
            break

        show_init = False
        all_sprites = pygame.sprite.Group()
        items = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(6):
            item = Fall()
            all_sprites.add(item)
            items.add(item)

        score = 0
        start_time = pygame.time.get_ticks()

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()
    past_seconds = (now - start_time) / 1000
    time_left = 60 - int(past_seconds)
    if time_left < 0:
        time_left = 0
    degree = past_seconds / 60
    if degree > 1:
        degree = 1
    player.update()
    for item in items:
        item.update(degree)
    hits = pygame.sprite.spritecollide(player,items,False,pygame.sprite.collide_circle)
    for hit in hits:
        score += hit.score
        hit.reset()

    if score > high_score:
        high_score = score

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_information(score,high_score,time_left)
    pygame.display.update()

    if past_seconds >= 60:
        save_score(high_score)
        result = game_over(score,high_score)

        if result == "quit":
            running = False
        elif result == "restart":
            show_init = True

pygame.quit()