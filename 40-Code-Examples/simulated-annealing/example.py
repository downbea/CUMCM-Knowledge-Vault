from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); f=lambda x:(x-2)**2+np.sin(5*x); x=8.;fx=f(x);best=(x,fx);T=5.
    for _ in range(2500):
        y=x+rng.normal(scale=.5); fy=f(y)
        if fy<fx or rng.random()<np.exp((fx-fy)/T):x,fx=y,fy
        if fx<best[1]:best=(x,fx)
        T*=.997
    save({'x':best[0],'objective':best[1]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
