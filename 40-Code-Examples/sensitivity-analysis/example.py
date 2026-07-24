from pathlib import Path
import json, numpy as np

def model(a,b):return a*a+2*b

def main():
    base={'a':2.,'b':3.}; rows=[]
    for name in base:
        for pct in [-.1,.1]:
            x=base.copy();x[name]*=1+pct;rows.append({'parameter':name,'pct':pct,'output':model(**x),'relative_output_change':model(**x)/model(**base)-1})
    save({'baseline':model(**base),'perturbations':rows})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
