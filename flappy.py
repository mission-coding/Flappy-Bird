import pygame
import sys
import random

pygame.init()

# game window
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird by Vivek")

# images
background_image = pygame.image.load("gallery/sprites/background.png").convert_alpha()
homescreen = pygame.image.load("gallery/sprites/home.png").convert_alpha()
homescreen = pygame.transform.scale(homescreen, (screen_width, screen_height))
gameover = pygame.image.load("gallery/sprites/over.png").convert_alpha()
gameover = pygame.transform.scale(gameover, (screen_width, screen_height))
base1_image = pygame.image.load("gallery/sprites/base.png").convert_alpha()
base2_image = pygame.image.load("gallery/sprites/base.png").convert_alpha()
bird_image = [
    pygame.image.load("gallery/sprites/bird_up.png").convert_alpha(),
    pygame.image.load("gallery/sprites/bird_down.png").convert_alpha(),
]

# sounds
die = pygame.mixer.Sound('gallery/audio/die.wav')
hit = pygame.mixer.Sound('gallery/audio/hit.wav')
point = pygame.mixer.Sound('gallery/audio/point.wav')
swoosh = pygame.mixer.Sound('gallery/audio/swoosh.wav')
wing = pygame.mixer.Sound('gallery/audio/wing.wav')

def welcome():
    run = True
    bird_x = 45
    bird_y = 150
    base_height = 112
    base_speed = 6
    base1_x = 0
    base2_x = screen_width
    base_y = screen_height - base_height
    clock = pygame.time.Clock()
    fps = 30
    fly_count = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game_loop()
        # moving base
        base1_x -= base_speed
        base2_x -= base_speed

        if base1_x <= -screen_width:
            base1_x = screen_width
        if base2_x <= -screen_width:
            base2_x = screen_width

        screen.blit(background_image, (0, 0))
        screen.blit(base1_image, (base1_x, base_y))  # base1
        screen.blit(base2_image, (base2_x, base_y))  # base2
        # bird
        if fly_count+1 > 4:
            fly_count = 0
        screen.blit(bird_image[fly_count//2], (bird_x, bird_y))
        fly_count += 1
        screen.blit(homescreen, (0, 0))

        clock.tick(fps)
        pygame.display.update()

def game_loop():
    # colors
    black = (0, 0, 0)

    def draw_text(text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, black)
        screen.blit(text_surface, (x, y))

    # variables
    base_height = 112
    bird_width = 34
    bird_height = 24
    gravity = 1
    jump_velocity = -9
    bird_x = 45
    bird_y = 150
    bird_velocity = 0
    base_speed = 7
    fly_count = 0
    base1_x = 0
    base2_x = screen_width
    base_y = screen_height - base_height
    over = False
    clock = pygame.time.Clock()
    fps = 30
    bird_moving = True
    pipes = []
    pipes_counter = 0
    score = 0

    class Pipe:
        def __init__(self):
            self.lower_pipe_image = pygame.image.load("gallery/sprites/pipe.png").convert_alpha()
            self.upper_pipe_image = pygame.transform.rotate(self.lower_pipe_image, 180)
            self.pipe_width = 52
            self.pipe_height = 320
            self.pipe_gap = 130
            self.lower_pipe_x = screen_width
            self.lower_pipe_y = random.randint(200, 350)
            self.upper_pipe_x = screen_width
            self.upper_pipe_y = self.lower_pipe_y - self.pipe_height - self.pipe_gap
            self.base_speed = 7
            self.bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            self.moving = True

        def display_pipe(self):
            screen.blit(self.lower_pipe_image, (self.lower_pipe_x, self.lower_pipe_y))
            screen.blit(self.upper_pipe_image, (self.upper_pipe_x, self.upper_pipe_y))

        def moving_pipe(self):
            if self.moving:
                self.lower_pipe_x -= base_speed
                self.upper_pipe_x -= base_speed

        def collision_with_pipe(self):
            nonlocal score
            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            self.lower_pipe_rect = pygame.Rect(self.lower_pipe_x, self.lower_pipe_y, self.pipe_width, self.pipe_height)
            self.upper_pipe_rect = pygame.Rect(self.upper_pipe_x, self.upper_pipe_y, self.pipe_width, self.pipe_height)

            if bird_rect.colliderect(self.lower_pipe_rect) or bird_rect.colliderect(self.upper_pipe_rect):
                self.moving = False
                hit.play()
                game_over()

    def game_over():
        nonlocal over
        nonlocal base_speed
        nonlocal bird_moving
        bird_moving = False
        over = True
        base_speed = 0
        screen.blit(gameover, (0, 0))
        draw_text("Score: " + str(score), 35, 90, 220)  # Display the score

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not over:
                    bird_velocity = jump_velocity
                    wing.play()
                elif event.key == pygame.K_RETURN and over:
                    game_loop()

        # Bird movement
        if bird_moving:
            bird_y += bird_velocity
            bird_velocity += gravity

        # collisions with the ground
        if bird_y >= screen_height - base_height - bird_height:
            over = True

        # collisions with pipes
        if not over:
            for pipe in pipes:
                pipe.collision_with_pipe()
                if not pipe.moving:
                    game_over()

        # Move pipes 
        if not over:
            for pipe in pipes:
                pipe.moving_pipe()
                if pipe.lower_pipe_x + pipe.pipe_width < 0:
                    pass

            # Move base
            base1_x -= base_speed
            base2_x -= base_speed

            if base1_x <= -screen_width:
                base1_x = screen_width
            if base2_x <= -screen_width:
                base2_x = screen_width

            # Generating pipes after some distance
            if pipes_counter >= 30:
                pipes.append(Pipe())
                pipes_counter = 0
            pipes_counter += 1

        # Draw everything
        screen.blit(background_image, (0, 0))
        for pipe in pipes:
            pipe.display_pipe()

        screen.blit(base1_image, (base1_x, base_y))
        screen.blit(base2_image, (base2_x, base_y))
        if fly_count+1 > 4:
            fly_count = 0

        if bird_moving:
            screen.blit(bird_image[fly_count//2], (bird_x, bird_y))
            fly_count += 1
        # screen.blit(bird_image, (bird_x, bird_y))
        if not bird_moving:
            screen.blit(bird_image[0], (bird_x, bird_y))

        if not over:
            # Increase score when passing through a pipe
            for pipe in pipes:
                if pipe.moving and pipe.lower_pipe_x + pipe.pipe_width < bird_x < pipe.lower_pipe_x + pipe.pipe_width + 10:
                    score += 1
                    # print(score)
                    point.play()
                    
            draw_text(str(score), 45, screen_width/2 - 13, 100)

        if over:
            game_over() 

        pygame.display.update()
        clock.tick(fps)

welcome()
