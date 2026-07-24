from pathlib import Path
import json, numpy as np
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.metrics import mean_absolute_error

def main():
    x=np.arange(30).reshape(-1,1); y=2*x.ravel()+1; y=y.astype(float); y[[5,20]] += [30,-35]
    lr=LinearRegression().fit(x,y); hb=HuberRegressor().fit(x,y)
    save({'ols_coef':lr.coef_[0],'huber_coef':hb.coef_[0],'ols_mae':mean_absolute_error(y,lr.predict(x)),'huber_mae':mean_absolute_error(y,hb.predict(x))})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
