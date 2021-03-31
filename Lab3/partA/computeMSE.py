import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

image1 = mpimg.imread("both.jpg")
files = os.listdir("./")
p = []
MSE = []

for file in files:
    filename, extension = file.split('.')
    if extension == 'ppm':
        image2= mpimg.imread(file)
        p.append(int(filename)/10)
        MSE.append(mse(image1, image2))

minIndex = MSE.index(min(MSE))

plt.plot(p,MSE)
plt.xlabel('p')
plt.ylabel('MSE')
plt.title("MSE vs p")
plt.text(p[minIndex],MSE[minIndex], "Minimum MSE at p = " + str(p[minIndex]))
plt.show()

