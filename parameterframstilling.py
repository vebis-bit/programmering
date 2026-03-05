import matplotlib.pyplot as plt
import numpy as np
def x(x0, r_x,t):
    return x0 + r_x * t
def y(y0,r_y,t):
    return y0 + r_y * t

A = (1,2)
B = (1,9)
r1 = (3,4)
r2 = (9,1)
t = np.linspace(-20,20,100)

plt.plot(x(A[0],r1[0],t),y(A[1],r1[1],t), label='Parametrisk kurve l')
plt.plot(A[0], A[1], 'ro', label='Startpunkt A')
plt.plot(B[0], B[1], 'bo', label='Startpunkt B')
plt.plot(x(B[0],r2[0],t),y(B[1],r2[1],t), 'g--', label='parametrisk kurve m')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()
