from pathlib import Path
import json, numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def main():
    t=np.arange(60); y=.4*t+np.sin(t/3); X=t.reshape(-1,1); rmses=[]
    for tr,te in TimeSeriesSplit(n_splits=5).split(X):
        m=LinearRegression().fit(X[tr],y[tr]);rmses.append(mean_squared_error(y[te],m.predict(X[te]))**.5)
    save({'fold_rmse':rmses,'mean_rmse':float(np.mean(rmses))})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
