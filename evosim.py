import pygame
import random
import time

# Constants
GRID_SIZE = 200
CELL_SIZE = 5
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # 100 by 5
CREATURE_COUNT = 100
FOOD_COUNT = 3000
ITERATIONS_PER_CYCLE = 50  # Each cycle has 50 iterations
CYCLE_LIMIT = 3  # Creatures die after not eating for 3 cycles

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame, screen, clock
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

#creature class
class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_eaten = False  # Track if the creature has eaten this cycle
        self.food_eaten_count = 3
    
    def move(self):
        # Random movement (up, down, left, right, and diagonal directions)
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0),  # Cardinal directions
                                   (1, 1), (1, -1), (-1, 1), (-1, -1)])  # Diagonal directions
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        
        # Keep the creature inside bounds
        self.x = max(0, min(GRID_SIZE - 1, new_x))
        self.y = max(0, min(GRID_SIZE - 1, new_y))
        
    def eat(self, food_map):
        #if creature occupies same space as food, eat it
        if (self.x, self.y) in food_map:
            del food_map[(self.x, self.y)] 
            self.food_eaten = True 
            return True
    
    def eaten(self):
        return self.food_eaten
    
    def food_eaten_count(self):
        return self.food_eaten_count

    def reproduce(self):
        # Offspring inherits the same position
        offspring = Creature(self.x, self.y)
        return offspring

# Initialize creatures and food
creatures = [Creature(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)) for _ in range(CREATURE_COUNT)]
food_map = {(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)): 1 for _ in range(FOOD_COUNT)}

# Add print statement to confirm creature creation
print(f"Initial number of creatures: {len(creatures)}")  # Should print 50 initially
food_regrowth = {}  # Dictionary to track food that needs to regrow

running = True
cycle_count = 1

while running:

    screen.fill(BLACK)

    #make sure food_eaten set to false at start of cycle
    for creature in creatures:
        creature.food_eaten = False
    
    # THIS IS ONE ITERATION

    # Run the simulation for the specified number of iterations (50 iterations per cycle)
    for r in range(ITERATIONS_PER_CYCLE):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen before drawing new positions
        screen.fill(BLACK)
        
        # Draw food
        for (fx, fy) in food_map.keys():
            pygame.draw.rect(screen, GREEN, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw creatures
        for creature in creatures:
            pygame.draw.rect(screen, WHITE, (creature.x * CELL_SIZE, creature.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Move and eat for all creatures
        for creature in creatures:
            creature.move()
            creature.eat(food_map)
        
        # regrow food after 1 cycle has passed
        for (fx, fy) in list(food_regrowth.keys()):
            food_regrowth[(fx, fy)] -= 1
            if food_regrowth[(fx, fy)] <= 0:
                food_map[(fx, fy)] = 1
                del food_regrowth[(fx, fy)]
        
        pygame.display.flip()
        clock.tick(60)

    creatures_without_food = 0

    for creature in creatures:
        #
        if creature.food_eaten == False:
            creature.food_eaten_count -= 1
            creatures_without_food += 1

    
    # only creatures that have eaten in this cycle will survive
    survivors = [c for c in creatures if c.food_eaten]  
    offspring_count = 0
    
    new_creatures = []
    for c in survivors:
        if cycle_count % 3 == 0:
            offspring = c.reproduce()
            new_creatures.append(offspring)
            offspring_count += 1
            offspring = c.reproduce()
            new_creatures.append(offspring)
            offspring_count += 1
    
    creatures = survivors + new_creatures  # Combine survivors and offspring
    '''print(f"Offspring created: {offspring_count}")'''
    
    # Regrow food in random positions
    if cycle_count % 3 == 0:
        for _ in range(FOOD_COUNT - len(food_map)):
            fx, fy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if (fx, fy) not in food_map:
                food_map[(fx, fy)] = 1
                food_regrowth[(fx, fy)] = 1  # Mark food for regrowth
    
    # Count how many creatures didn't eat this cycle
    '''creatures_without_food = sum(1 for c in creatures if not c.food_eaten)'''

    # Count how many creatures have food_eaten_count at 0
    creatures_food_eaten_count_zero = sum(1 for c in creatures if c.food_eaten_count == 0)

    # Print the results
    # Print the number of creatures and offspring created
    print(f"CYCLE {cycle_count}")
    print(f"Number of creatures: {len(creatures)}")
    print(f"Creatures about to die: {creatures_food_eaten_count_zero}")
    print(f"Creatures that have reproduced: {offspring_count}")
    print("")

    cycle_count += 1

    #add new_creatures when introducing offspring
    creatures = [c for c in creatures if c.food_eaten_count >= 0]

    if len(creatures) == 0:
        print("GAME OVER")
        break

    '''print("Starting next set of iterations in 5 seconds...")'''
    time.sleep(1)

pygame.quit()
