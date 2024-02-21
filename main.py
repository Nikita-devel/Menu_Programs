import sys
import pygame
from button import Button
import subprocess

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)


PLAY_BACK = Button(image=None, pos=(1150, 670), 
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")


def games():
    buttons = [
        {"text": "Puissance 4", "action": lambda: subprocess.run(["python", "gamesss/connect-4-master/connect4.py"])},
        {"text": "Pong Game", "action": lambda: subprocess.run(["python", "gamesss/pong_game.py"])},
        {"text": "Snake", "action": lambda: subprocess.run(["python", "gamesss/snake_game.py"])},
        {"text": "Flappy Bird", "action": lambda: subprocess.run(["python", "gamesss/flappy.py"])},
    ]

    button_spacing = 20  
    column_spacing = 200 

    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        GAME_TEXT = get_font(45).render("This is the GAMES screen.", True, "White")
        GAME_RECT = GAME_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(GAME_TEXT, GAME_RECT)

        column1_buttons = buttons[:5]
        column2_buttons = buttons[5:]

        for i, button_info in enumerate(column1_buttons):
            button = Button(image=None, pos=(540, 200 + i * (60 + button_spacing)),
                            text_input=button_info['text'],
                            font=get_font(30),
                            base_color="Yellow",
                            hovering_color="Green")

            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GAME_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    button_info["action"]()

        for i, button_info in enumerate(column2_buttons):
            button = Button(image=None, pos=(740 + column_spacing, 200 + i * (60 + button_spacing)),
                            text_input=button_info['text'],
                            font=get_font(30),
                            base_color="Yellow",
                            hovering_color="Green")

            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GAME_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    button_info["action"]()

        PLAY_BACK.changeColor(GAME_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(GAME_MOUSE_POS):
                    return

        pygame.display.update()

def guide(game_name):
    while True:
        GUIDE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        GUIDE_TEXT = get_font(45).render(f"This is the {game_name} GUIDE screen.", True, "White")
        GUIDE_RECT = GUIDE_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(GUIDE_TEXT, GUIDE_RECT)

        PLAY_BACK.changeColor(GUIDE_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(GUIDE_MOUSE_POS):
                    return

        pygame.display.update()

def main_menu():
    buttons = [
        {"text": "GAMES", "action": games},
        {"text": "GUIDE", "action": lambda: guide("GAME")},
        {"text": "QUIT", "action": pygame.quit}
    ]

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for i, button_info in enumerate(buttons):
            button = Button(image=pygame.image.load(f"assets/{button_info['text']} Rect.png"),
                            pos=(640, 250 + i * 150),
                            text_input=button_info['text'],
                            font=get_font(75),
                            base_color="#d7fcd4",
                            hovering_color="Green")

            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(MENU_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    button_info["action"]()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main_menu()
