import numpy as np
import matplotlib.pyplot as plt

def create_histograms():
    num_samples = 1000000
    num_bins = 1000
    x_range = (-10, 10)
    uniform_samples = np.random.uniform(-1.0, 1.0, (num_samples, 4))
    
    histograms = []
    titles = ["One uniform variate", "Two uniform variates", "Three uniform variates", "Four uniform variates"]
    for i in range(4):
        samples_sum = np.cumsum(uniform_samples[:, :i+1], axis=1)[:, -1]
        hist, bins = np.histogram(samples_sum, bins=num_bins, range=x_range)
        histograms.append((hist, bins, titles[i]))
    
    return histograms

class InteractivePlot:
    def __init__(self, histograms):
        self.histograms = histograms
        self.current_view = 0
        
        self.figure, self.ax = plt.subplots()
        print("Press 'n' to shift to next plot")
        self.figure.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        self.show_histogram(self.current_view)
        plt.show()
    
    def show_histogram(self, index):
        self.ax.clear()
        hist, bins, title = self.histograms[index]
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        self.ax.bar(bin_centers, hist, width=(bins[1] - bins[0]), edgecolor='black')
        self.ax.set_ylim(0, 12000)
        self.ax.set_title(title, fontsize=16, family='sans-serif')
        self.ax.set_xlabel('x', fontsize=16, family='sans-serif')
        self.ax.set_ylabel('counts', fontsize=16, family='sans-serif')
        
        self.figure.canvas.draw()
    
    def on_key_press(self, event):
        if event.key == 'n':
            self.current_view = (self.current_view + 1) % len(self.histograms)
            self.show_histogram(self.current_view)

if __name__ == "__main__":
    histograms = create_histograms()
    InteractivePlot(histograms)

