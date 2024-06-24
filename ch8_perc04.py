import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

class Percolator:
    def __init__(self, nx=400, ny=400, p=0.5):
        self.nx = nx
        self.ny = ny
        self.p = p
        self.grid = np.zeros((nx, ny), dtype=bool)
        self.cluster_ids = np.full((nx, ny), -1, dtype=int)
        self.iterations = 0
        self.next()

    def next(self):
        self.grid = np.random.rand(self.nx, self.ny) < self.p
        self.cluster_ids.fill(-1)
        self.iterations += 1

    def is_occupied(self, i, j):
        return self.grid[i, j]

    def cluster(self):
        current_cluster_id = 0
        for i in range(self.nx):
            for j in range(self.ny):
                if self.grid[i, j] and self.cluster_ids[i, j] == -1:
                    self._flood_fill(i, j, current_cluster_id)
                    current_cluster_id += 1
        return current_cluster_id

    def _flood_fill(self, i, j, cluster_id):
        to_fill = [(i, j)]
        while to_fill:
            x, y = to_fill.pop()
            if self.cluster_ids[x, y] == -1:
                self.cluster_ids[x, y] = cluster_id
                neighbors = self._get_neighbors(x, y)
                for nx, ny in neighbors:
                    if self.grid[nx, ny] and self.cluster_ids[nx, ny] == -1:
                        to_fill.append((nx, ny))

    def _get_neighbors(self, x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.nx - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.ny - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def percolates(self):
        top_clusters = set(self.cluster_ids[0, self.grid[0, :]])
        bottom_clusters = set(self.cluster_ids[-1, self.grid[-1, :]])
        return not top_clusters.isdisjoint(bottom_clusters)

class PercolatorWidget:
    def __init__(self, percolator):
        self.percolator = percolator
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.35)
        self.canvas = self.ax.imshow(self.percolator.grid, cmap='Greys', interpolation='nearest')

        # Adding a new axes for the labels
        self.iter_label = self.fig.text(0.02, 0.02, f'Iterations: {self.percolator.iterations}', transform=self.fig.transFigure)
        self.percolation_label = self.fig.text(0.5, 0.02, f'Percolates: {self.percolator.percolates()}', transform=self.fig.transFigure)

        ax_next = plt.axes([0.8, 0.1, 0.1, 0.05])
        self.btn_next = Button(ax_next, 'Next')
        self.btn_next.on_clicked(self.next_step)

        ax_p = plt.axes([0.1, 0.15, 0.65, 0.03])
        self.slider_p = Slider(ax_p, 'p', 0.0, 1.0, valinit=self.percolator.p)
        self.slider_p.on_changed(self.update_p)

    def next_step(self, event):
        self.percolator.next()
        self.percolator.cluster()
        self.update_canvas()

    def update_p(self, val):
        self.percolator.p = self.slider_p.val
        self.next_step(None)

    def update_canvas(self):
        self.canvas.set_data(self.percolator.grid)
        self.iter_label.set_text(f'Iterations: {self.percolator.iterations}')
        self.percolation_label.set_text(f'Percolates: {self.percolator.percolates()}')
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

if __name__ == "__main__":
    percolator = Percolator(nx=200, ny=200, p=0.5)
    widget = PercolatorWidget(percolator)
    widget.show()

