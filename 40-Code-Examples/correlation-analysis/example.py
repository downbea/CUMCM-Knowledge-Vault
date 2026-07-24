from pathlib import Path
import json, numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

def main():
    x=np.arange(1,11); y=x**2+np.array([0,1,-1,1,0,-2,2,0,1,-1])
    save({'pearson':pearsonr(x,y).statistic,'spearman':spearmanr(x,y).statistic,'kendall':kendalltau(x,y).statistic})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
