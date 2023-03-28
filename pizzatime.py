import os
import pygame
import time
import random
import sys

# initialize pygame
pygame.init()

# define constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
BUTTON_SIZE = 50
BUTTON_SPEED = 5

# set up the window
flags = pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
pygame.display.set_caption("It's Pizza Time!")

# create the button
button_pos = [random.randint(0, WINDOW_WIDTH - BUTTON_SIZE), random.randint(0, WINDOW_HEIGHT - BUTTON_SIZE)]
button_color = (255, 0, 0)

# define the function to move the button
BUTTON_SPEED = 15
def move_button():
    global button_pos
    x, y = button_pos
    dx, dy = random.randint(-BUTTON_SPEED, BUTTON_SPEED), random.randint(-BUTTON_SPEED, BUTTON_SPEED)
    x += dx
    y += dy
    if x < 0:
        x = 0
    elif x > WINDOW_WIDTH - BUTTON_SIZE:
        x = WINDOW_WIDTH - BUTTON_SIZE
    if y < 0:
        y = 0
    elif y > WINDOW_HEIGHT - BUTTON_SIZE:
        y = WINDOW_HEIGHT - BUTTON_SIZE
    button_pos = [x, y]

# define the function to check if the button has been clicked
def is_button_clicked(pos):
    x, y = pos
    bx, by = button_pos
    if bx <= x <= bx + BUTTON_SIZE and by <= y <= by + BUTTON_SIZE:
        return True
    return False

# set up the timer
timer_start = time.time()
timer_length = 232 # 3 minutes and 52 seconds
timer_font = pygame.font.SysFont(None, 50)

# set up the shutdown message
shutdown_font = pygame.font.SysFont(None, 50)
shutdown_text = shutdown_font.render("Out Of Time!", True, (255, 0, 0))
shutdown_text_rect = shutdown_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# start the audio
audio_file = os.path.join(sys._MEIPASS, 'pizzatime.mp3')
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# run the game loop
running = True
while running:

    # move the button and redraw the screen
    move_button()
    window.fill((255, 255, 255))
    pygame.draw.rect(window, button_color, (button_pos[0], button_pos[1], BUTTON_SIZE, BUTTON_SIZE))

    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and is_button_clicked(pygame.mouse.get_pos()):
            running = False

    # check the timer
    time_passed = int(time.time() - timer_start)
    if time_passed >= timer_length:
        window.blit(shutdown_text, shutdown_text_rect)
        os.system("shutdown /s /t 1")
        running = False
    else:
        time_remaining = timer_length - time_passed
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        time_text = timer_font.render("{:02d}:{:02d}".format(minutes, seconds), True, (0, 0, 0))
        time_text_rect = time_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        window.blit(time_text, time_text_rect)

    # update the display
    pygame.display.update()

# clean up pygame
pygame.quit()
