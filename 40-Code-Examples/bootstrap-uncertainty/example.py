from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); x=rng.lognormal(mean=1,sigma=.5,size=60); stats=[]
    for _ in range(2000):stats.append(np.median(rng.choice(x,size=len(x),replace=True)))
    lo,hi=np.quantile(stats,[.025,.975]);save({'median':float(np.median(x)),'ci95':[float(lo),float(hi)]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
