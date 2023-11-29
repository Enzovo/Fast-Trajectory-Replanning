import random
from collections import deque

# size 101*101, probability of blocked cell 0.3
GRID_SIZE = 101
OBSTACLE_PROBABILITY = 0.3

# generate grid
def generate_grid():
    return [[1 if random.random() < OBSTACLE_PROBABILITY else 0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# BFS
def bfs(grid):
    visited = [[False]*len(grid[0]) for _ in range(len(grid))]
    queue = deque([(0, 0)])

    while queue:
        x, y = queue.popleft()
        if (x, y) == (len(grid)-1, len(grid[0])-1):
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))

    return False

# save to txt files under folder ./gridworld
def save_grid_to_file(grid, filename):
    with open(filename, 'w') as file:
        for row in grid:
            file.write(''.join(str(cell) for cell in row) + '\n')

gridworlds = []
while len(gridworlds) < 50:
    grid = generate_grid()
    if bfs(grid):
        gridworlds.append(grid)
        filename = f"./gridworld/{len(gridworlds)}.txt"
        save_grid_to_file(grid, filename)
        print(f"Gridworld {len(gridworlds)} generated and saved to {filename}.")
print("All gridworlds generated.")