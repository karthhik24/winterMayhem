import pygame
import sys
import random


pygame.init()


SCREEN_SIZE = 600
GRID_SIZE = 3
cell_size = SCREEN_SIZE // GRID_SIZE


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Winter Mayhem")  


LIGHT_BLUE = (173, 216, 230)  
LINE_COLOR = (0, 0, 0)  
TEXT_COLOR = (255, 215, 0)  
RESULT_BG_COLOR = (0, 0, 128)  
GLITTER_COLOR = (255, 215, 0)  


font = pygame.font.Font("Lobster-Regular.ttf", 50)


wreath_img = pygame.image.load("wreath.png")  
wreath_img = pygame.transform.scale(wreath_img, (cell_size - 20, cell_size - 20))

bell_img = pygame.image.load("bell.png")  
bell_img = pygame.transform.scale(bell_img, (cell_size - 20, cell_size - 20))


game_bgm = "winter-wonderland-sleigh-ride-christmas-instrumental-264894.mp3" 
win_bgm = "brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3"  
token_bgm = "coinhit.mp3" 
draw_bgm = "080047_lose_funny_retro_video-game-80925.mp3"  


pygame.mixer.music.load(game_bgm) 
pygame.mixer.music.set_volume(0.1)  
pygame.mixer.music.play(-1) 


token_sound = pygame.mixer.Sound(token_bgm)
draw_sound = pygame.mixer.Sound(draw_bgm)


board = [' ' for _ in range(9)]
current_player = 'X'


class GlitterLight:
    def __init__(self):
        self.x = random.randint(0, SCREEN_SIZE)
        self.y = random.randint(0, SCREEN_SIZE)
        self.size = random.randint(2, 4)  
        self.alpha = random.randint(150, 255)  
        self.fade_direction = random.choice([1, -1])  

    def fade(self):
        if self.fade_direction == 1: 
            self.alpha += 3
            if self.alpha >= 255:
                self.fade_direction = -1  
        else:  
            self.alpha -= 3
            if self.alpha <= 150:
                self.fade_direction = 1  

    def draw(self):
        glitter_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        pygame.draw.circle(glitter_surface, (GLITTER_COLOR[0], GLITTER_COLOR[1], GLITTER_COLOR[2]), (self.size, self.size), self.size)
        
        glitter_surface.set_alpha(self.alpha)  
        screen.blit(glitter_surface, (self.x - self.size, self.y - self.size))


def draw_background():
    screen.fill(LIGHT_BLUE)  


def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * cell_size, 0), (i * cell_size, SCREEN_SIZE), 5)
        pygame.draw.line(screen, LINE_COLOR, (0, i * cell_size), (SCREEN_SIZE, i * cell_size), 5)


def draw_marks():
    for i in range(9):
        row = i // 3
        col = i % 3
        if board[i] == 'X':
            screen.blit(wreath_img, (col * cell_size + 10, row * cell_size + 10))
        elif board[i] == 'O':
            screen.blit(bell_img, (col * cell_size + 10, row * cell_size + 10))


def check_winner():
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),  
                            (0, 4, 8), (2, 4, 6)]  
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]  
    return None


def check_draw():
    return ' ' not in board


def result_screen(result, winner=None):
    
    pygame.mixer.music.stop()

   
    if result == "Winner":
        pygame.mixer.music.load(win_bgm)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()
    elif result == "Draw":
        draw_sound.play()

   
    if result == "Winner" and winner == 'X':
        winner_image = pygame.image.load("wreathwins.webp")
    elif result == "Winner" and winner == 'O':
        winner_image = pygame.image.load("bellwins.webp")
    elif result == "Draw":
        winner_image = pygame.image.load("Draw_wins.webp")

    winner_image = pygame.transform.scale(winner_image, (SCREEN_SIZE, SCREEN_SIZE))

    result_running = True
    while result_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(winner_image, (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)
        result_running = False

    pygame.mixer.music.stop()
    reset_game()


def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    pygame.mixer.music.load(game_bgm)
    pygame.mixer.music.play(-1)

# Main game loop
def main():
    global current_player
    game_over = False
    while True:
        draw_background()
        draw_grid()
        draw_marks()

        if game_over:
            winner = check_winner()
            if winner:
                result_screen("Winner", winner)
                game_over = False
            elif check_draw():
                result_screen("Draw")
                game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // cell_size, pos[0] // cell_size
                index = row * 3 + col
                if board[index] == ' ':
                    board[index] = current_player
                    current_player = 'O' if current_player == 'X' else 'X'
                    token_sound.play()
                    if check_winner() or check_draw():
                        game_over = True

        pygame.display.update()


if __name__ == "__main__":
    main()
