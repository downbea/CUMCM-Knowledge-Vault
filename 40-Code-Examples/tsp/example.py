from pathlib import Path
import json, itertools, numpy as np

def main():
    pts=np.array([[0,0],[1,0],[1,1],[0,1],[.5,1.6]],float);D=np.linalg.norm(pts[:,None,:]-pts[None,:,:],axis=2);best=None
    for perm in itertools.permutations(range(1,len(pts))):
        route=(0,)+perm+(0,);dist=sum(D[a,b] for a,b in zip(route[:-1],route[1:]));
        if best is None or dist<best[0]:best=(dist,route)
    save({'distance':best[0],'route':best[1]})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
