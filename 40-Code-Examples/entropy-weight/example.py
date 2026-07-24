from pathlib import Path
import json, numpy as np

def main():
    X=np.array([[80,60,90],[70,85,75],[95,65,80]],float)
    Z=(X-X.min(0))/(X.max(0)-X.min(0)+1e-12); P=Z/(Z.sum(0)+1e-12); n=len(X)
    E=-(P*np.log(P+1e-12)).sum(0)/np.log(n); d=1-E; w=d/d.sum()
    save({'weights':w.tolist(),'entropy':E.tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
