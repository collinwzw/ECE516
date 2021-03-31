import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread("./1s.JPG",0)
img2 = cv2.imread("./2s.JPG",0)
comparagram = np.zeros((256,256))
for i in range(img1.shape[0]):
    for j in range(img1.shape[1]):
        x = img1[i][j]
        y = img2[i][j]
        comparagram[y][x] += 1
print(np.sum(comparagram))
comparagram = np.log(comparagram)
xlist = []
ylist = []
for i in range(256):
    for j in range(256):
        if comparagram[i][j] >= 7:
            xlist.append(256 - i)
            ylist.append(j)
xlist = np.log(xlist)
ylist = np.log(ylist)
plt.plot(xlist,ylist,'o')
z = np.polyfit(xlist, ylist, 1)
p = np.poly1d(z)
plt.plot(x,p(x),"r--")
# the line equation:
print("y=%.6fx+(%.6f)"%(z[0],z[1]))
#plt.plot(xlist,ylist)
plt.show()
plt.imshow(comparagram,interpolation='none',origin='lower')
# plt.colorbar()
# plt.show()
