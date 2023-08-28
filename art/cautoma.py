import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
FPS = 1000
CELL_SIZE = 20

# Create the window in fullscreen mode
window = pygame.display.set_mode((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Rules for the Game of Life
def game_of_life_rules(cell, neighbors):
    if cell == 1 and (neighbors < 2 or neighbors > 3):
        return 0
    elif cell == 0 and neighbors == 3:
        return 1
    return cell

# Compute the next state of the grid
def compute_next_state_optimized(grid, rule_func):
    # Create padded grid to handle edge cases
    padded_grid = np.pad(grid, ((1, 1), (1, 1)), mode='wrap')
    
    # Calculate the sum of neighbors for each cell
    neighbors = (padded_grid[:-2, :-2] + padded_grid[:-2, 1:-1] + padded_grid[:-2, 2:] +
                 padded_grid[1:-1, :-2] + padded_grid[1:-1, 2:] +
                 padded_grid[2:, :-2] + padded_grid[2:, 1:-1] + padded_grid[2:, 2:])
    
    # Apply rule function elementwise
    next_state = np.vectorize(rule_func)(grid, neighbors)
    
    return next_state


# Draw the grid
def draw_grid(window, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            color = (255, 255, 255) if grid[i, j] == 1 else (0, 0, 0)
            pygame.draw.rect(window, color, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Pause functionality and grid reset
paused = False
def toggle_cell(grid, x, y):
    i, j = y // CELL_SIZE, x // CELL_SIZE
    grid[i, j] = 1 - grid[i, j]

# Seeds
SEEDS = {
    "random": lambda: np.random.choice([0, 1], GRID_WIDTH * GRID_HEIGHT).reshape((GRID_HEIGHT, GRID_WIDTH)),
    "glider": lambda: np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]),
    # Add more seeds if needed
}

# Main function
# I will refactor the code to achieve the desired console printout and also optimize the use of global variables.

def cellular_automata(seed="random", rule_func=None):
    if rule_func is None:
        rule_func = game_of_life_rules
        
    grid = SEEDS[seed]()
    # Print seed 
    print("Initial Seed:")
    print(grid)
    
    paused = False
    step_count = 0
    running = True
    clock = pygame.time.Clock()
    
    while running:
        window.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:  # Pause/Unpause
                    paused = not paused
                elif event.key == pygame.K_r:  # Reset grid
                    grid = SEEDS["random"]()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Toggle cell state
                x, y = pygame.mouse.get_pos()
                toggle_cell(grid, x, y)

        # Draw the grid
        draw_grid(window, grid)

        if not paused:
            # Update the grid
            grid = compute_next_state_optimized(grid, rule_func)

        pygame.display.update()
        clock.tick(FPS)
        step_count += 1
        
    print(f"Simulation ended after {step_count} steps.")
    pygame.quit()


# Note: I've removed the repeated seed print, the FPS print and the redundant global keyword usage.
# I've also moved the seed print to the top of the function so it only prints once at the beginning.
# At the end of the simulation, the total number of steps is printed.

# Return the refactored code as a string
cellular_automata()
