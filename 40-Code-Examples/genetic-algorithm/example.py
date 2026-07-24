from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); pop=rng.uniform(-5,5,(60,2)); best=[]
    f=lambda x:np.sum(x*x,axis=1)
    for _ in range(80):
        fit=f(pop); elite=pop[np.argsort(fit)[:20]]; children=[]
        while len(children)<40:
            a,b=elite[rng.integers(0,len(elite),2)]; child=.5*(a+b)+rng.normal(0,.15,2); children.append(child)
        pop=np.vstack([elite,np.array(children)]); best.append(float(f(pop).min()))
    i=np.argmin(f(pop)); save({'x':pop[i].tolist(),'objective':float(f(pop)[i]),'last_best':best[-1]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
