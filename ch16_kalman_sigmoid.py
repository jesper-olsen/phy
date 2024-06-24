import sys
import numpy as np
from scipy.special import expit
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Define the parameters and their ranges
W = 0.8
THETA = 0.0

# Define the sigmoid function
def sigmoid(x, W, THETA):
    return (np.exp(W*x + THETA) - np.exp(-(W*x + THETA))) / (np.exp(W*x + THETA) + np.exp(-(W*x + THETA)))

# Generate data points with noise
np.random.seed(42)
x_values = np.arange(-5.0, 5.0, 0.2)
error = 0.05
y_values = sigmoid(x_values, W, THETA) + error * np.random.normal(size=x_values.shape)

# Plot the initial data
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.plot(x_values, y_values, 'bo', label='Data with noise')

# Initial plot of the sigmoid function
line, = ax.plot(x_values, sigmoid(x_values, W, THETA), 'r-', linewidth=2, label='Sigmoid fit')

# Update the parameters and replot
def update_plot(event):
    global W, THETA
    
    # Simulate progressive fit (simplified for demonstration purposes)
    for _ in range(1):  # Single iteration for simplicity
        for i in range(len(x_values)):
            xi = x_values[i]
            yi = y_values[i]
            sechS = 1.0 / np.cosh(W * xi + THETA)
            sech2S = sechS**2
            H = np.array([[sech2S * xi, sech2S]])
            R_inv = np.array([[1 / (error**2)]])
            A = np.array([W, THETA])
            CC = np.eye(2) * 0.5
            
            CCP_inv = np.linalg.inv(CC) + H.T @ R_inv @ H
            CCP = np.linalg.inv(CCP_inv)
            AP = CCP @ (np.linalg.inv(CC) @ A + H.T @ R_inv @ (H @ A + yi - sigmoid(xi, W, THETA)))
            
            W, THETA = AP
            
    line.set_ydata(sigmoid(x_values, W, THETA))
    fig.canvas.draw()

# Add a button for updating the plot
ax_button = plt.axes([0.81, 0.05, 0.1, 0.075])
button = Button(ax_button, 'Next')
button.on_clicked(update_plot)

ax.set_title('Sigmoid')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
plt.show()

