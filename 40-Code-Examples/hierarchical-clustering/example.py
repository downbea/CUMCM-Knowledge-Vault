from pathlib import Path
import json
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

def main():
    X,_=make_blobs(n_samples=120,centers=3,random_state=2026); labels=AgglomerativeClustering(n_clusters=3,linkage='ward').fit_predict(X)
    save({'silhouette':silhouette_score(X,labels),'counts':{str(i):int((labels==i).sum()) for i in set(labels)}})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
