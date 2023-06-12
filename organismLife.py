import random # Importing the random module to generate random numbers

# Setting initial values for x and y coordinates
x = 0
y = 0

# This function generates a random number between 0 and 10.
# It simulates the presence of food in a space.
# If the random number is above a certain threshold, it indicates food is present.
def foodGen():
    return random.randint(0, 10) # Generating a random integer between 0 and 10

# This function generates a 3x3 grid representing the world around the organism.
# Each cell contains [x-coordinate, y-coordinate, food presence (random number 0-10)].
def worldGenerator():
    return [
        [x-1, y+1, foodGen()], [x, y+1, foodGen()], [x+1, y+1, foodGen()],
        [x-1, y, foodGen()], [x, y, foodGen()], [x+1, y, foodGen()],
        [x-1, y-1, foodGen()], [x, y-1, foodGen()], [x+1, y-1, foodGen()]
    ]

# Defining a class called Organism to represent an individual organism
class Organism:
    # Constructor: sets the initial health and name of the organism
    def __init__(self, health, name):
        self.health = health
        self.name = name

    # Method to get the current health of the organism
    def get_health(self):
        return self.health

    # Method to set the health of the organism
    def set_health(self, value):
        self.health = value

    # Method to simulate the organism's eye. Currently, it just prints the data.
    def eye(self, data):
        print("EYE:")
        print(data)
        return data

    # Method to compress the data. It checks if there is food (food > 5) in each space and sets the value to 1, otherwise 0.
    def compression(self, data):
        for i in range(len(data)):
            if data[i][2] > 5:
                data[i][2] = 1
            else:
                data[i][2] = 0
        print("COMPRESSION: ")
        print(data)
        return data

    # Method that uses the eye and compression methods to process visual data.
    def vision(self, data):
        visualStream = self.eye(data)
        visualStream = self.compression(visualStream)
        print("VISION: ")
        print(visualStream)
        return visualStream

    # Method to detect food in the vicinity.
    def foodDetection(self, data):
        space = self.vision(data)
        for each in space:
            if each[2] == 1:
                self.set_health(self.get_health() + 5) # If food is detected, increase health by 10
                return [each[0], each[1]]
        return [0, 0]

    # Method to check if the organism can reproduce based on its health.
    def reproduction(self):
        if self.get_health() >= 100:
            self.set_health(50) # Reduce health to 50 after reproduction
            return True
        else:
            return False

    # Method to move the organism. If there is no food, it loses 1 health, otherwise it loses 2 health.
    def move(self, data):
        if data[0] == 0 and data[1] == 0:
            health = self.get_health()
            print(health)
            health = health - 1
            self.set_health(health)
        else:
            health = self.get_health()
            print(health)
            health = health - 2
            self.set_health(health)

    # Method to simulate one cycle of the organism's life.
    def cycle(self):
        print(self.name)
        data = worldGenerator() # Generate the world around the organism
        placeToMove = self.foodDetection(data) # Detect food
        self.move(placeToMove) # Move the organism

# List to store organisms
# get input from user for number of cycles to run

cycleNumber = input("Enter the number of cycles to run: ")
cycleNumber = int(cycleNumber)


organisms = [Organism(20, "Organism 0")]

# Loop through 30 cycles
for i in range(cycleNumber):
    print("Cycle: " + str(i))
    for organism in organisms:
        # Check if the organism can reproduce
        if organism.reproduction() == True:
            print("Reproduction")
            # Create a new instance of the Organism class and add it to the list
            new_organism = Organism(20, "Organism " + str(len(organisms)))
            organisms.append(new_organism)
            print("New Organism: " + new_organism.name)
        organism.cycle() # Simulate one cycle of the organism's life
