"""Supervisor journals process state; interrupted supervisors remain explicitly incomplete."""
from pathlib import Path
import argparse, datetime, json, subprocess, sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('route',choices=['markitdown','pymupdf-no-ocr','pymupdf-rapidocr','marker'])
    p.add_argument('--out',required=True)
    p.add_argument('--llama-server');p.add_argument('--model');p.add_argument('--mmproj')
    p.add_argument('--timeout',type=int,default=900)
    a=p.parse_args();out=Path(a.out).resolve()
    if out.exists():p.error('Use a NEW output directory; historical evidence is never overwritten')
    out.parent.mkdir(parents=True,exist_ok=True)
    log=out.with_name(out.name+'-console.log')
    cmd=[sys.executable,'-u',str(Path(__file__).with_name('run_route.py')),a.route,'--out',str(out)]
    for key,value in [('llama-server',a.llama_server),('model',a.model),('mmproj',a.mmproj)]:
        if value:cmd += ['--'+key,value]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    journal=out.with_name(out.name+'-supervisor.json')
    journal.write_text(json.dumps({'utc_started':started,'state':'started','exit_code':None,'note':'No completed record means process exit remains unknown.'},indent=2),encoding='utf8')
    with log.open('xb') as stream:
        proc=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT)
        try:code=proc.wait(timeout=a.timeout);timed_out=False
        except subprocess.TimeoutExpired:
            proc.terminate();code=proc.wait();timed_out=True
    status={'utc_started':started,'exit_code':code,'timed_out':timed_out,'console_file':log.name,
            'note':'Inspect conversion.json and raw.md separately; checkpoint presence is not full accuracy.'}
    out.mkdir(exist_ok=True)
    (out/'process.json').write_text(json.dumps(status,indent=2),encoding='utf8')
    journal.write_text(json.dumps(dict(status,state='completed'),indent=2),encoding='utf8')
    print(json.dumps(status),flush=True)
    return 0 if code==0 and not timed_out else 1

if __name__=='__main__':raise SystemExit(main())
