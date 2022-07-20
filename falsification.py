import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from SIR import *
from moonlight import *
from PID import *

def oscillations(T):
    osc = [(T[i] - T[i-1]) for i in range(1, len(T))]
    return osc


script = """
signal {real o;}
domain minmax;
formula emergency = globally (o < 1000);
"""
moonlightScript = ScriptLoader.loadFromText(script)
# monitoring the properties
monitor = moonlightScript.getMonitor("emergency")
sir = SIR()
K_p = 3.8
K_i = 0.02
K_d = 0
t = np.arange(0, 365, 1)
def findMinimum(N):
    minSTL = float('Inf')
    vRob = float('Inf')
    for i in range(N):
        k_p = K_p + np.random.normal(K_p, scale=K_p/10)
        k_i = K_i + np.random.normal(K_i, scale=K_i/10)
        pid_controller = PID(sir, Kp=k_p, Ki=k_i, Kd=K_d)
        S, I, R, u = pid_controller.pid(10**4, t)
        oscillation = oscillations(I)
        o_signal = [[yy] for yy in oscillation]
        result = monitor.monitor(list(t[:-1].astype(np.float64)),o_signal)
        stl =  result[0][1]
        if (stl < minSTL):
            minSTL = stl
            vSTL = [k_p, k_i]
        if minSTL < 0:
            break

    print('minSTL parameter: ' + str(vSTL))
    print('minSTL: ' + str(minSTL))
    return S, I, R, u

N = 100
S, I, R, u  = findMinimum(N)
u[-1] = u[-2]
plt.plot(t,u)
plt.xlabel('days')
plt.ylabel('R0')
plt.savefig('fals_1.png')
script = """
signal {real y;}
domain minmax;
formula prolonged_overshoot = !{globally [0.0, 10]  (y > 1000)};
"""

def findMinimum(N):
    minSTL = float('Inf')
    for i in range(N):
        k_p = K_p + np.random.normal(K_p, scale=K_p/10)
        k_i = K_i + np.random.normal(K_i, scale=K_i/10)
        pid_controller = PID(sir, Kp=k_p, Ki=k_i, Kd=K_d)
        S, I, R, u = pid_controller.pid(10**4, t)
        y_signal = [[yy] for yy in I]
        result = monitor.monitor(list(t[:-1].astype(np.float64)),y_signal)
        stl =  result[0][1]
        if (stl < minSTL):
            minSTL = stl
            vSTL = [k_p, k_i]
        if minSTL < 0:
            break

    print('minSTL parameter: ' + str(vSTL))
    print('minSTL: ' + str(minSTL))
    return S, I, R, u

N = 100
S, I, R, u  = findMinimum(N)
u[-1] = u[-2]
plt.clf()
plt.plot(t,u)
plt.xlabel('days')
plt.ylabel('R0')
plt.savefig('fals_2.png')
