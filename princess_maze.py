import pygame
import random
import time

# Initialize the game
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
BACKGROUND_COLOR = (0, 128, 0)
PIECE_COLOR = (255, 215, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Princess in the Garden")

# Load assets
princess_image = pygame.image.load("princess.png")
princess_image = pygame.transform.scale(princess_image, (CELL_SIZE, CELL_SIZE))
piece_image = pygame.image.load("piece.png")
piece_image = pygame.transform.scale(piece_image, (CELL_SIZE, CELL_SIZE))
wall_image = pygame.image.load("wall.png")
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image, (CELL_SIZE, CELL_SIZE))

# Game variables
princess_pos = [5, 5]

# Generate random positions for walls, avoiding the starting position of the princess
wall_count = 10
walls = []
while len(walls) < wall_count:
    wall_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    if wall_pos not in walls and wall_pos != princess_pos:
        walls.append(wall_pos)

# Generate random positions for pieces, avoiding walls and the starting position of the princess
piece_count = 5
pieces = []
while len(pieces) < piece_count:
    piece_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    if piece_pos not in pieces and piece_pos not in walls and piece_pos != princess_pos:
        pieces.append(piece_pos)

# Generate random positions for monsters, avoiding walls and the starting position of the princess
monster_count = 3
monsters = []
while len(monsters) < monster_count:
    monster_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    if monster_pos not in monsters and monster_pos not in walls and monster_pos != princess_pos:
        monsters.append(monster_pos)

score = 0
monster_delay = 1000  # Initial delay for monster movement in milliseconds
monster_timer = time.time()

def move_monster(monster_pos, princess_pos):
    # Determine the direction to move to get closer to the princess
    if monster_pos[0] < princess_pos[0]:
        new_pos = [monster_pos[0] + 1, monster_pos[1]]
    elif monster_pos[0] > princess_pos[0]:
        new_pos = [monster_pos[0] - 1, monster_pos[1]]
    elif monster_pos[1] < princess_pos[1]:
        new_pos = [monster_pos[0], monster_pos[1] + 1]
    elif monster_pos[1] > princess_pos[1]:
        new_pos = [monster_pos[0], monster_pos[1] - 1]
    else:
        new_pos = monster_pos

    # Ensure new position is within grid bounds and not in walls
    if (0 <= new_pos[0] < GRID_SIZE and
        0 <= new_pos[1] < GRID_SIZE and
        new_pos not in walls):
        return new_pos
    return monster_pos

# Main game loop
running = True
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_pos = princess_pos[:]
            if event.key == pygame.K_UP:
                new_pos[1] -= 1
            elif event.key == pygame.K_DOWN:
                new_pos[1] += 1
            elif event.key == pygame.K_LEFT:
                new_pos[0] -= 1
            elif event.key == pygame.K_RIGHT:
                new_pos[0] += 1

            # Boundary check and wall collision check
            if (0 <= new_pos[0] < GRID_SIZE and
                0 <= new_pos[1] < GRID_SIZE and
                new_pos not in walls):
                princess_pos = new_pos
    
    # Move monsters
    if current_time - monster_timer > monster_delay / 1000.0:
        for i in range(len(monsters)):
            monsters[i] = move_monster(monsters[i], princess_pos)
        monster_timer = current_time
        # Increase monster speed gradually
        if monster_delay > 100:
            monster_delay -= 20
    
    # Check for collisions with monsters
    if princess_pos in monsters:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Collect pieces
    if princess_pos in pieces:
        pieces.remove(princess_pos)
        score += 1
    
    # Drawing
    screen.fill(BACKGROUND_COLOR)
    for piece in pieces:
        screen.blit(piece_image, (piece[0] * CELL_SIZE, piece[1] * CELL_SIZE))
    for wall in walls:
        screen.blit(wall_image, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE))
    for monster in monsters:
        screen.blit(monster_image, (monster[0] * CELL_SIZE, monster[1] * CELL_SIZE))
    screen.blit(princess_image, (princess_pos[0] * CELL_SIZE, princess_pos[1] * CELL_SIZE))

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    # Check for game over (winning condition)
    if not pieces and running:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
    
    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
