from __future__ import annotations
from pathlib import Path
import runpy, json, time, traceback

root=Path(__file__).resolve().parents[1]/'40-Code-Examples'
rows=[]
for script in sorted(root.glob('*/example.py')):
    t=time.time()
    try:
        runpy.run_path(str(script),run_name='__main__'); rc=0; err=''
    except Exception:
        rc=1; err=traceback.format_exc()[-2000:]
    rows.append({'name':script.parent.name,'returncode':rc,'seconds':round(time.time()-t,3),'stderr':err})
out=Path(__file__).parent/'seed-example-validation.json'
out.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
failed=[x for x in rows if x['returncode']]
print(json.dumps({'total':len(rows),'failed':len(failed),'seconds':round(sum(x['seconds'] for x in rows),3),'report':str(out)},ensure_ascii=False,indent=2))
raise SystemExit(1 if failed else 0)
