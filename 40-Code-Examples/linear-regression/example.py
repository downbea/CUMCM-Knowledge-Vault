from pathlib import Path
import json, numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def main():
    rng=np.random.default_rng(2026); X=rng.normal(size=(80,2)); y=3+2*X[:,0]-1.5*X[:,1]+rng.normal(scale=.3,size=80)
    m=LinearRegression().fit(X,y); pred=m.predict(X)
    save({'intercept':m.intercept_,'coef':m.coef_.tolist(),'rmse':mean_squared_error(y,pred)**.5,'r2':m.score(X,y)})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
