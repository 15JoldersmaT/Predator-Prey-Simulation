import pygame
import numpy as np
import random


print ('Good example setup, 2 cats 2 mice')
noMice = input('Number of Mice?')
noCats = input('Number of Cats?')
wallMut = False
wM = input('Mouse mutate on walls? (y or n)')
if wM == 'y':
    wallMut = True


#Activation Function
af = input('Activation Function? l for leaky relu, s for sigmoid, r for relu : ')

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
CATCH_DISTANCE = 10  # Example catch distance in pixels
MOUSE_SPEED = 2
CAT_SPEED = 9

mouseLoseStreak = 0
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


def find_closestCat(mouse, cats):
    closest_cat = None
    min_distance = float('inf')
    for cat in cats:
        if not cat.catch:  # Check if the cat hasn't caught a mouse yet
            dist = distance(mouse.rect.centerx, mouse.rect.centery, cat.rect.centerx, cat.rect.centery)
            if dist < min_distance:
                min_distance = dist
                closest_cat = cat
    return closest_cat

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def reset_predators(predators):
    # Set predators to a specific starting position
    for predator in predators:
        predator.rect.x = random.randint(1,800)  # Define starting x-coordinate
        predator.rect.y = random.randint(1,600)  # Define starting y-coordinate
        predator.catch = False


def reset_preys(preys):
    # Set preys to a different specific starting position
    for prey in preys:
        prey.rect.x = random.randint(1,800)  # Define starting x-coordinate
        prey.rect.y = random.randint(1,600)  # Define starting y-coordinate
        prey.catch = False
        
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


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)
    
    
class Animal:
    def __init__(self, x, y, color, speed):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.speed = speed
        self.catch = False  # Initialize catch attribute
        self.brain = np.random.rand(5, 2)  # Adjusted brain shape
  # Example brain structure

    def draw(self):
        # Calculate the center of the rectangle
        center = self.rect.center
        # Assuming the width and height of the rect are the same, use either for the radius
        radius = self.rect.width // 2
        pygame.draw.circle(screen, self.color, center, radius)

    
    
    def think(self, inputs):
        global af
        # Simple neural network without activation function
        output = np.dot(inputs, self.brain)
        if af == 's':
            return sigmoid(output)
        elif af == 'l': 
            return leaky_relu(output)
        else:
            return relu(output)
        

    def move(self, direction):
        #Add randomness to the movement
        random_movement = np.random.rand(2) * 2 - 1  # Random values between -1 and 1
        random_scale = 0.3  # Adjust this to increase/decrease randomness
        move_x, move_y = direction[0] + random_movement[0] * random_scale, direction[1] + random_movement[1] * random_scale

        # Clamp the movement values based on the speed
        move_x = max(-self.speed, min(self.speed, move_x))
        move_y = max(-self.speed, min(self.speed, move_y))

        # Update position
        self.rect.x += int(move_x)
        self.rect.y += int(move_y)

        # Keep within screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Cat(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, RED, CAT_SPEED)
        self.edge_touch = False

    def move(self, direction):
        super().move(direction)  # Call the move method from the parent class
        # Check if touching the edge of the screen
        if self.rect.left <= 10 or self.rect.right >= SCREEN_WIDTH -10 or self.rect.top <= 10 or self.rect.bottom >= SCREEN_HEIGHT -10:
            self.edge_touch = True
            if wallMut == True:
                mutate_brain(self.brain,.1)
            #mutate_brain(self.brain)

            self.edge_touch = False

    def draw(self):
        if self.catch == False:
            super().draw()
        else:
            return
            
        
     

class Mouse(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, MOUSE_SPEED)
        self.edge_touch = False
    def move(self, direction):
        global epoch
        global wallMut 
        super().move(direction)  # Call the move method from the parent class
        # Check if touching the edge of the screen
        if self.rect.left <= 10 or self.rect.right >= SCREEN_WIDTH -10 or self.rect.top <= 10 or self.rect.bottom >= SCREEN_HEIGHT -10:
            self.edge_touch = True

            if wallMut == True:
                mutate_brain(self.brain, .1)
            #mutate_brain(self.brain)
            
            #mutate_brain(self.brain)

            #Time = 0
            #epoch = epoch + 1
            #print (epoch)
            #reset_predators(cats)
            #reset_preys(mice)
            self.edge_touch = False
    def draw(self):
        if self.catch == False:
            super().draw()
        else:
            return

        
