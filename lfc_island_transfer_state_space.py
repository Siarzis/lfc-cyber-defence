from control import *
from numpy.linalg import inv, solve
import matplotlib.pyplot as plt

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
AB = [[-D/M, 1/M, 0, 0],
	 [0, -1/Tt, 1/Tt, 0],
	 [-1/(R*Tg), 0, -1/Tg, -K/Tg],
	 [beta, 0, 0, 0]
	]

E = [[-1/M],
	 [0],
	 [0],
	 [0]
	]

C = [[1, 0, 0, 0],
	 [0, 0, 0, 1.0],
	]

# attack matrix
F = [[0],
	 [0],
	 [0],
	 [1]
	]

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
	 [0, 0],
	]

# calculate the system matrices under the new coordinate

A_t = np.dot(np.dot(T, AB), T_inv)
B_t = 1
E_t = np.dot(T, E)
C_t = np.dot(np.dot(S, C), T_inv)

print(A_t)
print(E_t)
print(C_t)

manual = 1
attack = 1

if attack == 0:
	island_lfc = ss(AB, E, C, 0)

	if manual == 0:
		response = step_response(island_lfc)
		plt.plot(response.time, response.outputs[0][0])
	elif manual == 1:
		T = np.arange(0, 30, 0.1, dtype=float)
		U = [np.ones_like(T)]

		t, y = forced_response(island_lfc, T=T, U=U)
		plt.plot(t, y[0])
elif attack == 1:
	EF = np.hstack([E, F]).tolist()
	island_lfc = ss(AB, EF, C, 0)

	if manual == 0:
		response = step_response(island_lfc)
		plt.plot(response.time, response.outputs[0][0])
	elif manual == 1:
		attack_time = 100

		T = np.arange(0, 30, 0.1, dtype=float)
		attack_array = np.append(np.zeros_like(T[:attack_time]), np.sin(T[attack_time:]))
		U = [np.zeros_like(T), attack_array]

		t, y = forced_response(island_lfc, T=T, U=U)
		plt.plot(t, y[0])

plt.grid()
# plt.show()