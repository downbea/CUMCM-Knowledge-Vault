from pathlib import Path
import json, numpy as np

def main():
    X=np.array([[80,60,90],[70,85,75],[95,65,80],[88,75,92]],float)
    Z=(X-X.min(0))/(X.max(0)-X.min(0)+1e-12); s=Z.std(0,ddof=1); corr=np.corrcoef(Z,rowvar=False)
    info=s*((1-corr).sum(0)); w=info/info.sum(); save({'weights':w.tolist(),'information':info.tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
