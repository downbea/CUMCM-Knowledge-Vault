from pathlib import Path
import json, numpy as np

def main():
    rng=np.random.default_rng(2026); n=200000; xy=rng.random((n,2)); pi=4*np.mean((xy*xy).sum(1)<=1); se=4*np.sqrt((pi/4)*(1-pi/4)/n)
    save({'pi_estimate':pi,'standard_error':se,'n':n})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
