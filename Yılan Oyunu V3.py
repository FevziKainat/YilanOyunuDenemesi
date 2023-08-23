import pygame
import random

snake_speed = 12
window_color = (200, 200, 200)
snake_color = (0, 0, 0)
food_color = (223, 50, 50)
special_food_color = (50, 223, 50)
snake_start = [100, 50]
snake_positions = [[100, 50], [90, 50], [80, 50]]
food_position = [random.randrange(1, 100) * 10, random.randrange(1, 75) * 10]
score = 0
high_score = 0
direction = "RIGHT"
pygame.init()
pygame.display.set_caption('Yılan Oyunu')
window = pygame.display.set_mode((1000, 750))
fps = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
normal_food_counter = 0

def save_high_score(high_score):
    with open("C:\\Users\\HP\\Desktop\\high_score.txt", "w") as file:
        file.write(str(high_score))

def load_high_score():
    try:
        with open("C:\\Users\\kullanici_adi\\Desktop\\high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0



def draw_food(food_color):
    pygame.draw.rect(window, food_color,
                     pygame.Rect(food_position[0], food_position[1], 
                                 10, 10))

def update_direction():
    global direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "LEFT":
                direction = "RIGHT"
                # Update snake position
def update_snake():
    global snake_start
    global food_position
    global score
    global high_score
    global direction
    global normal_food_counter

    if direction == "UP":
        snake_start[1] -= 10
    elif direction == "DOWN":
        snake_start[1] += 10
    elif direction == "LEFT":
        snake_start[0] -= 10
    elif direction == "RIGHT":
        snake_start[0] += 10
    
    if snake_start[0] >= 1000:
        snake_start[0] = 0
    if snake_start[0] < 0:
        snake_start[0] = 990
    if snake_start[1] >= 750:
        snake_start[1] = 0
    if snake_start[1] < 0:
        snake_start[1] = 740
    if snake_start == food_position:
        score += 1
        normal_food_counter += 1
        food_position = [random.randrange(1, 100) * 10,
                         random.randrange(1, 75) * 10]
        snake_positions.append(list(snake_positions[-1]))
        snake_positions.insert(0, list(snake_start))
    else:
        snake_positions.insert(0, list(snake_start))
        if len(snake_positions) > score +1: 
            snake_positions.pop(-1)

    for pos in snake_positions[1:]:
        if pos == snake_start:
            # Yılan kendine çarptığında skoru güncelle ve True döndür
            if score > high_score:
                high_score = score
            return True

    # Yılan kendine çarpmadığında skoru güncelle ve False döndür
    if score > high_score:
        high_score= score
    return False


def show_score(score):
    font = pygame.font.Font(None,35)
    score_text = font.render("Skor: " + str(score), True, (0,0,0))
    window.blit(score_text,(0,0))

def show_high_score(high_score):
    font = pygame.font.Font(None,35)
    high_score_text = font.render("En Yüksek Skor: " + str(high_score), True, (0,0,0))
    window.blit(high_score_text,(700,0))

def show_timer(start_ticks):
    font = pygame.font.Font(None,35)
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 
    timer_text = font.render("Zaman: " + str(int(seconds//60)).zfill(2) + "." + str(int(seconds%60)).zfill(2), True, (0,0,0))
    text_rect = timer_text.get_rect(center=(500,50)) 
    window.blit(timer_text,text_rect)

def display_game_over():
    font = pygame.font.Font(None,50)
    game_over_text1 = font.render("Oyun Bitti", True, (0,0,0))
    game_over_text2 = font.render("Tekrar Oyna", True, (0,0,0))
    text_rect1 = game_over_text1.get_rect(center=(500,375)) 
    text_rect2 = game_over_text2.get_rect(center=(500,425)) 
    window.blit(game_over_text1,text_rect1)
    window.blit(game_over_text2,text_rect2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

def update_screen(window_color):
    window.fill(window_color)
    
def draw_snake(snake_color):
     for pos in snake_positions:
         pygame.draw.rect(window, snake_color,
                          pygame.Rect(pos[0], pos[1], 10, 10))
high_score = load_high_score()
while True:
    update_direction()
    game_over = update_snake()
    
    if game_over:
     save_high_score(high_score)
    
     restart = display_game_over()
     if restart:
            snake_start = [100, 50]
            snake_positions = [[100, 50], [90, 50], [80, 50]]
            food_position = [random.randrange(1, 100) * 10,
                             random.randrange(1, 75) * 10]
            score = 0
            direction = "RIGHT"
            start_ticks = pygame.time.get_ticks()  # Zamanlayıcıyı sıfırla
            continue
    else:
            break
    update_screen(window_color)
    draw_snake(snake_color)
    draw_food(food_color)
    
    # Skor, en yüksek skor ve zamanı ekrana yazdır
    show_score(score)
    show_high_score(high_score)
    show_timer(start_ticks)

    pygame.display.update()
    fps.tick(snake_speed)

