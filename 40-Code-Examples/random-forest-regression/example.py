from pathlib import Path
import json
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

def main():
    X,y=make_regression(n_samples=200,n_features=6,noise=10,random_state=2026); m=RandomForestRegressor(n_estimators=120,random_state=2026,n_jobs=1)
    rmse=(-cross_val_score(m,X,y,cv=5,scoring='neg_root_mean_squared_error')).mean(); m.fit(X,y)
    save({'cv_rmse':rmse,'feature_importance':m.feature_importances_.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
