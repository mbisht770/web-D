import pygame
import heapq
import random

# Initialize Pygame
pygame.init()

# Grid settings
GRID_SIZE = 30
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Pygame setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("A* Pathfinding Visualization")

# Directions for neighbors (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Obstacles, start, and end points
obstacles = set()
start = None
end = None


class Node:
    """A* Node representing a position in the grid."""
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start
        self.h = h  # Estimated cost to goal (heuristic)
        self.f = g + h  # Total cost (F = G + H)
        self.parent = parent  # Track path

    def __lt__(self, other):
        return self.f < other.f  # Needed for priority queue


def heuristic(a, b):
    """Manhattan distance heuristic for A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node):
    """Return valid neighboring positions"""
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in obstacles:
            neighbors.append((nx, ny))
    return neighbors


def astar(start, end):
    """A* algorithm to find the shortest path"""
    open_set = []
    heapq.heappush(open_set, Node(*start, g=0, h=heuristic(start, end)))
    closed_set = set()
    came_from = {}

    while open_set:
        current = heapq.heappop(open_set)

        if (current.x, current.y) == end:
            return reconstruct_path(came_from, current)

        closed_set.add((current.x, current.y))

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            new_node = Node(*neighbor, g=current.g + 1, h=heuristic(neighbor, end), parent=current)
            heapq.heappush(open_set, new_node)
            came_from[neighbor] = current

    print("No path found!")
    return None  # No valid path


def reconstruct_path(came_from, current):
    """Reconstructs the path from start to end"""
    path = []
    while current:
        path.append((current.x, current.y))
        current = current.parent
    return path[::-1]  # Reverse to get start → end


def reset_game():
    """Clears the grid and resets start/end points."""
    global start, end, obstacles
    start = None
    end = None
    obstacles = set()


def draw_grid():
    """Draws the grid lines"""
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_SIZE, y))


def draw_elements(path):
    """Draws start, end, obstacles, and path"""
    screen.fill(WHITE)

    # Draw obstacles
    for (x, y) in obstacles:
        pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw path
    if path:
        for (x, y) in path:
            pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw start
    if start:
        pygame.draw.rect(screen, BLUE, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw end
    if end:
        pygame.draw.rect(screen, RED, (end[0] * CELL_SIZE, end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_grid()
    pygame.display.flip()


# Main game loop
running = True
path = None

while running:
    draw_elements(path)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

            if event.button == 1:  # Left click: Set start
                if (grid_x, grid_y) not in obstacles and (grid_x, grid_y) != end:
                    start = (grid_x, grid_y)

            elif event.button == 3:  # Right click: Set end
                if (grid_x, grid_y) not in obstacles and (grid_x, grid_y) != start:
                    end = (grid_x, grid_y)

            elif event.button == 2:  # Middle click: Add obstacle
                if (grid_x, grid_y) != start and (grid_x, grid_y) != end:
                    obstacles.add((grid_x, grid_y))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start and end:
                    path = astar(start, end)
                    if path is None:
                        print("No valid path! Resetting...")
                        reset_game()
                else:
                    print("Set start and end points before running A*")

            elif event.key == pygame.K_r:  # Reset game
                reset_game()
                path = None

pygame.quit()
