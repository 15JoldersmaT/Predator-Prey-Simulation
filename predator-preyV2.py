import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
TIME_THRESHOLD = 1380  # Time in milliseconds, e.g., 30 seconds
CATCH_DISTANCE = 30  # Example catch distance in pixels

start_time = pygame.time.get_ticks()
epoch = 0
Time =0
# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Predator-Prey Ecosystem")

# Clock to control game's frame rate
clock = pygame.time.Clock()


def find_closest(animal, others):
    closest = None
    min_distance = float('inf')
    for other in others:
        dist = distance(animal.rect.centerx, animal.rect.centery, other.rect.centerx, other.rect.centery)
        if dist < min_distance:
            min_distance = dist
            closest = other
    return closest


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def reset_predators(predators):
    # Set predators to a specific starting position
    for predator in predators:
        predator.rect.x = random.randint(1,800)  # Define starting x-coordinate
        predator.rect.y = random.randint(1,600)  # Define starting y-coordinate

def reset_preys(preys):
    # Set preys to a different specific starting position
    for prey in preys:
        prey.rect.x = 400  # Define starting x-coordinate
        prey.rect.y = 400  # Define starting y-coordinate
        
def mutate_brain(brain, mutation_rate=0.2, mutation_amount=0.2):
    # Apply mutation to each weight in the brain
    for i in range(brain.shape[0]):
        for j in range(brain.shape[1]):
            if random.random() < mutation_rate:  # Random chance to mutate
                # Apply a small random change
                change = np.random.normal(0, mutation_amount)
                brain[i][j] += change

def leaky_relu(x, alpha=0.01):
        return np.maximum(alpha * x, x)
    
class Animal:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.brain = np.random.rand(5, 2)  # Adjusted brain shape
  # Example brain structure

    def draw(self):
        # Calculate the center of the rectangle
        center = self.rect.center
        # Assuming the width and height of the rect are the same, use either for the radius
        radius = self.rect.width // 2
        pygame.draw.circle(screen, self.color, center, radius)

    
    
    def think(self, inputs):
        # Simple neural network without activation function
        output = np.dot(inputs, self.brain)
        return leaky_relu(output)

    def move(self, direction):

        # Add randomness to the movement
        random_movement = np.random.rand(2) * 2 - 1  # Random values between -1 and 1
        random_scale = 0.5  # Adjust this to increase/decrease randomness
        move_x, move_y = direction[0] + random_movement[0] * random_scale, direction[1] + random_movement[1] * random_scale

        # Convert to integer and clamp values
        move_x = int(move_x)
        move_y = int(move_y)
        max_move = 7  # Example max movement per step
        move_x = max(-max_move, min(max_move, move_x))
        move_y = max(-max_move, min(max_move, move_y))
        
        # Convert to integer and clamp values
        move_x = int(direction[0])
        move_y = int(direction[1])

        # Optionally, you can clamp the move to a max value
        max_move = 7  # Example max movement per step
        move_x = max(-max_move, min(max_move, move_x))
        move_y = max(-max_move, min(max_move, move_y))

        # Update position
        self.rect.x += move_x
        self.rect.y += move_y

        # Keep within screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

class Cat(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.catch = False  # Initialize catch attribute


class Mouse(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN)
        self.edge_touch = False
    def move(self, direction):
        super().move(direction)  # Call the move method from the parent class
        # Check if touching the edge of the screen
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.edge_touch = True

        
cats = [Cat(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(5)]
mice = [Mouse(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(10)]



def check_collision(predator, prey, catch_distance):
    predator_center = predator.rect.center
    prey_center = prey.rect.center
    return distance(predator_center[0], predator_center[1], prey_center[0], prey_center[1]) < catch_distance

def construct_input_for_animal(animal, animals):
    inputs = []
    for other in animals:
        inputs.extend([other.rect.x, other.rect.y, animal.rect.x - other.rect.x, animal.rect.y - other.rect.y])
    return np.array(inputs)

myFont = pygame.font.SysFont("Times New Roman", 18)


running = True
while running:

    
    # Render the time and display it
    time_surface = myFont.render(f"Time: {epoch} s", True, BLACK)
    screen.blit(time_surface, (10, 500))  # Position it at the bottom of the screen

    Time = Time + 1
    current_time = pygame.time.get_ticks()
    if Time > TIME_THRESHOLD:
        for cat in cats:
            mutate_brain(cat.brain)


        for mouse in mice:
            mutate_brain(mouse.brain)


        # Reset the timer
        Time = 0
        epoch = epoch + 1
        print (epoch)
        reset_predators(cats)
        reset_preys(mice)
    last_cat_to_catch = None
    catch_count = 0  # Counter for the number of cats that have caught a mouse

    for cat in cats:
        for mouse in mice:
            if check_collision(cat, mouse, CATCH_DISTANCE):
                cat.catch = True
                mutate_brain(mouse.brain)
                


    # Check if all cats have caught a mouse or no mice are left
    for cat in cats:
        for mouse in mice:
            if check_collision(cat, mouse, CATCH_DISTANCE):
                cat.catch = True
                catch_count += 1
                last_cat_to_catch = cat
                # Logic to handle caught mouse (e.g., remove the mouse)

    # Check if all but one cat have caught a mouse
    if catch_count >= len(cats) - 1:
        for cat in cats:
            if cat != last_cat_to_catch:
                # Mutate cats except the last one to catch a mouse
                mutate_brain(cat.brain)
                cat.catch = False  # Reset the catch attribute for the next round
        reset_predators(cats)
        reset_preys(mice)
        epoch = epoch + 1
        print (epoch)
        catch_count = 0  # Reset the counter
        last_cat_to_catch = None

        # Reset the timer
    start_time = current_time
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

     # Update and draw cats
    for cat in cats:
        closest_mouse = find_closest(cat, mice)
        if closest_mouse:
            # Calculate differences in x and y coordinates
            diff_x = closest_mouse.rect.x - cat.rect.x
            diff_y = closest_mouse.rect.y - cat.rect.y
            inputs = np.array([diff_x, diff_y, cat.rect.x, cat.rect.y, Time])  # Cat inputs
        else:
            inputs = np.array([0, 0, 1])  # No mouse case
        direction = cat.think(inputs)
        cat.move(direction)
        cat.draw()

    # Update and draw mice
    for mouse in mice:

        #experimenting with this
        #if mouse.edge_touch:
            #mutate_brain(mouse.brain)
            #mouse.edge_touch = False  # Reset the flag
            
        closest_cat = find_closest(mouse, cats)
        if closest_cat:
            # Calculate differences in x and y coordinates
            diff_x = closest_cat.rect.x - mouse.rect.x
            diff_y = closest_cat.rect.y - mouse.rect.y
            inputs = np.array([diff_x, diff_y, mouse.rect.x, mouse.rect.y,Time])  # Mouse inputs
        else:
            inputs = np.array([0, 0, 1])  # No cat case
        direction = mouse.think(inputs)
        mouse.move(direction)
        mouse.draw()

    for cat in cats:
        for mouse in mice:
            if check_collision(cat, mouse, CATCH_DISTANCE):
                # Mutate cat's brain
                mutate_brain(mouse.brain)

                # Reset positions
                #reset_predators(cats)
                #reset_preys(mice)

    if len(cats) < 2:
        print ('Cat Winners')
    if len(mice) < 2:
        print ('Mice Winners')

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
