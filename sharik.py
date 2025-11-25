import pygame
from random import randint
import sys
import os

pygame.init()

WIDTH = 330
HEIGHT = 471
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sharik Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

fon = pygame.image.load("images/fon9 (1).jpg")
fon1 = pygame.image.load("images/fon9 (1).jpg")

block_img = pygame.image.load("images/bloooock1-Photoroom.png")
block_img2 = pygame.image.load("images/bloooock1-Photoroom.png")

shar = pygame.image.load("images/shar91-Photoroom.png")
shar_rect = shar.get_rect(center=(WIDTH // 2, 400))

bg_y = 0
time1 = 0
time2 = 0
game_state = "menu"
max_lives = 3
lives = max_lives
invuln_timer = 0
slow_timer = 0
shake_timer = 0
clock = pygame.time.Clock()

record_file = "sharik_record.txt"
if os.path.exists(record_file):
    try:
        with open(record_file, "r") as f:
            best_score = int(f.read())
    except:
        best_score = 0
else:
    best_score = 0


def create_block(offset):
    img = block_img if randint(0, 1) == 0 else block_img2
    rect = img.get_rect(center=(randint(0, WIDTH - img.get_width()), offset))
    return {"img": img, "rect": rect, "type": randint(0, 2)}


blocks = [create_block(0), create_block(-230)]
bonuses = []


def reset_game():
    global time1, time2, lives, invuln_timer, slow_timer, shake_timer, blocks, bonuses, game_state
    time1 = 0
    time2 = 0
    lives = max_lives
    invuln_timer = 0
    slow_timer = 0
    shake_timer = 0
    shar_rect.center = (WIDTH // 2, 400)
    blocks[:] = [create_block(0), create_block(-230)]
    bonuses[:] = []
    game_state = "playing"


def spawn_bonus():
    t = ["score", "slow", "shield"][randint(0, 2)]
    size = 22
    rect = pygame.Rect(randint(0, WIDTH - size), -size, size, size)
    bonuses.append({"rect": rect, "type": t})


def draw_bonus(surface, bonus, ox=0, oy=0):
    x = bonus["rect"].x + ox
    y = bonus["rect"].y + oy
    w = bonus["rect"].width
    h = bonus["rect"].height
    t = bonus["type"]

    if t == "shield":
        pygame.draw.polygon(surface, (0, 180, 0),
                            [(x + w//2, y), (x + w, y + h//3),
                             (x + 3*w//4, y + h), (x + w//4, y + h),
                             (x, y + h//3)])
        pygame.draw.polygon(surface, (255, 255, 255),
                            [(x + w//2, y), (x + w, y + h//3),
                             (x + 3*w//4, y + h), (x + w//4, y + h),
                             (x, y + h//3)], 2)

    elif t == "slow":
        cx = x + w // 2
        cy = y + h // 2
        pygame.draw.polygon(surface, (150, 220, 255),
                            [(cx, y), (x + w, cy), (cx, y + h), (x, cy)])
        pygame.draw.polygon(surface, (230, 250, 255),
                            [(cx, y), (x + w, cy), (cx, y + h), (x, cy)], 2)

    elif t == "score":
        r = w // 2
        c = (x + r, y + r)
        pygame.draw.circle(surface, (255, 215, 0), c, r)
        pygame.draw.circle(surface, (255, 255, 255), c, r, 2)


def draw_heart(surface, x, y, size=16, color=(255, 0, 0)):
    r = size // 2
    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + 3*r, y + r), r)
    pygame.draw.polygon(surface, color,
                        [(x, y + r), (x + size*2, y + r), (x + size, y + size*2)])


running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    if game_state == "menu":
        sc.fill(BLACK)
        f1 = pygame.font.SysFont("Arial", 42)
        f2 = pygame.font.SysFont("Arial", 24)

        sc.blit(f1.render("Sharik Game", True, WHITE),
                (WIDTH//2 - 110, 100))
        sc.blit(f2.render("Press SPACE to start", True, WHITE),
                (WIDTH//2 - 110, 180))
        sc.blit(f2.render(f"Best score: {best_score}", True, WHITE),
                (WIDTH//2 - 90, 220))

        if keys[pygame.K_SPACE]:
            reset_game()

    elif game_state == "playing":
        time2 += 1
        if time2 >= 30:
            time2 = 0
            time1 += 1

        if invuln_timer > 0:
            invuln_timer -= 1
        if slow_timer > 0:
            slow_timer -= 1
        if shake_timer > 0:
            shake_timer -= 1

        base_fall = 2 + time1 // 5
        fall_speed = base_fall // 2 if slow_timer > 0 else base_fall

        player_speed = min(8, 3 + time1 // 10)

        for b in blocks:
            sp = fall_speed * (1.5 if b["type"] == 1 else 0.8 if b["type"] == 2 else 1)
            b["rect"].y += int(sp)
            if b["rect"].top > HEIGHT:
                b["rect"].bottom = 0
                b["rect"].x = randint(0, WIDTH - b["rect"].width)
                b["type"] = randint(0, 2)

        if randint(1, 200) == 1:
            spawn_bonus()

        for bn in bonuses[:]:
            bn["rect"].y += max(2, fall_speed - 1)
            if bn["rect"].top > HEIGHT:
                bonuses.remove(bn)
                continue
            if shar_rect.colliderect(bn["rect"]):
                if bn["type"] == "score":
                    time1 += 5
                elif bn["type"] == "slow":
                    slow_timer = 180
                elif bn["type"] == "shield":
                    invuln_timer = 180
                bonuses.remove(bn)

        if keys[pygame.K_LEFT]:
            shar_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            shar_rect.x += player_speed

        shar_rect.x = max(0, min(WIDTH - shar_rect.width, shar_rect.x))

        for b in blocks:
            if shar_rect.colliderect(b["rect"]) and invuln_timer == 0:
                lives -= 1
                invuln_timer = 90
                shake_timer = 20
                b["rect"].bottom = 0
                b["rect"].x = randint(0, WIDTH - b["rect"].width)
                if lives <= 0:
                    game_state = "game_over"

        bg_y = (bg_y + 1) % HEIGHT

        if shake_timer > 0:
            ox = randint(-4, 4)
            oy = randint(-4, 4)
        else:
            ox = oy = 0

        sc.blit(fon, (ox, bg_y + oy))
        sc.blit(fon1, (ox, bg_y - HEIGHT + oy))

        for b in blocks:
            sc.blit(b["img"], (b["rect"].x + ox, b["rect"].y + oy))

        for bn in bonuses:
            draw_bonus(sc, bn, ox, oy)

        if not (invuln_timer > 0 and (invuln_timer // 5) % 2 == 0):
            sc.blit(shar, (shar_rect.x + ox, shar_rect.y + oy))

        if shake_timer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 70))
            sc.blit(overlay, (0, 0))

        f = pygame.font.SysFont("Arial", 20)
        sc.blit(f.render("Lives:", True, BLACK), (10, 10))

        lx = 10 + f.size("Lives:")[0] + 8
        for i in range(lives):
            draw_heart(sc, lx + i * 22, 8, size=10)

        sc.blit(f.render(f"Score: {time1}", True, BLACK),
                (WIDTH - 90, 10))

    elif game_state == "pause":
        sc.fill(BLACK)
        f = pygame.font.SysFont("Arial", 36)
        sc.blit(f.render("Game paused!", True, WHITE), (60, 120))
        sc.blit(f.render("Press W to continue", True, WHITE), (20, 170))
        if keys[pygame.K_w]:
            game_state = "playing"

    elif game_state == "game_over":
        sc.fill(BLACK)
        f = pygame.font.SysFont("Arial", 36)
        sc.blit(f.render("Game over!", True, WHITE), (70, 60))

        if time1 > best_score:
            best_score = time1
            with open(record_file, "w") as f2:
                f2.write(str(best_score))

        f2 = pygame.font.SysFont("Arial", 24)
        sc.blit(f2.render(f"Score: {time1}", True, WHITE), (110, 130))
        sc.blit(f2.render(f"Best: {best_score}", True, WHITE), (115, 170))
        sc.blit(f2.render("Press R to restart", True, WHITE), (70, 220))
        sc.blit(f2.render("Press Q to exit", True, WHITE), (80, 260))

        if keys[pygame.K_r]:
            reset_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
