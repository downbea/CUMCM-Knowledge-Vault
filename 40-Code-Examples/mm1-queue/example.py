from pathlib import Path
import json

def main():
    lam,mu=4.,6.;rho=lam/mu;L=rho/(1-rho);W=1/(mu-lam);Lq=rho*rho/(1-rho);Wq=rho/(mu-lam)
    save({'utilization':rho,'L':L,'Lq':Lq,'W':W,'Wq':Wq})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
