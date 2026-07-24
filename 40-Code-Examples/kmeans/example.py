from pathlib import Path
import json
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def main():
    X,_=make_blobs(n_samples=180,centers=3,cluster_std=.7,random_state=2026); m=KMeans(n_clusters=3,n_init=20,random_state=2026).fit(X)
    save({'silhouette':silhouette_score(X,m.labels_),'centers':m.cluster_centers_.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
