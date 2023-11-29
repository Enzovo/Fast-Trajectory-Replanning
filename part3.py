import heapq
import matplotlib.pyplot as plt
import time

# class cell, containing reachable, coordinates, g,h,f
class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    # choose greater g
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

# class Astar with 101*101 created grid
class AStar(object):
    def __init__(self, grid_width=101, grid_height=101):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = grid_height
        self.grid_width = grid_width

    def get_grid(self):
        grid = [[0 for _ in range(self.grid_height)] for _ in range(self.grid_width)]
        for cell in self.cells:
            if not cell.reachable:
                grid[cell.x][cell.y] = 1
        return grid

    # start point(0,0), end point(grid_width-1, grid_height-1), that is, (100,100)
    # input contains the filename of the saved txt file which has the saved grid
    def init_grid(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Generate grid from lines
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if lines[x][y] == '1':
                    reachable = False
                else:
                    reachable = True

                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(0, 0)
        self.end = self.get_cell(self.grid_width - 1, self.grid_height - 1)

    #  Manhattan distance
    def get_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    # 4 adjacent cells
    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    # use parent to look back to get the path
    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not None:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.reverse()
        return path

    # update parent, g,h,f
    def update_cell(self, adj, cell):
        adj.g = cell.g + 1
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop from open set
            f, cell = heapq.heappop(self.opened)
            # add it to close set
            self.closed.add(cell)
            if cell is self.end:
                # find the path
                return self.get_path()
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                # reachable and not visited adjacent
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 1:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

# repeated astar class of forward / backward
class RepeatedAStar(AStar):
    def __init__(self, forward=True):
        super().__init__()
        self.forward = forward

    def solve(self):
        if self.forward:
            # forward
            self.start, self.end = self.get_cell(0, 0), self.get_cell(100, 100)
        else:
            # backward
            self.start, self.end = self.get_cell(100, 100), self.get_cell(0, 0)
        while self.start != self.end:
            path = super().solve()
            if path is None:
                return None
            for x, y in path:
                cell = self.get_cell(x, y)
                if not cell.reachable:
                    break
                self.start = cell
        return self.get_path()


total_time_forward = 0
total_time_backward = 0

# run each for 50 times, compare the total time
for i in range(1, 51):
    filename = f"./gridworld/{i}.txt"

    # forward
    forward = RepeatedAStar(forward=True)
    # initialize grid using filename
    forward.init_grid(filename)
    # only calculate the time for solving
    start_time = time.time()
    forward.solve()
    end_time = time.time()
    time_forward = end_time - start_time
    total_time_forward += time_forward

    # backward
    backward = RepeatedAStar(forward=False)
    # initialize grid using filename
    backward.init_grid(filename)
    # only calculate the time for solving
    start_time = time.time()
    backward.solve()
    end_time = time.time()
    time_backward = end_time - start_time
    total_time_backward += time_backward

print("Total time for repeated forward A*: ", total_time_forward)
print("Total time for repeated backward A*: ", total_time_backward)


# visualization of grid and path
def visualize_grid(ax, grid, path):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:  # 1 means blocked
                ax.scatter(j, i, color='blue')
    path_x = [coord[1] for coord in path]
    path_y = [coord[0] for coord in path]
    ax.plot(path_x, path_y, color='red')

# visualization comparision of repeated forward and backward
filename = './gridworld/1.txt'

# subplot
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Repeated Forward A*
forward = RepeatedAStar(forward=True)
forward.init_grid(filename)
p1 = forward.solve()
grid_repeated_forward = forward.get_grid()
visualize_grid(axs[0], grid_repeated_forward, p1)
axs[0].set_title('Repeated Forward A*')

# Repeated Backward A*
backward = RepeatedAStar(forward=False)
backward.init_grid(filename)
p2 = backward.solve()
grid_repeated_backward = backward.get_grid()
visualize_grid(axs[1], grid_repeated_backward, p2)
axs[1].set_title('Repeated Backward A*')

plt.show()