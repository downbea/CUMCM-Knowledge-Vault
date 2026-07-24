from pathlib import Path
import json, numpy as np
from scipy.integrate import solve_ivp

def main():
    beta,gamma=.3,.1
    def f(t,y):S,I,R=y;return [-beta*S*I,beta*S*I-gamma*I,gamma*I]
    sol=solve_ivp(f,[0,160],[.99,.01,0],t_eval=np.linspace(0,160,321)); peak=int(np.argmax(sol.y[1]));save({'R0':beta/gamma,'peak_time':float(sol.t[peak]),'peak_infected':float(sol.y[1,peak])})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
