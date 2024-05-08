import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Colors
White = (217, 232, 227)
Blue = (0, 31, 77)

# Game window
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zen Pong")

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Square size
SQUARE_SIZE = 50

# Number of squares
numSquaresX = width // SQUARE_SIZE
numSquaresY = height // SQUARE_SIZE

# Create squares grid
squares = [[White if i < numSquaresX // 2 else Blue for j in range(numSquaresY)] for i in range(numSquaresX)]

# Ball properties
x1, y1 = width // 4, height // 2
dx1, dy1 = 5, -5

x2, y2 = (width // 4) * 3, height // 2
dx2, dy2 = -5, 5

iteration = 0

# Draw the ball
def draw_ball(x, y, color):
    pygame.draw.circle(screen, color, (int(x), int(y)), SQUARE_SIZE // 2)

# Draw squares
def draw_squares():
    for i in range(numSquaresX):
        for j in range(numSquaresY):
            pygame.draw.rect(screen, squares[i][j], (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Update squares and handle bouncing
def update_square_and_bounce(x, y, dx, dy, color):
    updated_dx, updated_dy = dx, dy

    # Check multiple points around the ball's circumference
    angles = [i * math.pi / 180 for i in range(0, 360, 45)]  # Use degrees with a step of 45

    for angle in angles:
        check_x = x + math.cos(angle) * (SQUARE_SIZE / 2)
        check_y = y + math.sin(angle) * (SQUARE_SIZE / 2)

        i = int(check_x // SQUARE_SIZE)
        j = int(check_y // SQUARE_SIZE)

        if 0 <= i < numSquaresX and 0 <= j < numSquaresY:
            if squares[i][j] != color:
                squares[i][j] = color

                # Determine bounce direction based on the angle
                if abs(math.cos(angle)) > abs(math.sin(angle)):
                    updated_dx = -updated_dx
                else:
                    updated_dy = -updated_dy

                # Add some randomness to the bounce
                updated_dx += random.uniform(-0.25, 0.25)
                updated_dy += random.uniform(-0.25, 0.25)

    return updated_dx, updated_dy

"""# Function to update the score element
def update_score_element():
    day_score = sum(row.count(MysticMint) for row in squares)
    night_score = sum(row.count(Blue) for row in squares)
    score_text = f"day {day_score} | night {night_score}"
    font = pygame.font.Font(None, 36)
    score_surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(score_surface, (20, 30))"""

# Function to check boundary collision
def check_boundary_collision(x, y, dx, dy):
    if x + dx > width - SQUARE_SIZE / 2 or x + dx < SQUARE_SIZE / 2:
        dx = -dx
    if y + dy > height - SQUARE_SIZE / 2 or y + dy < SQUARE_SIZE / 2:
        dy = -dy
    return dx, dy

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(White)

    # Draw squares
    draw_squares()

    # Draw and update ball 1
    draw_ball(x1, y1, Blue)
    dx1, dy1 = update_square_and_bounce(x1, y1, dx1, dy1, White)
    dx1, dy1 = check_boundary_collision(x1, y1, dx1, dy1)

    # Draw and update ball 2
    draw_ball(x2, y2, White)
    dx2, dy2 = update_square_and_bounce(x2, y2, dx2, dy2, Blue)
    dx2, dy2 = check_boundary_collision(x2, y2, dx2, dy2)

    # Update positions
    x1 += dx1
    y1 += dy1
    x2 += dx2
    y2 += dy2

    iteration += 1
    if iteration % 1000 == 0:
        print("iteration", iteration)

    """# Update score element
    update_score_element()"""

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
