from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); n=30; x=rng.uniform(-5,5,(n,2)); v=np.zeros_like(x); p=x.copy(); f=lambda z:(z*z).sum(1); ps=f(p); g=p[np.argmin(ps)].copy()
    for _ in range(100):
        v=.7*v+1.4*rng.random((n,2))*(p-x)+1.4*rng.random((n,2))*(g-x); x=np.clip(x+v,-5,5); s=f(x); mask=s<ps; p[mask]=x[mask];ps[mask]=s[mask];g=p[np.argmin(ps)].copy()
    save({'x':g.tolist(),'objective':float((g*g).sum())})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
