from pathlib import Path
import json, numpy as np
from scipy.optimize import minimize_scalar

def main():
    rows=[]
    for w in np.linspace(0,1,11):
        f=lambda x:w*(x-1)**2+(1-w)*(x-4)**2; r=minimize_scalar(f,bounds=(0,5),method='bounded')
        rows.append({'weight':float(w),'x':float(r.x),'f1':float((r.x-1)**2),'f2':float((r.x-4)**2)})
    save({'pareto_samples':rows})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
