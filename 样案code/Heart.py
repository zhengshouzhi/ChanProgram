# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

X = np.arange(-5.0, 5.0, 0.1)
Y = np.arange(-5.0, 5.0, 0.1)

x, y = np.meshgrid(X, Y)
f = 17 * x ** 2 - 16 * np.abs(x) * y + 17 * y ** 2 - 225

fig = plt.figure()
cs = plt.contour(x, y, f, 0, colors = 'r')
plt.xlabel('WangXiaoMei')
plt.show()