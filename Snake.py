import pygame
import random

def generate_food(snake):
    while True:
        food=(random.randint(0,GRID_WIDTH-1),
        random.randint(0,GRID_HEIGHT-1))
        
        if food not in snake:
            return food
def get_high():
    try:
        with open("highscore.txt") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0
# Initialize Pygame
pygame.init()
 
# Window settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
HEADER = 60
SCORE = 0
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + HEADER

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))
highscore=get_high()
pygame.display.set_caption("Snake Game")
font=pygame.font.SysFont(None,80)
score_font=pygame.font.SysFont(None,32)
high_score=pygame.font.SysFont(None,32)

# Colors (RGB)
BACKGROUND = (25, 25, 25)
GRID_COLOR = (45, 45, 45)

# Control the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
gameover = False
pause = False
# Snake position: (column, row)
snake = [(10, 10), (9, 10), (8, 10)]

# Food window size
food=generate_food(snake)

# Initial movement direction: right
direction = (1, 0)

clock = pygame.time.Clock()
MOVE_DELAY = 120
last_move_time = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not gameover:
                pause = not pause
            elif event.key == pygame.K_r and gameover:
                snake = [(10, 10), (9, 10), (8, 10)]
                food=generate_food(snake)
                (SCORE,gameover,direction)=(0,False,(1,0))
                last_move_time=pygame.time.get_ticks()
            elif (not pause) and (not gameover):
                if event.key == pygame.K_UP and direction != (0,1):
                    direction = (0,-1)
                elif event.key == pygame.K_DOWN and direction != (0,-1):
                    direction = (0,1)
                elif event.key == pygame.K_LEFT and direction != (1,0):
                    direction = (-1,0)
                elif event.key == pygame.K_RIGHT and direction != (-1,0):
                    direction = (1,0)
            

    # Draw the background
    screen.fill(BACKGROUND)
    
    for x, y in snake:
        pygame.draw.rect(
        screen,
        (0, 220, 90),
        (x * CELL_SIZE, y * CELL_SIZE + HEADER,
         CELL_SIZE, CELL_SIZE))

    # Draw vertical grid lines
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(
            screen, GRID_COLOR,
            (x, HEADER), (x, SCREEN_HEIGHT))

    # Draw horizontal grid lines
    for y in range(HEADER, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(
            screen, GRID_COLOR,
            (0, y), (SCREEN_WIDTH, y))
        
    # Food spawn point
    food_rect=pygame.Rect(
        food[0]*CELL_SIZE,
        food[1]*CELL_SIZE + HEADER,
        CELL_SIZE,
        CELL_SIZE)
    pygame.draw.rect(screen,(255,60,60),food_rect)
    
    # Movement of the Snake
    current_time = pygame.time.get_ticks()

    if (not gameover) and (not pause) and (current_time - last_move_time >= MOVE_DELAY):
        head_x, head_y = snake[0]

        new_head = (
        head_x + direction[0],
        head_y + direction[1])

        new_head=(
            new_head[0]%30,
            new_head[1]%30)

        eating = new_head == food
        
        if eating:
            collision_body=snake
        else:
            collision_body=snake[:-1]
            
        if new_head in collision_body:
            gameover=True
        else:
            snake.insert(0, new_head)
            if eating:
                SCORE+=10
                food=generate_food(snake)
            else:
                snake.pop()
        
        last_move_time = current_time
    score_text=score_font.render(f"SCORE:\n  {SCORE}",True,(255,255,255))
    screen.blit(score_text,(10,10))
    high_text=high_score.render(f"HIGH SCORE:\n        {highscore}",True,(255,255,255))
    screen.blit(high_text,(440,10))
    if gameover:
        text=font.render("GAME OVER!!",True,(255,60,60))
        text_rect=text.get_rect(
            center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(text,text_rect)
        if SCORE > highscore:
            highscore = SCORE
    elif pause:
        text=font.render("PAUSED",True,(255,60,60))
        text_rect=text.get_rect(
            center=(SCREEN_WIDTH//2,(SCREEN_HEIGHT+HEADER)//2))
        screen.blit(text,text_rect)
    # Display the frame
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
with open("highscore.txt","w") as wrt:
    wrt.write(str(highscore))
# Shut down Pygame
pygame.quit()
