from pathlib import Path
import json

def knapsack(values,weights,cap):
    dp=[0]*(cap+1)
    for v,w in zip(values,weights):
        for c in range(cap,w-1,-1): dp[c]=max(dp[c],dp[c-w]+v)
    return dp[cap]
def main(): save({'optimal_value':knapsack([6,10,12],[1,2,3],5)})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
