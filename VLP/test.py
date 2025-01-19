from Poettmann_Carpenter import poettmann_carpenter
from PVT.PVT import pvt_table
import matplotlib.pyplot as plt

qo = 2000
gor = 1200
fw = 0.25
thp = 500
tht = 39
id = 1.661
shoe = 1650

pressure_grad = poettmann_carpenter(qo, gor, fw, pvt_table, thp, tht, id, shoe, 200)
plt.plot(pressure_grad['Depth'], pressure_grad['Pressure'])
plt.show()