cats = [Cat(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(int(noCats))]
mice = [Mouse(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(int(noMice))]


input_size = 2 + 6 * len(cats) + 6 * len(mice) +1   # 2 for self, 6 per other animal

for cat in cats:
    cat.brain = np.random.rand(input_size, 2)

for mouse in mice:
    mouse.brain = np.random.rand(input_size, 2)
    
def check_collision(predator, prey, catch_distance):
    predator_center = predator.rect.center
    prey_center = prey.rect.center
    return distance(predator_center[0], predator_center[1], prey_center[0], prey_center[1]) < catch_distance

def normalize_coordinate(x, max_value):
    return x / max_value

def construct_input_for_animal(current_animal, cats, mice):
    global Time
    inputs = []
    normT = normalize_coordinate(Time, TIME_THRESHOLD)
    normX = normalize_coordinate(current_animal.rect.x, SCREEN_WIDTH)
    normY = normalize_coordinate(current_animal.rect.y, SCREEN_HEIGHT)
    # Include the current animal's own x, y positions first
    inputs.extend([current_animal.rect.x, current_animal.rect.y])

    for cat in cats:
        # Include the x, y positions, type flag, and catch status of the cat
        cat_type_flag = 1  # 1 for Cat
        cat_status = 1 if cat.catch else 0
        inputs.extend([cat.rect.x, cat.rect.y, cat_type_flag, cat_status])
        # Include the differences in x, y
        diff_x = current_animal.rect.x - cat.rect.x
        diff_y = current_animal.rect.y - cat.rect.y
        diff_x = normalize_coordinate(diff_x, SCREEN_WIDTH)
        diff_y = normalize_coordinate(diff_y, SCREEN_WIDTH)
        inputs.extend([diff_x, diff_y])

    for mouse in mice:
        # Include the x, y positions, type flag, and catch status of the mouse
        mouse_type_flag = 0  # 0 for Mouse
        mouse_status = 1 if mouse.catch else 0
        inputs.extend([mouse.rect.x, mouse.rect.y, mouse_type_flag, mouse_status])
        # Include the differences in x, y
        diff_x = current_animal.rect.x - mouse.rect.x
        diff_y = current_animal.rect.y - mouse.rect.y
        diff_x = normalize_coordinate(diff_x, SCREEN_WIDTH)
        diff_y = normalize_coordinate(diff_y, SCREEN_WIDTH)
        inputs.extend([diff_x, diff_y])
    inputs.append(normT)
    return np.array(inputs)

myFont = pygame.font.SysFont("Times New Roman", 18)


running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                FPS = 10  # Increase FPS
            elif event.key == pygame.K_2:
                FPS = 20  # Decrease FPS
            elif event.key == pygame.K_3:
                FPS = 25  # Decrease FPS
            elif event.key == pygame.K_4:
                FPS = 30  # Decrease FPS
            elif event.key == pygame.K_5:
                FPS = 45  # Decrease FPS
            elif event.key == pygame.K_6:
                FPS = 60  # Decrease FPS
            elif event.key == pygame.K_7:
                FPS = 120  # Decrease FPS
            elif event.key == pygame.K_8:
                FPS = 220  # Decrease FPS
            elif event.key == pygame.K_9:
                FPS = 550  # Decrease FPS
            elif event.key == pygame.K_0:
                FPS = 1500  # Decrease FPS




            if FPS < 10:  # Ensure FPS doesn't go below a reasonable threshold
                FPS = 10
    
    # Render the time and display it
    time_surface = myFont.render(f"Time: {epoch} s", True, BLACK)
    screen.blit(time_surface, (10, 500))  # Position it at the bottom of the screen

    Time = Time + 1
    current_time = pygame.time.get_ticks()
    if Time > TIME_THRESHOLD:
        for cat in cats:
            mutate_brain(cat.brain, .2)
            #mutate_brain(cat.brain)


        #No need to update mice brains, they won
        #for mouse in mice:
            #mutate_brain(mouse.brain)


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
            if check_collision(cat, mouse, CATCH_DISTANCE) and cat.catch == False and mouse.catch == False:
                mutate_brain(mouse.brain, .5,.5)
                mouse.catch = True
                cat.catch = True
                

                


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
            if cat == last_cat_to_catch:
                # Mutate cats except the last one to catch a mouse
                mutate_brain(cat.brain)
                #mutate_brain(cat.brain)

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
    
    

    # Update and draw mice
    for cat in cats:
        inputs = construct_input_for_animal(cat, cats, mice)
        direction = cat.think(inputs)
        cat.move(direction)
        cat.draw()

    for mouse in mice:
        inputs = construct_input_for_animal(mouse, cats, mice)
        direction = mouse.think(inputs)
        mouse.move(direction)
        mouse.draw()

   

 

    epoch_surface = myFont.render(f"Epoch: {epoch}", True, WHITE)
    epoch_position = (SCREEN_WIDTH - 150, 10)  # Adjust position as needed
    screen.blit(epoch_surface, epoch_position)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
