from pathlib import Path
import json, numpy as np

def gm11(x0,n_forecast=2):
    x0=np.asarray(x0,float); x1=np.cumsum(x0); z=.5*(x1[1:]+x1[:-1]); B=np.c_[-z,np.ones(len(z))]
    a,b=np.linalg.lstsq(B,x0[1:],rcond=None)[0]; k=np.arange(len(x0)+n_forecast)
    x1hat=(x0[0]-b/a)*np.exp(-a*k)+b/a; x0hat=np.r_[x0[0],np.diff(x1hat)]; return x0hat,a,b

def main():
    x=np.array([100,112,126,141,158],float); pred,a,b=gm11(x,2); save({'a':a,'b':b,'fitted_and_forecast':pred.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
