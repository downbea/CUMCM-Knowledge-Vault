from pathlib import Path
import json
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

def main():
    X,_=make_moons(n_samples=180,noise=.08,random_state=2026); labels=DBSCAN(eps=.25,min_samples=5).fit_predict(StandardScaler().fit_transform(X))
    save({'clusters':len(set(labels))-(1 if -1 in labels else 0),'noise_count':int((labels==-1).sum())})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
