from pathlib import Path
import json, numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def main():
    t=np.arange(36); y=20+.5*t+3*np.sin(2*np.pi*t/12)
    m=ExponentialSmoothing(y,trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit()
    save({'forecast':m.forecast(6).tolist(),'sse':float(m.sse)})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
