from pathlib import Path
import json, numpy as np

def main():
    ref=np.array([1,2,3,4],float); X=np.array([[1.1,1.9,3.2,3.8],[.8,2.2,2.7,4.4]],float)
    D=np.abs(X-ref); dmin,dmax=D.min(),D.max(); rho=.5; coeff=(dmin+rho*dmax)/(D+rho*dmax); grade=coeff.mean(1)
    save({'grades':grade.tolist(),'coefficients':coeff.tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
