from pathlib import Path
import json, numpy as np
from scipy.optimize import linear_sum_assignment

def main():
    cost=np.array([[9,2,7],[6,4,3],[5,8,1]]);r,c=linear_sum_assignment(cost);save({'pairs':list(zip(r.tolist(),c.tolist())),'cost':int(cost[r,c].sum())})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
