from pathlib import Path
import json, numpy as np

def main():
    subjective=np.array([.5,.3,.2]); objective=np.array([.3,.4,.3]); alpha=.6
    w=alpha*subjective+(1-alpha)*objective; w/=w.sum(); save({'alpha':alpha,'weights':w.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
