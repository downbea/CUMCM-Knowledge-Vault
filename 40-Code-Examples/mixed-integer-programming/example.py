from pathlib import Path
import json, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def main():
    c=np.array([-5,-4.]); constraint=LinearConstraint([[6,4]],-np.inf,[24]); bounds=Bounds([0,0],[np.inf,np.inf])
    res=milp(c,integrality=[1,1],bounds=bounds,constraints=constraint)
    save({'success':res.success,'x':res.x.tolist(),'maximum':-res.fun})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
