from pathlib import Path
import json, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def main():
    rng=np.random.default_rng(2026); z=rng.normal(size=100); X=np.c_[z+.1*rng.normal(size=100),2*z+.2*rng.normal(size=100),rng.normal(size=100)]
    pca=PCA().fit(StandardScaler().fit_transform(X))
    save({'explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'components':pca.components_.tolist()})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
