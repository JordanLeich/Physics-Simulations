import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800  # Dimensions for the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
COLORS = [
    (255, 0, 0),     # Red
    (0, 0, 255),     # Blue
    (0, 255, 0),     # Green
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (128, 0, 128),   # Purple
    (0, 255, 255),   # Cyan
    (255, 192, 203), # Pink
]

# Circle properties
CIRCLE_RADIUS = 400  # Increased radius
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)

# Ball properties
BALL_RADIUS = 20  # Initial radius for balls
MAX_RADIUS = CIRCLE_RADIUS  # Maximum radius a ball can grow
BALL_SPEED_MULTIPLIER = 1.1
SPEED_INCREMENT = 2

# Ball class to encapsulate properties and behaviors
class Ball:
    def __init__(self, color, pos, speed):
        self.color = color
        self.pos = list(pos)
        self.speed = list(speed)
        self.radius = BALL_RADIUS

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def check_collision(self):
        dist_from_center = math.sqrt((self.pos[0] - CIRCLE_CENTER[0]) ** 2 + (self.pos[1] - CIRCLE_CENTER[1]) ** 2)

        # Check for collision with the circle border
        if dist_from_center + self.radius >= CIRCLE_RADIUS:
            # Calculate the normal vector at the point of collision
            normal_angle = math.atan2(self.pos[1] - CIRCLE_CENTER[1], self.pos[0] - CIRCLE_CENTER[0])

            # Reverse ball direction and increase speed
            self.speed[0] = -self.speed[0] * BALL_SPEED_MULTIPLIER
            self.speed[1] = -self.speed[1] * BALL_SPEED_MULTIPLIER

            # Update ball position to the edge of the circle
            self.pos[0] = CIRCLE_CENTER[0] + (CIRCLE_RADIUS - self.radius) * math.cos(normal_angle)
            self.pos[1] = CIRCLE_CENTER[1] + (CIRCLE_RADIUS - self.radius) * math.sin(normal_angle)

            # Increase ball size
            self.radius += SPEED_INCREMENT

# Create a list of balls with random properties
def create_ball():
    return Ball(
        color=random.choice(COLORS),
        pos=[random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS), random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)],
        speed=[random.choice([-3, 3]) * random.uniform(1, 2), random.choice([-3, 3]) * random.uniform(1, 2)]
    )

balls = [create_ball() for _ in range(random.randint(3, 10))]

# Surface for transparent circle
transparent_circle = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
pygame.draw.circle(transparent_circle, (255, 255, 255, 128), (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)

# Function to draw balls
def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen, ball.color, (int(ball.pos[0]), int(ball.pos[1])), ball.radius)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and check collisions for each ball
    for ball in balls:
        ball.move()
        ball.check_collision()

        # Check if the ball is too large
        if ball.radius >= MAX_RADIUS:
            balls.remove(ball)  # Remove the ball
            balls.append(create_ball())  # Add a new ball

    # Draw the transparent circle and balls
    screen.blit(transparent_circle, (CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[1] - CIRCLE_RADIUS))
    draw_balls()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
