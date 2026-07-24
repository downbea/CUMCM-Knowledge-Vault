from pathlib import Path
import json, numpy as np

def main():
    A=np.array([[1,3,5],[1/3,1,2],[1/5,1/2,1]],float)
    vals,vecs=np.linalg.eig(A); k=np.argmax(vals.real); w=np.abs(vecs[:,k].real); w/=w.sum()
    n=len(A); ci=(vals[k].real-n)/(n-1); ri={1:0,2:0,3:.58,4:.90}[n]; cr=ci/ri if ri else 0
    save({'weights':w.tolist(),'lambda_max':vals[k].real,'CR':cr})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
