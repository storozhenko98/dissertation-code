import numpy as np
import os
import pygame
from multiprocessing import Process, Array, cpu_count

SCREENSHOT_DIR = "screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.mkdir(SCREENSHOT_DIR)

# Initialize Pygame
pygame.init()

# Constants
FPS = 1000
CELL_SIZE = 1

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

def capture_screenshot(window, step_count):
    """Capture the current state of the window and save it as an image."""
    filename = os.path.join(SCREENSHOT_DIR, f"screenshot_{step_count}.png")
    pygame.image.save(window, filename)

def apply_rule_110(row):
    extended_row = np.pad(row, (1, 1), mode='wrap')
    new_row = np.zeros_like(row)
    for i in range(1, len(extended_row) - 1):
        key = tuple(extended_row[i-1:i+2].ravel())
        new_row[i-1] = RULE_110[key]
    return new_row

def rule_110_segment(start, end, grid, result, width):
    written_rows = 0
    for i in range(start, end):
        new_row = apply_rule_110(grid[i])
        for j, val in enumerate(new_row):
            result[i * width + j] = val
        written_rows += 1
    print(f"Process {start}-{end}: Wrote {written_rows} rows.")

def compute_next_state_for_rule_110_parallel(grid):
    num_processes = cpu_count()
    rows_per_process = GRID_HEIGHT // num_processes

    result = Array('i', GRID_HEIGHT * GRID_WIDTH)  # 'i' corresponds to int32 in C
    processes = []
    for i in range(num_processes - 1):  # Exclude the last process here
        start_index = i * rows_per_process
        end_index = (i + 1) * rows_per_process
        print(f"Process {i}: Start={start_index}, End={end_index}")
        p = Process(target=rule_110_segment, args=(start_index, end_index, grid, result, GRID_WIDTH))
        processes.append(p)
        p.start()

    # Handle the last process separately
    start_index = (num_processes - 1) * rows_per_process
    end_index = GRID_HEIGHT  # Go all the way to the end
    print(f"Process {num_processes - 1}: Start={start_index}, End={end_index}")
    p = Process(target=rule_110_segment, args=(start_index, end_index, grid, result, GRID_WIDTH))
    processes.append(p)
    p.start()

    for p in processes:
        p.join()

    # Debugging: Print size of the resultant array
    print(f"Size of result array: {len(result)}")

    # Convert shared array back to numpy array
    result_grid = np.frombuffer(result.get_obj(), dtype=np.int32).reshape(GRID_HEIGHT, GRID_WIDTH)
    return result_grid

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
    current_row = 1  # Start with the second row
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
            # Update only the next row based on the last computed row
            grid[current_row] = apply_rule_110(grid[current_row - 1])
            current_row += 1
            if current_row >= GRID_HEIGHT:  # Reset the grid once we reach the bottom
                grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
                grid[0] = SEEDS[seed]()
                current_row = 1

        pygame.display.update()
        capture_screenshot(window, step_count)
        clock.tick(FPS)
        step_count += 1
        
    print(f"Simulation ended after {step_count} steps.")
    pygame.quit()


cellular_automata()
