import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up some constants
FPS = 100

# Create the window in fullscreen mode
window = pygame.display.set_mode((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

# Get the size of the window (which should now match the screen size)081298

WIDTH, HEIGHT = window.get_size()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:
    # Fill the window with a random image
    random_image = np.random.randint(0, 256, (WIDTH, HEIGHT, 3), dtype=np.uint8)
    pygame.surfarray.blit_array(window, random_image)

    # Update the window
    pygame.display.update()

    # Run at a maximum of 60 frames per second
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Exit on ESC key
            if event.key == pygame.K_ESCAPE:
                running = False

# Done! Time to quit.
pygame.quit()
