from SIR import *
from PID import *
import numpy as np


def overshoot(x, ref):
    over = round(max(x) - ref, 3)
    return over


def rise_time(x, t, ref):
    ref = np.array([ref for i in range(len(x))])
    idx = min(np.where(np.abs(x - ref) < 10))
    rise = t[idx]
    return rise


def steady_state_error(x, ref):
    error = round(np.abs(x[-1] - ref), 3)
    return error


def settling_time(x, t):
    idx = np.where(np.abs(x - x[-1]) < 1)[0]  # put 1 as parameters
    idx = [j for i, j in enumerate(idx) if abs(j - idx[min(i + 1, len(idx) - 1)]) < 2]
    i = min(idx)
    time = t[i]
    return time

sir = SIR()
pid_controller = PID(sir, Kp=3.8, Ki=0.02, Kd=0)
t = np.arange(0, 365, 1)
S, I, R, u = pid_controller.pid(10**4, t)
print(f'rise time:{rise_time(I, t, 10**4)}')
print(f'overshoot:{overshoot(I, 10**4)}')
print(f'steady_state_error:{steady_state_error(I, 10**4)}')
print(f'settling_time:{settling_time(I, t)}')
