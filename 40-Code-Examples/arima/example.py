from pathlib import Path
import json, numpy as np
from statsmodels.tsa.arima.model import ARIMA

def main():
    rng=np.random.default_rng(2026); y=np.cumsum(rng.normal(size=80))
    m=ARIMA(y,order=(1,1,1)).fit(); save({'aic':float(m.aic),'forecast':m.forecast(5).tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
