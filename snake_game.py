import pygame
import time
import random
import os

pygame.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

dis = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
dis_width, dis_height = pygame.display.get_surface().get_size()

pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 25

custom_font = pygame.font.Font("F:/Games_Menu_School_project/Menu/assets/font.ttf", 25)

game_over_sound = pygame.mixer.Sound("F:/Games_Menu_School_project/Menu/assets/snake/audio/gameover.mp3")
eat_sound = pygame.mixer.Sound("F:/Games_Menu_School_project/Menu/assets/snake/audio/eat.mp3")

pygame.mixer.music.load("F:/Games_Menu_School_project/Menu/assets/snake/audio/backsound.mp3")
pygame.mixer.music.play(-1)

background_img = pygame.image.load("F:/Games_Menu_School_project/Menu/assets/snake/background.jpg")
snake_head_img = pygame.transform.scale(pygame.image.load("F:/Games_Menu_School_project/Menu/assets/snake/Head.png"), (snake_block, snake_block))
snake_body_img = pygame.transform.scale(pygame.image.load("F:/Games_Menu_School_project/Menu/assets/snake/Body.png"), (snake_block, snake_block))
food_img = pygame.transform.scale(pygame.image.load("F:/Games_Menu_School_project/Menu/assets/snake/Food.png"), (snake_block, snake_block))

angle = 0
global game_over_sound_played
game_over_sound_played = False

def Your_score(score):
    value = custom_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [(dis_width - value.get_width()) // 2, 10])

def message(msg, color):
    mesg = custom_font.render(msg, True, color)
    dis.blit(mesg, [(dis_width - mesg.get_width()) // 2, (dis_height - mesg.get_height()) // 2])

def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == 0:
            dis.blit(snake_head_img, (x[0], x[1]))
        else:
            dis.blit(snake_body_img, (x[0], x[1]))

def spawn_food():
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    return foodx, foody


score_file_path = "highest_score.txt"
highest_score = 0


def load_highest_score():
    global highest_score
    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as file:
            highest_score = int(file.read())

def save_highest_score():
    with open(score_file_path, 'w') as file:
        file.write(str(highest_score))


load_highest_score()


def show_score(score, record):
    score_text = custom_font.render(f"Score: {score} Record: {record}", True, yellow)
    dis.blit(score_text, [10, 10])

def gameLoop():
    global game_over
    global game_over_sound_played
    global highest_score
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foods = [spawn_food() for _ in range(5)]

    while not game_over:
        while game_close == True:
            dis.blit(background_img, (0, 0))

            if Length_of_snake - 1 > highest_score:
                highest_score = Length_of_snake - 1
                # Зберігаємо рекорд при досягненні нового рекорду
                save_highest_score()

            message(f"You lose! Your Score: {Length_of_snake - 1} Highest Score: {highest_score}", red)

            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_over_sound_played = False
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.blit(background_img, (0, 0))

        for food in foods:
            dis.blit(food_img, (food[0], food[1]))

        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1, highest_score)
        pygame.display.update()

        for food in foods:
            if x1 == food[0] and y1 == food[1]:
                foods.remove(food)
                foods.append(spawn_food())
                Length_of_snake += 1
                eat_sound.play()

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_List.insert(0, snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[Length_of_snake:]

        for x in snake_List[1:]:
            if x == snake_Head:
                game_close = True

        clock.tick(snake_speed)

    pygame.mixer.music.stop()
    pygame.quit()
    save_highest_score()
    quit()
    
load_highest_score()
gameLoop()