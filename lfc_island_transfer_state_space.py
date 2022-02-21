from control import *
import matplotlib.pyplot as plt

# In this script, the Load Frequency Control system of a single
# area is defined by its State Space representation

# Parameters
D, M = 1, 10
Tg = 0.1
Tt = 0.3
R = 0.05
beta = 20

# integral controller gain
K = 0.9

A = [[-D/M, 1/M, 0, 0],
	 [0, -1/Tt, 1/Tt, 0],
	 [-1/(R*Tg), 0, -1/Tg, -K/Tg],
	 [beta, 0, 0, 0]
	]

B = [[-1/M],
	 [0,],
	 [0,],
	 [0]
	]

C = [[1, 0, 0, 0],
	 [0, 0, 0, 1.0],
	]

island_lfc = ss(A, B, C, 0)

response = step_response(island_lfc)

plt.plot(response.time, response.outputs[1][0])
plt.grid()

plt.show()