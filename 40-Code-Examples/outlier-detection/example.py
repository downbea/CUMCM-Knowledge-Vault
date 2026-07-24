from pathlib import Path
import json, numpy as np
from sklearn.ensemble import IsolationForest

def main():
    x=np.array([10,11,9,10,12,100],dtype=float).reshape(-1,1)
    q1,q3=np.quantile(x,[.25,.75]); iqr=q3-q1
    iqr_flags=((x.ravel()<q1-1.5*iqr)|(x.ravel()>q3+1.5*iqr)).tolist()
    iso=(IsolationForest(contamination='auto',random_state=2026).fit_predict(x)==-1).tolist()
    save({'iqr_flags':iqr_flags,'isolation_forest_flags':iso})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
