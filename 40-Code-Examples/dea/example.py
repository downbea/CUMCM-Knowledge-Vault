from pathlib import Path
import json, numpy as np
from scipy.optimize import linprog

def dea_input_efficiency(X,Y,o):
    n,m=X.shape; s=Y.shape[1]
    c=np.r_[np.zeros(n),1.0]
    A=[]; b=[]
    for i in range(m): A.append(np.r_[-X[:,i],-X[o,i]]); b.append(0)
    for r in range(s): A.append(np.r_[Y[:,r],0]); b.append(Y[o,r])
    Aeq=[np.r_[np.ones(n),0]]; beq=[1]
    res=linprog(c,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*n+[(0,None)],method='highs')
    return float(res.x[-1])
def main():
    X=np.array([[2,3],[3,2],[4,4]],float);Y=np.array([[5],[5],[6]],float)
    save({'efficiency':[dea_input_efficiency(X,Y,i) for i in range(len(X))]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
