import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (1, 255, 0)
RED = (255, 0, 0)

# Bird settings
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_y_change = 0
gravity = 1

# Pipe settings
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(200, 400)
pipe_x = SCREEN_WIDTH
pipe_gap = 150
pipe_velocity = 4

# Game settings
clock = pygame.time.Clock()
running = True
score = 0
font = pygame.font.Font(None, 36)

# Login settings
user_authenticated = False
username = "ammar"
password = "ammar"
input_box = pygame.Rect(100, 200, 200, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
login_successful = False

# Plane selection settings
plane_selected = False
planes = ["Red", "Green", "Blue"]
selected_plane = None

def draw_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, rect)

def login_screen():
    global text, active, color, username, password, login_successful
    while not login_successful:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        username, password = text.split("ammar ")
                        login_successful = True  # For simplicity, auto-login on enter
                        text = 'ammar'
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        draw_text(screen, "Enter Username and Password:", font, BLACK, (50, 150))
        draw_text(screen, text, font, color, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def plane_selection_screen():
    global plane_selected, selected_plane
    while not plane_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_plane = "Red"
                    plane_selected = True
                elif event.key == pygame.K_2:
                    selected_plane = "Green"
                    plane_selected = True
                elif event.key == pygame.K_3:
                    selected_plane = "Blue"
                    plane_selected = True

        screen.fill(WHITE)
        draw_text(screen, "Select Your Plane:", font, BLACK, (100, 100))
        draw_text(screen, "1. Red", font, RED, (100, 200))
        draw_text(screen, "2. Green", font, GREEN, (100, 250))
        draw_text(screen, "3. Blue", font, (0, 0, 255), (100, 300))

        pygame.display.flip()
        clock.tick(30)

def main_game_loop():
    global bird_y, bird_y_change, pipe_x, PIPE_HEIGHT, score, running

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = -10

        # Gravity effect
        bird_y_change += gravity
        bird_y += bird_y_change

        # Pipe movement
        pipe_x -= pipe_velocity
        if pipe_x < -PIPE_WIDTH:
            pipe_x = SCREEN_WIDTH
            PIPE_HEIGHT = random.randint(200, 400)
            score += 1

        # Collision detection
        if bird_y < 0 or bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:
            running = False

        if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
            if bird_y < PIPE_HEIGHT or bird_y + BIRD_HEIGHT > PIPE_HEIGHT + pipe_gap:
                running = False

        # Drawing
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, [bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT])
        pygame.draw.rect(screen, GREEN, [pipe_x, 0, PIPE_WIDTH, PIPE_HEIGHT])
        pygame.draw.rect(screen, GREEN, [pipe_x, PIPE_HEIGHT + pipe_gap, PIPE_WIDTH, SCREEN_HEIGHT])

        # Score display
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

# Run the game
login_screen()
plane_selection_screen()
main_game_loop()
