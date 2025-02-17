from Poettmann_Carpenter import poettmann_carpenter_2
from PVT.PVT import pvt_table
import matplotlib.pyplot as plt

qo = 400
gor = 1200
fw = 0.25
thp = 300
tht = 39
id = 1.661
shoe = 1600

# pressure_grad = poettmann_carpenter(qo, gor, fw, pvt_table, thp, tht, id, shoe, 500)
pressure_grad = poettmann_carpenter_2(qo, gor, fw, pvt_table, thp, tht, id, shoe, 500)
plt.plot(pressure_grad['Pressure'], pressure_grad['Depth'])
plt.gca().invert_yaxis()
plt.show()
