from __future__ import annotations
from SIR import *
def smooth(u, target, sign):
    if sign == 1 and u < target:
        u += 1
    if sign == 0 and u > target:
        u -= 1

    return u
class PID:
    def __init__(self, model, Kp=None, Ki=None, Kd=None):
        self.model = model
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd


    def pid(self,
            ref: float,
            t: np.array):
        out = np.zeros(len(t))
        proc = np.zeros(len(t))
        e = np.zeros(len(t))
        ig = np.zeros(len(t))
        d = np.zeros(len(t))
        D = np.zeros(len(t))
        P = np.zeros(len(t))
        Ig = np.zeros(len(t))
        S = np.ones(len(t)) * self.model.S0
        I = np.ones(len(t)) * self.model.I0
        R = np.ones(len(t)) * self.model.R0
        u = np.ones(len(t)) * 10
        x0 = [self.model.S0, self.model.I0, self.model.R0]
        for i in range(len(t)-1):
            dt = t[i+1] - t[i]
            e[i] = (ref - proc[i])/ref
            if i > 0:
                ig[i] = ig[i - 1] + e[i] * dt
                d[i] = (e[i] - e[i - 1]) / dt
            P[i] = self.Kp * e[i]
            Ig[i] = self.Ki * ig[i]
            D[i] = self.Kd * d[i]
            out[i] = P[i] + Ig[i] + D[i]
            if i%14==0 and i > 0:
            # bounds for the controlled variable
               if out[i] > 10:
                   out[i] = 10
               if out[i] < 0.5:
                   out[i] = 0.5
               u[i] = out[i]
            else:
               u[i] = u[i - 1]

            ts = [t[i], t[i+1]]
            x0 = self.model.sim_step(x0, u[i], ts, S, I, R, i)
            proc[i + 1] = I[i + 1]

        return S, I, R, u