from pathlib import Path
import json, numpy as np

def main():
    X=np.array([[80,60,90],[70,85,75],[95,65,80]],float); w=np.array([.4,.3,.3])
    Z=X/np.sqrt((X**2).sum(0)); V=Z*w; best=V.max(0); worst=V.min(0)
    dp=np.linalg.norm(V-best,axis=1); dn=np.linalg.norm(V-worst,axis=1); score=dn/(dp+dn)
    save({'scores':score.tolist(),'ranking':(np.argsort(-score)+1).tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
