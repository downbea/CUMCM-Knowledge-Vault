from pathlib import Path
import json
from scipy.optimize import linprog

def main():
    res=linprog(c=[-3,-2],A_ub=[[1,1],[2,1]],b_ub=[4,6],bounds=[(0,None),(0,None)],method='highs')
    save({'success':res.success,'x':res.x.tolist(),'maximum':-res.fun,'slack':res.slack.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
