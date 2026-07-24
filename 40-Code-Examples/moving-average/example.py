from pathlib import Path
import json, numpy as np

def main():
    y=np.array([10,12,13,15,16,18,19],float); window=3
    fitted=np.convolve(y,np.ones(window)/window,mode='valid'); forecast=float(y[-window:].mean())
    save({'fitted':fitted.tolist(),'forecast':forecast})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
