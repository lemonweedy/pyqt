import pygame
import sys
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Game")
last_time = pygame.time.get_ticks()
time_limit = 5 * 1000
time_up = False  

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 60)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return num1, num2

def generate_addition_question():
    num1, num2 = generate_question()
    return num1, num2, num1 + num2

def generate_subtraction_question():
    num1, num2 = generate_question()
    return max(num1, num2), min(num1, num2), abs(num1 - num2)

def generate_multiplication_question():
    num1, num2 = generate_question()
    return num1, num2, num1 * num2

def generate_division_question():
    num1, num2 = generate_question()
    while num1 % num2 != 0:
        num1, num2 = generate_question()
    return num1, num2, num1 // num2

def game_over_screen(score, high_score):
    screen.fill(WHITE)
    draw_text("Game Over", title_font, RED, screen_width // 2, screen_height // 4)
    draw_text(f"Your Score: {score}", button_font, BLUE, screen_width // 2, screen_height // 2)
    draw_text(f"High Score: {high_score}", button_font, BLUE, screen_width // 2, screen_height // 2 + 50)
    draw_text("Click to Play Again", button_font, GREEN, screen_width // 2, screen_height // 2 + 100)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    game_running = False
    player_answer = ""
    correct_answer = 0
    new_question = True
    score = 0
    high_score = 0
    timer = 5 * 1000
    last_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - last_time
        remaining_time = max(0, (time_limit - elapsed_time) // 1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_running:
                    if screen_width // 2 - 100 <= event.pos[0] <= screen_width // 2 + 100:
                        if screen_height // 2 <= event.pos[1] <= screen_height // 2 + 50:
                            game_running = True
                            new_question = True
                            question_type = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
                            if question_type == 'addition':
                                correct_answer = generate_addition_question()
                                question_text = f"{correct_answer[0]} + {correct_answer[1]} = ?"
                            elif question_type == 'subtraction':
                                correct_answer = generate_subtraction_question()
                                question_text = f"{correct_answer[0]} - {correct_answer[1]} = ?"
                            elif question_type == 'multiplication':
                                correct_answer = generate_multiplication_question()
                                question_text = f"{correct_answer[0]} * {correct_answer[1]} = ?"
                            else:
                                correct_answer = generate_division_question()
                                question_text = f"{correct_answer[0]} / {correct_answer[1]} = ?"
                            
                        elif screen_height // 2 + 70 <= event.pos[1] <= screen_height // 2 + 120:
                            pygame.quit()
                            sys.exit()

            if event.type == pygame.KEYDOWN:  
                if game_running and event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                                                  pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    player_answer += event.unicode
                elif game_running and event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]
                elif game_running and event.key == pygame.K_RETURN:
                    if player_answer and int(player_answer) == correct_answer[2]:
                        new_question = True
                        player_answer = ""
                        score += 1
                        if score > high_score:
                            high_score = score
                        last_time = current_time
                        
                    elif not player_answer:
                        player_answer = ""
                    else:
                        game_running = False
                        game_over_screen(score, high_score)
                        player_answer = ""

        if game_running and elapsed_time >= time_limit:
            game_running = False
            
            

        if not game_running:
            if time_up:
                game_over_screen(score, high_score)
            else:
                draw_text("Math Game", title_font, BLUE, screen_width // 2, screen_height // 4)
                pygame.draw.rect(screen, GREEN, (screen_width // 2 - 100, screen_height // 2, 200, 50))
                draw_text("Start Game", button_font, WHITE, screen_width // 2, screen_height // 2 + 25)
                pygame.draw.rect(screen, RED, (screen_width // 2 - 100, screen_height // 2 + 70, 200, 50))
                draw_text("Quit", button_font, WHITE, screen_width // 2, screen_height // 2 + 95)
                pygame.display.flip()

        
        if game_running and elapsed_time >= timer:
            game_running = False
            game_over_screen(score, high_score)
            player_answer = ""

        screen.fill(WHITE)

        if not game_running:
            
            draw_text("Math Game", title_font, BLUE, screen_width // 2, screen_height // 4)
            pygame.draw.rect(screen, GREEN, (screen_width // 2 - 100, screen_height // 2, 200, 50))
            draw_text("Start Game", button_font, WHITE, screen_width // 2, screen_height // 2 + 25)
            pygame.draw.rect(screen, RED, (screen_width // 2 - 100, screen_height // 2 + 70, 200, 50))
            draw_text("Quit", button_font, WHITE, screen_width // 2, screen_height // 2 + 95)
            pygame.display.flip()
            if event.type == pygame.KEYDOWN:

                if game_running and event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                                                  pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    player_answer += event.unicode
                elif game_running and event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]
                elif game_running and event.key == pygame.K_RETURN:
                    if player_answer and int(player_answer) == correct_answer[2]:
                        new_question = True
                        player_answer = ""
                        score += 1
                        if score > high_score:
                            high_score = score
                        last_time = current_time
                    elif not player_answer:
                        player_answer = ""
                    else:
                        game_running = False
                        game_over_screen(score, high_score)
                        player_answer = ""

        if game_running and elapsed_time >= timer:
            game_running = False
            game_over_screen(score, high_score)
            player_answer = ""

        
        screen.fill(WHITE)

        if not game_running:
            
            draw_text("Math Game", title_font, BLUE, screen_width // 2, screen_height // 4)

            
            pygame.draw.rect(screen, GREEN, (screen_width // 2 - 100, screen_height // 2, 200, 50))
            draw_text("Start Game", button_font, WHITE, screen_width // 2, screen_height // 2 + 25)

            
            pygame.draw.rect(screen, RED, (screen_width // 2 - 100, screen_height // 2 + 70, 200, 50))
            draw_text("Quit", button_font, WHITE, screen_width // 2, screen_height // 2 + 95)
        else:
            if new_question:
                
                question_type = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
                if question_type == 'addition':
                    correct_answer = generate_addition_question()
                    question_text = f"{correct_answer[0]} + {correct_answer[1]} = ?"
                elif question_type == 'subtraction':
                    correct_answer = generate_subtraction_question()
                    question_text = f"{correct_answer[0]} - {correct_answer[1]} = ?"
                elif question_type == 'multiplication':
                    correct_answer = generate_multiplication_question()
                    question_text = f"{correct_answer[0]} * {correct_answer[1]} = ?"
                else:
                    correct_answer = generate_division_question()
                    question_text = f"{correct_answer[0]} / {correct_answer[1]} = ?"
                new_question = False

        
            draw_text(question_text, text_font, BLUE, screen_width // 2, screen_height // 4)

            
            draw_text(player_answer, text_font, BLUE, screen_width // 2, screen_height // 2)

            draw_text(f"Time Left: {remaining_time}", button_font, BLACK, screen_width // 2, 50)
   
        pygame.display.flip()

if __name__ == "__main__":
    main()