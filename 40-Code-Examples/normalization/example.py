from pathlib import Path
import json, numpy as np

def main():
    x=np.array([[10,100],[20,80],[30,60]],float)
    benefit=(x-x.min(0))/(x.max(0)-x.min(0))
    cost=(x.max(0)-x)/(x.max(0)-x.min(0))
    z=(x-x.mean(0))/x.std(0,ddof=0)
    save({'benefit':benefit.tolist(),'cost':cost.tolist(),'zscore':z.tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
