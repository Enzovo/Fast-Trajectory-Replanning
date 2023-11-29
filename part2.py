import heapq
import matplotlib.pyplot as plt

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

    def __lt__(self, other):
        return self.f < other.f

# choose greater g
class CellGreater(Cell):
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

# choose less g
class CellLess(Cell):
    def __lt__(self, other):
        if self.f == other.f:
            return self.g < other.g
        return self.f < other.f

# class Astar
class AStar(object):
    def __init__(self, grid_width=5, grid_height=5):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = grid_height
        self.grid_width = grid_width

    # initialize grid, all is unblocked for part 2
    # start point(0,0), end point(grid_width-1, grid_height-1), that is, (4,4) in part 2
    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(0, 0)
        self.end = self.get_cell(self.grid_width-1, self.grid_height-1)

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

# use greater g
class AStarGreater(AStar):
    def __init__(self, grid_width=5, grid_height=5):
        super().__init__(grid_width, grid_height)
        self.cells = [CellGreater(x, y, True) for x in range(grid_width) for y in range(grid_height)]

# use less g
class AStarLess(AStar):
    def __init__(self, grid_width=5, grid_height=5):
        super().__init__(grid_width, grid_height)
        self.cells = [CellLess(x, y, True) for x in range(grid_width) for y in range(grid_height)]

class RepeatedAStarGreater(AStarGreater):
    pass  # inherit all from AStarGreater

class RepeatedAStarLess(AStarLess):
    pass  # inherit all from AStarLess

# visualization of grid and path
def visualize_grid(ax, grid, path):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:  # 1 means bloced
                ax.scatter(j, i, color='black')
    path_x = [coord[1] for coord in path]
    path_y = [coord[0] for coord in path]
    ax.plot(path_x, path_y, color='red')

fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# Repeated Forward A* with greater g
forward_greater = RepeatedAStarGreater()
forward_greater.init_grid()
p1 = forward_greater.solve()
visualize_grid(axs[0], [[0]*5]*5, p1)
axs[0].set_title('Greater g')

# Repeated Forward A* with less g
forward_less = RepeatedAStarLess()
forward_less.init_grid()
p2 = forward_less.solve()
visualize_grid(axs[1], [[0]*5]*5, p2)
axs[1].set_title('Less g')

plt.show()