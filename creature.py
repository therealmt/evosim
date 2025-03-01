import random


#creature class
class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_eaten = False  # Track if the creature has eaten this cycle
        self.food_eaten_count = 3
    
    def move(self, GRID_SIZE):
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