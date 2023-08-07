# Import necessary libraries
from utils.config import *
import os
import random
from src.NN import Agent, nn_layers
import numpy as np
import pygame

# Initialize the pygame library
pygame.init()

# Initialize the game window
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino Runner")  # Set window title

# Load and set the game icon
Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

# Load various game assets
RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR = (0, 0, 0)


class Dinosaur:
    Y_POS = 310
    Y_POS_DUCK = 340

    def __init__(self, agent: Agent = None):
        # Initialize the dinosaur's attributes
        self.X_POS = int(20 + 80*random.random())
        if agent is None:
            self.agent = Agent()
        else:
            self.agent = agent
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_time = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, obstacles):
        # Update the dinosaur's behavior based on the agent's predictions
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        actions = [0, 0]
        if len(obstacles) > 0:
            # Prepare input data for the agent's prediction
            data = [obstacles[0].rect.x, obstacles[0].rect.y,
                    obstacles[0].rect.height, obstacles[0].rect.width, self.dino_rect.x, self.dino_rect.y, game_speed]
            data = np.asarray(data)
            actions = self.agent.predict(data)

        # Update the dinosaur's behavior based on the predicted actions
        if (actions[0] == 1) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif (actions[1] == 1):
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.jump_time = 0
        elif (sum(actions) == 0 or sum(actions) == 2) and not self.dino_jump:
            # If no specific action is predicted or both actions are predicted, run
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        return actions

    def duck(self):
        # Update the dinosaur's image and position when ducking
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        # Update the dinosaur's image and position when running
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        # Define a jump function and update the dinosaur's image and position during the jump
        def f(x: float):
            return -x*(x-1)*94*4*2
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y = self.Y_POS - f(self.jump_time)
            self.jump_time += 0.05
        if self.jump_time > 1.1:
            self.jump_time = 0
            self.dino_jump = False
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        # Draw the dinosaur's current image on the screen
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        # Initialize cloud's attributes
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        # Update cloud's position based on game speed
        self.x -= game_speed
        if self.x < -self.width:
            # Reset cloud's position if it goes off-screen
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        # Draw the cloud on the screen
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        # Initialize obstacle's attributes
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        # Update obstacle's position based on game speed
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove obstacle from list if it goes off-screen
            obstacles.pop()

    def draw(self, SCREEN):
        # Draw the obstacle on the screen
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        # Initialize small cactus obstacle
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        # Initialize large cactus obstacle
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [200, 250, 290, 320]

    def __init__(self, image):
        # Initialize bird obstacle
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        # Draw the bird animation frames on the screen
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Network:
    font = pygame.font.Font("freesansbold.ttf", 12)

    def __init__(self, sequence, x=500, y_center=140) -> None:
        self.sequence = sequence
        self.x = x
        self.y_center = y_center

    def draw(self, SCREEN, actions):
        # Draw a Neuronal Network from a sequence of chromosome
        inputs = ["X (obstacle)", "Y (obstacle)",
                  "Height (obstacle)", "Width(obstacle)",
                  "X (player)", "Y (player)", "Velocity"]
        # Draw the layers of the NN
        color = (100, 100, 100)
        active_color = (0, 255, 0)
        color_line = (0, 255, 0)
        # This function calculate the position on the SCREEN for each Neuron

        def get_coordenates(layer: int, index: int) -> tuple:
            x = self.x + layer*100
            y = self.y_center - nn_layers[layer] * \
                35//2 + 35*index  # A line center on 140
            return (x, y)

        # Draw the connections
        for gen in self.sequence:
            code = gen.get_code()
            pygame.draw.line(SCREEN, color_line,
                             get_coordenates(code[0], code[1]), get_coordenates(code[0]+1, code[2]), 5)

        # Draw the circles
        for j, layers in enumerate(nn_layers[:-1]):
            for i in range(layers):
                pygame.draw.circle(
                    SCREEN, color, get_coordenates(j, i), 12, 12)

        # Draw the last neurons
        if actions[0] == 1:
            pygame.draw.circle(
                SCREEN, active_color, get_coordenates(len(nn_layers)-1, 0), 12, 12)
        else:
            pygame.draw.circle(
                SCREEN, color, get_coordenates(len(nn_layers)-1, 0), 12, 12)
        if actions[1] == 1:
            pygame.draw.circle(
                SCREEN, active_color, get_coordenates(len(nn_layers)-1, 1), 12, 12)
        else:
            pygame.draw.circle(
                SCREEN, color, get_coordenates(len(nn_layers)-1, 1), 12, 12)

        # Write the inputs name
        for i, input in enumerate(inputs):
            text = self.font.render(input, True, FONT_COLOR)
            textRect = text.get_rect()
            (_, textRect.y) = get_coordenates(0, i)
            textRect.x = self.x - 120
            SCREEN.blit(text, textRect)


def main(players, generation):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    death_players = []
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    pause = False

    network = Network(players[0].agent.chromosome.get_sequence())

    # Update the score and game speed
    def description(generation, alive_players):
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        with open("./score.txt", "r+") as f:
            score_ints = [int(x) for x in f.read().split()]
            highscore = max(score_ints)
            if points > highscore:
                highscore = points
                f.write(str(highscore)+"\n")

        texts = [f"High Score: {highscore}", f"Current score: {points}",
                 f"Alive count: {alive_players}", f"Generation: {generation}"]

        for i, text in enumerate(texts):
            text = font.render(text, True, FONT_COLOR)
            textRect = text.get_rect()
            textRect.center = (900, 40 + i*30)
            SCREEN.blit(text, textRect)

    # Update the background's scrolling
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Unpause the game
    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    # Pause the game and display pause message
    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render(
            "Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        SCREEN.fill((255, 255, 255))

        # Generate new obstacles if no obstacles are present
        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 2)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # Update and draw players
        for player in players:
            player.draw(SCREEN)
            actions = player.update(obstacles)

        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            # Check collision between players and obstacles
            for player in players:
                if player.dino_rect.colliderect(obstacle.rect):
                    player.agent.score = points
                    death_players.append(player)
                    players.remove(player)
                    if len(players) == 0:
                        pygame.time.delay(1000)
                        return death_players

        # Update and draw background
        background()

        # Update and draw cloud
        cloud.draw(SCREEN)
        cloud.update()

        # Draw the Neuronal Network
        network = Network(players[-1].agent.chromosome.get_sequence())
        network.draw(SCREEN, actions)

        # Update score and manage frame rate
        description(generation, len(players))
        clock.tick(30)
        pygame.display.update()
