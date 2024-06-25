import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class IsingModelWidget:
    def __init__(self, model):
        self.model = model
        self.fig, self.ax = plt.subplots()
        self.image = self.ax.imshow(model.array, cmap='gray', vmin=-1, vmax=1)
        #self.animation = FuncAnimation(self.fig, self.update, frames=200, interval=50, repeat=False)
        self.animation = FuncAnimation(self.fig, self.update, frames=None, interval=5, repeat=False)
        plt.show()

    def update(self, frame):
        self.model.next()
        self.image.set_data(self.model.array)
        return self.image,

class IsingModel:
    def __init__(self, NX=400, NY=400, tau=5.0):
        self.NX = NX     # x-dimension
        self.NY = NY
        self.tau = tau   # temperature
        self.eps = -1    # ferromagnet. Not antiferromagnet.
        self.array = np.zeros((NX, NY), dtype=int)
        self.m = 0       # magnetisation
        self.u = 0.0     # internal energy

        # Initialize spins randomly and compute magnetization
        self.m = 0
        self.u = 0.0
        for i in range(self.NX):
            for j in range(self.NY):
                x = 1 if np.random.rand()>0.5 else -1
                self.array[i,j]=x
                self.m+=x
                for ip in range(i-1, i+2):
                    IP = ip % self.NX   # neighbour
                    for jp in range(j-1, j+2):
                        JP = jp % self.NY # neighbour
                        self.u += self.eps * self.array[i, j] * self.array[IP, JP]
                        # This works because the energy is only counted when both
                        # spins in the pair are initialized.  Before that, one of
                        # the indices is zero and will give no contribution.
 

    def next(self):
        if self.tau == 0.0:
            return

        N=self.NX*self.NY
        print(f"Temp {self.tau}, Mag {self.m/N}, Energy {self.u/N}")
        i = np.random.randint(0, self.NX)
        j = np.random.randint(0, self.NY)

        dE = 0
        for d in [-1, 1]:
            dE -= self.eps * self.array[i, j] * self.array[(i+d) % self.NX, j]
            dE -= self.eps * self.array[i, j] * self.array[i, (j+d) % self.NY]

        # Hastings-Metropolis 
        if dE <= 0 or np.exp(-dE / self.tau) > np.random.rand():
            self.array[i, j] *= -1
            self.m += 2 * self.array[i, j]
            #self.u -= 2 * dE
            self.u += 2 * dE

if __name__ == "__main__":
    #model = IsingModel(NX=100, NY=100, tau=2.0)
    model = IsingModel(NX=100, NY=100, tau=0.5)
    widget = IsingModelWidget(model)

