from pathlib import Path
import json
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture

def main():
    X,_=make_blobs(n_samples=180,centers=3,cluster_std=[.5,.8,1.0],random_state=2026); m=GaussianMixture(n_components=3,random_state=2026).fit(X)
    save({'bic':m.bic(X),'weights':m.weights_.tolist(),'means':m.means_.tolist()})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
