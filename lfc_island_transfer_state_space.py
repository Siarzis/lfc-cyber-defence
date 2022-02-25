import numpy as np

from numpy.linalg import inv, matrix_rank

import cvxpy as cp

np.set_printoptions(precision=3, suppress=True)

# In this script, the Load Frequency Control system of a single
# area is defined by its state-space representation

# parameters
D, M = 1, 10
Tg = 0.1
Tt = 0.3
R = 0.05
beta = 20

# integral controller gain
K = 0.9

# state, input, output matrices
A = [[-D/M, 1/M, 0, 0],
	 [0, -1/Tt, 1/Tt, 0],
	 [-1/(R*Tg), 0, -1/Tg, 0],
	 [beta, 0, 0, 0]
	]

B = [[0],
	 [0],
	 [1/Tg],
	 [0]
	]

E = [[-1/M],
	 [0],
	 [0],
	 [0]
	]

C = [[1, 0, 0, 0],
	 [0, 0, 0, 1],
	]

# attack matrix
F = [[0],
	 [0],
	 [0],
	 [1]
	]

# check if the desired transformation exists
if matrix_rank(np.dot(C, E)) == matrix_rank(E):
	print('Transformation condition satisfied.')
else:
	print('Transformation does not exist.')

# dimensions of system matrices
n, m, p, r = len(A), len(B[0]), len(C), len(E[0])

# transformation matrices

# T is selected so that
# 		[1]
# TxE =	[0]
#		[0]
#		[0]

T = [[-10, 0, 0, -10],
	 [0, 3, 0.4, -6.3],
	 [0, 7.1, 1.4, 9.5],
	 [0, -4.3, 6.8, 4.2]
	]
T_inv = inv(T)

S = [[1, 1],
	 [0, 4],
	]

# calculate the system matrices under the new coordinate

A_t = np.dot(np.dot(T, A), T_inv)
B_t = np.dot(T, B)
E_t = np.dot(T, E)
C_t = np.dot(np.dot(S, C), T_inv)

print('TE =' + np.array2string(E_t, precision=2, separator=',',
                      suppress_small=True))
print('SCT-1 =' + np.array2string(C_t, precision=2, separator=',',
                      suppress_small=True))

# extract tranformed matrices
A1 = A_t[0:r,0:r]
A2 = A_t[0:r,r:n]
A3 = A_t[r:n,0:r]
A4 = A_t[r:n,r:n]

B1 = B_t[0:r,:]
B2 = B_t[r:n,:]

E1 = E_t[0:r,:]

C1 = C_t[0:r,0:r]
C4 = C_t[r:p,r:n]

# print(A_t)
# print(A1)
# print(A2)
# print(A3)
# print(A4)

# print(B_t)
# print(B1)
# print(B2)

# print(E_t)
# print(E1)

# print(C_t)
# print(C1)
# print(C4)

P1 = cp.Variable((r, r), PSD=True)
P2 = cp.Variable((n-r, n-r), PSD=True)
X = cp.Variable((r, r), PSD=True)
Y = cp.Variable((n-r, p-r))
F = cp.Variable((m, p-r))
alpha1 = cp.Variable((1,1))
gamma = cp.Variable((1,1))

a = alpha1

print(P1)
print(P1.T)

LMI1 = cp.bmat([
        [X + X.T, P1, P1@A2],
        [P1, -alpha1, np.zeros((r, n-r))],
        [A2.T@P1, np.zeros((n-r, r)), A4.T@P2+P2@A4-C4.T@Y.T-Y@C4+cp.diag(a)]
            ])

LMI2 = cp.bmat([
        [-cp.diag(gamma), (B2.T@P2-F@C4).T],
        [B2.T@P2-F@C4, -cp.diag(gamma)],
            ])

cons1 = LMI1 << 0
cons2 = LMI2 << 0

cons3 = P1 >> 0
cons4 = P1 >> 0
cons5 = alpha1 >> 0

optprob = cp.Problem(cp.Minimize(gamma), constraints=[cons1, cons2, cons3,cons4, cons5])
optprob.solve()

P1op = P1.value
P2op = P2.value
Fop = F.value
Xop = X.value
Yop = Y.value

