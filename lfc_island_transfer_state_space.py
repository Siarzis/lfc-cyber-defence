from control import *
import matplotlib.pyplot as plt

# In this script, the Load Frequency Control system of a single
# area is defined by its state-space representation

# Parameters
D, M = 1, 10
Tg = 0.1
Tt = 0.3
R = 0.05
beta = 20

# integral controller gain
K = 0.9

# State, input, output matrices
A = [[-D/M, 1/M, 0, 0],
	 [0, -1/Tt, 1/Tt, 0],
	 [-1/(R*Tg), 0, -1/Tg, -K/Tg],
	 [beta, 0, 0, 0]
	]

B = [[-1/M],
	 [0],
	 [0],
	 [0]
	]

C = [[1, 0, 0, 0],
	 [0, 0, 0, 1.0],
	]

# Attack matrix
F = [[0],
	 [0],
	 [0],
	 [1]
	]

manual = 1
attack = 1

if attack == 0:
	island_lfc = ss(A, B, C, 0)

	if manual == 0:
		response = step_response(island_lfc)
		plt.plot(response.time, response.outputs[0][0])
	elif manual == 1:
		T = np.arange(0, 30, 0.1, dtype=float).tolist()
		U = [np.ones_like(T)]

		t, y = forced_response(island_lfc, T=T, U=U)
		plt.plot(t, y[0])
elif attack == 1:
	BF = np.hstack([B, F]).tolist()
	island_lfc = ss(A, BF, C, 0)

	if manual == 0:
		response = step_response(island_lfc)
		plt.plot(response.time, response.outputs[0][0])
	elif manual == 1:
		attack_time = 100

		T = np.arange(0, 30, 0.1, dtype=float).tolist()
		attack_array = np.append(np.zeros_like(T[:attack_time]), np.sin(T[attack_time:]))
		U = [np.zeros_like(T), attack_array]

		t, y = forced_response(island_lfc, T=T, U=U)
		plt.plot(t, y[0])

plt.grid()
plt.show()