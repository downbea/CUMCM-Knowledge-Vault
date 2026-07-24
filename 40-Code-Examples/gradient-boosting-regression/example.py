from pathlib import Path
import json
from sklearn.datasets import make_friedman1
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import cross_val_score

def main():
    X,y=make_friedman1(n_samples=220,noise=1,random_state=2026); m=HistGradientBoostingRegressor(max_iter=120,random_state=2026)
    rmse=(-cross_val_score(m,X,y,cv=5,scoring='neg_root_mean_squared_error')).mean(); save({'cv_rmse':rmse})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
