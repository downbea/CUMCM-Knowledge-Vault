from pathlib import Path
import json, numpy as np, pandas as pd
from sklearn.impute import KNNImputer

def main():
    df=pd.DataFrame({'x':[1,np.nan,3,4],'y':[2,4,np.nan,8]})
    result=pd.DataFrame(KNNImputer(n_neighbors=2).fit_transform(df),columns=df.columns)
    save({'before_missing':df.isna().sum().to_dict(),'after_missing':result.isna().sum().to_dict(),'values':result.round(3).to_dict('list')})

def save(obj):
    out=Path(__file__).parent/'output'; out.mkdir(exist_ok=True); (out/'result.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
