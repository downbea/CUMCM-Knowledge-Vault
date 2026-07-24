from pathlib import Path
import json, numpy as np

def main():
    states=np.array([0,0,1,1,2,1,2,2,1,0,1]); P=np.zeros((3,3))
    for a,b in zip(states[:-1],states[1:]):P[a,b]+=1
    P=P/(P.sum(1,keepdims=True)+1e-12); dist=np.array([1.,0,0])@np.linalg.matrix_power(P,5)
    save({'transition':P.tolist(),'distribution_t5':dist.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
