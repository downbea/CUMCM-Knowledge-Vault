from pathlib import Path
import json
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def main():
    X,y=make_classification(n_samples=240,n_features=8,n_informative=5,random_state=2026); m=RandomForestClassifier(n_estimators=120,random_state=2026,n_jobs=1)
    save({'cv_auc':cross_val_score(m,X,y,cv=5,scoring='roc_auc').mean(),'cv_f1':cross_val_score(m,X,y,cv=5,scoring='f1').mean()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
