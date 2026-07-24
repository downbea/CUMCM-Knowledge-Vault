from pathlib import Path
import json, numpy as np

def main():
    weights=np.array([.4,.35,.25]); R=np.array([[.6,.3,.1],[.2,.6,.2],[.3,.4,.3]])
    B=weights@R; levels=np.array([100,80,60]); score=float(B@levels)
    save({'membership':B.tolist(),'score':score,'level':int(np.argmax(B))})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
