from control import *
import matplotlib.pyplot as plt

s = tf('s')

# In this script, the Load Frequency Control system of a single
# area is defined by its Transfer Function. The system converges

# Parameters
Kps1, Tps1 = 120, 20
Kg1, Tg1 = 1, 0.08
Kt1, Tt1 = 1, 0.5
R1 = 2.4
B1 = 0.425


A = [[-1/Tps1, Kps1/Tps1, 0, 0, 0, 0, -Kps1/Tps1, 0, 0],
	 [0, -1/Tt1, 1/Tt1, 0, 0, 0, 0, 0, 0],
	 [-1/(R1*Tg1), 0, -1/Tg1, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, -1/Tps2, Kps2/Tps2, 0, -a12*Kps2/Tps2, 0, 0],
	 [0, 0, 0, 0, -1/Tt2, 1/Tt2, 0, 0, 0],
	 [0, 0, 0, -1/(R2*Tg2), 0, -1/Tg2, 0, 0, 0],
	 [T12, 0, 0, -T12, 0, 0, 0, 0, 0],
	 [B1, 0, 0, 0, 0, 0, 1, 0, 0],
	 [0, 0, 0, B2, 0, 0, a12, 0, 0]
	]

B = [[0, 0],
	 [0, 0],
	 [1/Tg1, 0],
	 [0, 0],
	 [0, 0],
	 [0, 1/Tg2],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

F = [[-Kps1/Tps1, 0],
	 [0, 0],
	 [0, 0],
	 [0, -Kps2/Tps2],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

BF = np.hstack([B, F]).tolist()

C = [[1.0, 0, 0, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 1.0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 1.0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 0, 1.0]
	]

from pprint import pprint
pprint(BF)


two_area_lfc = ss(A, BF, C, 0)

response = step_response(single_area)

plt.plot(response.time, response.outputs)
plt.grid()

plt.show()