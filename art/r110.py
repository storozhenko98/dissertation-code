import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
FPS = 1000
CELL_SIZE = 2

# Create the window in fullscreen mode
window = pygame.display.set_mode((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Rule 110
RULE_110 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0
}

def apply_rule_110(row):
    extended_row = np.pad(row, (1, 1), mode='wrap')
    new_row = np.zeros_like(row)
    for i in range(1, len(extended_row) - 1):
        new_row[i-1] = RULE_110[tuple(extended_row[i-1:i+2])]
    return new_row

# Compute the next state of the grid for Rule 110
def compute_next_state_for_rule_110(grid):
    new_grid = np.zeros_like(grid)
    new_grid[0] = grid[0]
    for i in range(1, GRID_HEIGHT):
        new_grid[i] = apply_rule_110(grid[i-1])
    return new_grid

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
    "rule_110": lambda: np.array([0 if i != GRID_WIDTH//2 else 1 for i in range(GRID_WIDTH)]).reshape(1, GRID_WIDTH)
}

def cellular_automata(seed="rule_110"):
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    grid[0] = SEEDS[seed]()
    
    print("Initial Seed:")
    print(grid[0])
    
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
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Toggle cell state
                x, y = pygame.mouse.get_pos()
                toggle_cell(grid, x, y)

        # Draw the grid
        draw_grid(window, grid)

        if not paused:
            # Update the grid
            grid = compute_next_state_for_rule_110(grid)

        pygame.display.update()
        clock.tick(FPS)
        step_count += 1
        
    print(f"Simulation ended after {step_count} steps.")
    pygame.quit()

cellular_automata()
