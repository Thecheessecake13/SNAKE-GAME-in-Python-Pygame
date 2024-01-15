import pygame
import random

pygame.init()

# current display
# creen_info = pygame.display.Info()
# screen_w = 800 #screen_info.current_w
# screen_h = 600 #screen_info.current_h

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

block_size = 30
square = block_size

# font
font = pygame.font.Font('font.ttf', block_size * 2)

# speed of game
fps = 10
clock = pygame.time.Clock()


# draw grid
def drawGrid():
    for x in range(0, 800, block_size):
        for y in range(0, 600, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)


class Snake:
    def __init__(self):
        # x and y positions of snake
        self.x = block_size
        self.y = block_size
        # snake directions
        self.xdir = 1
        self.ydir = 0
        # create body of snake that will be list of sqaures
        self.body = [pygame.Rect(self.x - block_size, self.y, block_size, block_size)]
        # head of snake runs on a different logic
        self.head = [pygame.Rect(self.x, self.y, block_size, block_size)]  # it is a list of rect
        # whether died or not
        self.dead = False

    # logic for snake movement
    def Update(self):  # for body position/instance
        # self eating and boundary crossing
        global apple
        if self.head[0].x == self.body[-1].x and self.head[0].y == self.body[-1].y:  # checking if dead or not
            self.dead = True
        if self.head[0].x not in range(0, 800) and self.head[0].y not in range(0, 600):
            self.dead = True

        # setting new score and new position
        if self.dead:
            self.x = block_size
            self.y = block_size
            self.xdir = 1
            self.ydir = 0
            self.body = [pygame.Rect(self.x - block_size, self.y, block_size, block_size)]
            self.head = [pygame.Rect(self.x, self.y, block_size, block_size)]
            self.dead = False
            apple.respawn()
            # apple = Apple()  # generate new apple instance
        # apple.Update()

        self.body.append(self.head[0])  # includes head and body together
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y

        # updating heads position
        self.head[0].x = self.head[0].x + self.xdir * block_size
        self.head[0].y = self.head[0].y + self.ydir * block_size
        self.body.remove(self.head[0])


class Apple:
    def __init__(self):
        self.respawn()  # Initial respawn of the apple

    def respawn(self):
        self.x = int(random.randint(0, 800 - block_size) / block_size) * block_size
        self.y = int(random.randint(0, 600 - block_size) / block_size) * block_size
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

        # self.x = int(random.randint(0, 800) / block_size) * block_size  # so that aplle finds the nearest block
        # self.y = int(random.randint(0, 600) / block_size) * block_size
        # rect for apple
        # self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

    def Update(self):
        pygame.draw.rect(screen, 'red', self.rect)


# drawGrid()

snake = Snake()
apple = Apple()

# initial render of the score outside game loop
screen.fill((0, 0, 0))
score_value = 0
score_render = font.render('Score: ' + str(score_value), True, 'white')
score_rect = score_render.get_rect(center=(800 / 2, 600 / 20))  # to draw a rect for screen blit

screen.blit(score_render, score_rect)
pygame.display.update()

running = True
while running:
    screen.fill((0, 0, 0))
    snake.Update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

    # draw snake head on screen
    pygame.draw.rect(screen, (69, 179, 61), snake.head[0])

    # to draw snake body using evry square by going through evry suqare
    for square in snake.body:
        # draw snake body on screen
        pygame.draw.rect(screen, (252, 186, 3), square)

    # eating mechanism
    if snake.head[0].x == apple.x and snake.head[0].y == apple.y:
        # add new square/body to snake length
        snake.body.append(pygame.Rect(square.x, square.y, block_size, block_size))
        score_value += 1
        # update the score
        score_render = font.render('Score: ' + str(score_value), True, 'white')
        apple.respawn()

    apple.Update()
    drawGrid()
    # blit score on screen
    screen.blit(score_render, score_rect)

    clock.tick(fps)

    # clock.tick(30)
    pygame.display.update()

# blit the final score outside the game loop
screen.blit(score_render, score_rect)
pygame.display.update()
