import pygame
import random
pygame.init()

print(10 % 3)
# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Side-Scrolling Game')

# Set up the clock        raise IOError(("MoviePy error: the file %s could not be found!\n"
clock = pygame.time.Clock()

# Flag to control the game loop
running = True
jumped = False
doubleJump = False
doubleJumpTick = 0

# Player properties
player = [350, 475, 0, 0]  # [x position, y position, x velocity, y velocity]
onGround = False
offset = 0
# Define the Debris class
class Debris:
    def __init__(self, direction):
        self.direction = direction
        
        # Set initial position based on player position
        self.ypos = player[1] + 49
        if direction == "Left":
            self.xpos = player[0] + 50
            self.xvel = random.randrange(0, 3)
            self.yvel = random.randrange(-3, 0)
        if direction == "Right":
            self.xpos = player[0]
            self.xvel = random.randrange(-3, 0)
            self.yvel = random.randrange(-3, 0)
        if direction == "Land":
            chance = random.randrange(0,2)
            if chance == 0:
                self.xpos = player[0]
                self.xvel = random.randrange(-3, 0)
                self.yvel = random.randrange(-3, 0)
            elif chance == 1:
                self.xpos = player[0] + 50
                self.xvel = random.randrange(0, 3)
                self.yvel = random.randrange(-3, 0)
        self.scale = 1.0  # Initial scale factor
        self.creation_time = pygame.time.get_ticks()  # Record creation time

    # Function to handle physics of debris
    def physics(self):
        self.xpos += self.xvel
        self.ypos += self.yvel
        
        # Apply gravity
        if self.ypos < 525:
            self.yvel += 0.15
        else:
            self.ypos = 525
            self.yvel = -self.yvel * 0.6  # Bounce
        
        # Bounce on walls
        if self.xpos <= 0 or self.xpos >= 800:
            self.xvel = -self.xvel
            
        # Calculate scale factor to simulate fading
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time
        if elapsed_time < 2000:  # 2 seconds
            self.scale = 1.0 - elapsed_time / 2000.0

    # Function to draw the debris
    def draw(self):
        scaled_size = int(6 * self.scale)  # Scale the size
        pygame.draw.rect(screen, (0, 125, 0), (self.xpos + offset, self.ypos, scaled_size, scaled_size))

# List to store debris objects
debris_list = []

# Function to move the player
def move_player():
    global doubleJump
    global onGround
    global doubleJumpTick
    global jumped
    global offset
    
    if keys[pygame.K_LEFT]:
        #player[2] = -5
        offset += 5
    elif keys[pygame.K_RIGHT]:
        #player[2] = 5
        offset -= 5
    else:
        player[2] = 0
    
    if player[1] >= 475:
        player[1] = 475
        onGround = True
        
    else:
        onGround = False

    if not onGround:
        player[3] += 1
        doubleJumpTick += 1
        print("falling!")
    else:
        doubleJumpTick = 0
        player[3] = 0
        
    if keys[pygame.K_UP]:
        if onGround == True:
            jumped = True
            player[3] = -15
        elif doubleJump == False and jumped == True and doubleJumpTick >= 10:
            print("Double Jumped")
            doubleJump = True
            player[3] =- 15
            
       
    

    player[0] += player[2]
    player[1] += player[3]

# Function to draw clouds
def draw_clouds():
    global offset
    for x in range(100, 800, 300):
        pygame.draw.circle(screen, (255, 255, 255), (x + offset, 100), 40)
        pygame.draw.circle(screen, (255, 255, 255), (x - 50+ offset, 125), 40)
        pygame.draw.circle(screen, (255, 255, 255), (x + 50+ offset, 125), 40)
        pygame.draw.rect(screen, (255, 255, 255), (x - 50+ offset, 100, 100, 65))

# Function to draw trees
def draw_trees():
    global offset
    for x in range(100, 800, 300):
        pygame.draw.rect(screen, (43, 29, 20), (x - 8+ offset, 370, 15, 160))
        pygame.draw.circle(screen, (0, 125, 0), (x + offset, 335), 40)
        pygame.draw.circle(screen, (0, 125, 0), (x - 40+ offset, 370), 40)
        pygame.draw.circle(screen, (0, 125, 0), (x + 40+ offset, 370), 40)

# Function to generate debris
def generate_debris():
    global onGround
    global jumped
    if onGround:
        if jumped:
            jumped = False
            doubleJump = False
            for i in range(8):
                debris_list.append(Debris("Land"))
        if keys[pygame.K_LEFT]:
            debris_list.append(Debris("Left"))
        if keys[pygame.K_RIGHT]:
            debris_list.append(Debris("Right"))
        pygame.time.set_timer(pygame.USEREVENT, 1000, True)  # Trigger event to stop generating debris after 1 second
# Main game loop
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop generating debris after 1 second

    keys = pygame.key.get_pressed()

    move_player()
    generate_debris()

    screen.fill((135, 206, 235))
    draw_clouds()
    draw_trees()

    pygame.draw.rect(screen, (0, 150, 0), (0, 525, 800, 75))
    pygame.draw.rect(screen, (255, 0, 255), (player[0], player[1], 50, 50))
    
    # Update and draw debris
    for debris in debris_list:
        debris.physics()
        debris.draw()
        
    pygame.display.flip()

pygame.quit()

