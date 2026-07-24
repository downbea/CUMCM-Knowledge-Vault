from pathlib import Path
import json
from scipy.optimize import differential_evolution

def main():
    f=lambda x:(x[0]-1.5)**2+(x[1]+.5)**2
    r=differential_evolution(f,[(-5,5),(-5,5)],seed=2026,polish=True); save({'x':r.x.tolist(),'objective':r.fun})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
