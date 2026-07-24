from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); true=np.linspace(0,10,50); z=true+rng.normal(scale=1,size=50)
    x=0.;P=1.;Q=.05;R=1.; est=[]
    for obs in z:
        P=P+Q; K=P/(P+R); x=x+K*(obs-x); P=(1-K)*P; est.append(x)
    rmse=float(np.mean((np.array(est)-true)**2)**.5); save({'rmse':rmse,'last_estimate':est[-1]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
