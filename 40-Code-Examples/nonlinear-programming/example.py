from pathlib import Path
import json, numpy as np
from scipy.optimize import minimize

def main():
    f=lambda x:(x[0]-2)**2+(x[1]-1)**2
    cons={'type':'ineq','fun':lambda x:x[0]+x[1]-1}
    res=minimize(f,[0,0],constraints=cons,bounds=[(0,None),(0,None)],method='SLSQP')
    save({'success':res.success,'x':res.x.tolist(),'objective':res.fun})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
