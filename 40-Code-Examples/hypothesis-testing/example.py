from pathlib import Path
import json, numpy as np
from scipy.stats import ttest_ind, mannwhitneyu, shapiro

def main():
    a=np.array([10,11,12,9,10,13,12]); b=np.array([8,9,10,7,11,9,8])
    save({'shapiro_a_p':shapiro(a).pvalue,'t_test_p':ttest_ind(a,b,equal_var=False).pvalue,'mann_whitney_p':mannwhitneyu(a,b,alternative='two-sided').pvalue})

def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
