from typing import Sequence

import numpy as np

from scipy.integrate import odeint
class SIR:
    def __init__(self):
        self.gamma = 1 / 30
        self.N = 10**7
        self.S0 = 10**7
        self.I0 = 1
        self.R0 = 0

    def odes(self,
             x: np.array,
             t: np.array,
             u: np.array):
        S, I, R = x
        R0 = u
        dSdt = - self.gamma * I * R0 * S/self.N
        dIdt = self.gamma * I * (R0 * S/self.N - 1)
        dRdt = self.gamma * I

        return [dSdt, dIdt, dRdt]

    def sim_step(self,
                 x: Sequence[np.array],
                 u: np.array,
                 ts: np.array,
                 S: np.array,
                 I: np.array,
                 R: np.array,
                 i: int):
        y = odeint(self.odes, x, ts, args=(u,))
        S[i + 1], I[i + 1], R[i + 1] = y[1]
        x = S[i + 1], I[i + 1], R[i + 1]
        return x

    def simulate(self,
                 u: np.array,
                 t: np.array):
        x = [self.S0, self.I0, self.R0]
        S = np.ones(len(t)) * x[0]
        I = np.ones(len(t)) * x[1]
        R = np.ones(len(t)) * x[2]
        for i in range(len(t) - 1):
            ts = [t[i], t[i + 1]]
            x = self.sim_step(x, u[i], ts, S, I, R, i)
        return S, I, R


