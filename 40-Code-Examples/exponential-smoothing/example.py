from pathlib import Path
import json, numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def main():
    y=np.array([10,12,13,15,16,18,19],float); m=SimpleExpSmoothing(y,initialization_method='estimated').fit(optimized=True)
    save({'alpha':m.params['smoothing_level'],'forecast':m.forecast(2).tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
