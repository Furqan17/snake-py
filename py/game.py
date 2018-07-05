import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lighter_blue = (100, 100, 255)

display_width = 800
display_height = 600


game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game - v1')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snake_head.png')
apple_img = pygame.image.load('apple.png')

block_size = 10
apple_thickness = 20


clock = pygame.time.Clock()
FPS = 30

direction = 'right'


small_font = pygame.font.SysFont('arial', 20)
medium_font = pygame.font.SysFont('arial', 30)
large_font = pygame.font.SysFont('arial', 40)

def game_intro():
    '''intro screen'''
    
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
                    
        game_display.fill(black)
        message_to_screen('Snake Game', white, -150,'large')
        message_to_screen('press "Space" to play or "Q" to quit', white, 100)
        pygame.display.update()
        clock.tick(15)
        
        

def snake(block_size, snake_list):

    if direction == 'right':
        head = pygame.transform.rotate(img, 270)

    if direction == 'left':
        head = pygame.transform.rotate(img, 90)

    if direction == 'up':
        head = img

    if direction == 'down':
        head = pygame.transform.rotate(img, 180)
    
    game_display.blit(head, (snake_list[-1][0], snake_list[-1][1]))
    
    for coord in snake_list[:-1]:
        game_display.fill(green, rect = [coord[0], coord[1], block_size, block_size])

def text_objects(text, color, size):
    '''Creates the surface for the text or something'''
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'medium':
        text_surface = medium_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()
    

def message_to_screen(msg: str, color, y_displace = 0, size = 'small') -> None:
    '''Return a message to the screen aligning with the
    following events
    '''
##    screen_text = font.render(msg, True, color)
##    game_display.blit(screen_text, [display_width / 2, display_height / 2])
    text_surface, text_rectangle = text_objects(msg, color, size)
    text_rectangle.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surface, text_rectangle)
    
def game_loop():
    global direction

    direction = 'right'
    game_exit = False
    game_over = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    random_apple_x = random.randrange(0, display_width - apple_thickness, 10)
    random_apple_y = random.randrange(0, display_height - apple_thickness, 10)
    
    while not game_exit:

        while game_over == True:
            game_display.fill(black)
            message_to_screen('Game Over', red, -50, size = 'large')
            message_to_screen('press "Space" to play again, or press "Q" to quit',
                              white, 50, size = 'medium')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_SPACE:
                        game_loop()
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                if event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                if event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.fill(black)

        
        #game_display.fill(red, rect = [random_apple_x, random_apple_y, block_size, block_size])

        game_display.blit(apple_img, (random_apple_x, random_apple_y))
        
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        if snake_head in snake_list[:-1]:
            game_over = True
            
        snake(block_size, snake_list)
        
        pygame.display.update()

        if lead_x == random_apple_x and lead_y == random_apple_y:
            random_apple_x = random.randrange(0, display_width - apple_thickness, 10)
            random_apple_y = random.randrange(0, display_height - apple_thickness, 10)
            snake_length += 1
 
            

##        if lead_x >= random_apple_x and lead_x <= random_apple_x + apple_thickness - block_size:
##            if lead_y >= random_apple_x and lead_x <= random_apple_x + apple_thickness - block_size:
##                random_apple_x = random.randrange(0, display_width - block_size, 10)
##                random_apple_y = random.randrange(0, display_height - block_size, 10)
##                snake_length += 1
                
            
            
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
game_loop()
