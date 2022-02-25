import numpy as np
from numpy.linalg import eig, inv, solve

a = np.array([[0, 0, 1, 0, 0, 0, 0], 
			  [0, -0.154, -0.04, 1.54, 0, -0.744, -0.032],
			  [0, 0.249, -1, -5.2, 0, 0.337, -1.12],
			  [0.0386, -0.996, 0, -2.117, 0, 0.02, 0], 
			  [0, 0.5, 0, 0, -4, 0, 0],
			  [0, 0, 0, 0, 0, -20, 0], 
			  [0, 0, 0, 0, 0, 0, -25]])

T = np.array([[0.844, 0.156, 0.0405, -1.5598, 0, 0.7535, 0.0324], 
			  [-1, 1, 0, 0, 0, 0, 0],
			  [0, 0, 1, 0, 0, 0, 0],
			  [0, 0, 0, 1, 0, 0, 0], 
			  [-1, 0, 0, 0, 1, 0, 0],
			  [0, 0, 0, 0, 0, 1, 0], 
			  [0, 0, 0, 0, 0, 0, 1]])

w, v = eig(a)

np.set_printoptions(precision=1, suppress=True)

print(solve([[0.015, -0.028], [0.002, -0.03]], [0, 0]))

T_inv = [[-0.1, 0.1, -0.04, 0.003],
		 [0, 0.108, 0.082, -0.023],
		 [0, 0.131, 0.027, 0.135],
		 [0, -0.1, 0.04, -0.003]]

print(inv(T_inv))