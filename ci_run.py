"""Execute three light routes on a fresh runner; preserve raw text in public job logs."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path(__file__).resolve().parent
assert sys.prefix != sys.base_prefix, "Run inside a fresh dedicated venv"
os.chdir(root)
def call(*args):
 subprocess.run([sys.executable,*args],check=True)
call('-m','pip','install','--no-compile','-r','requirements-baseline.txt')
call('check_outputs.py')
for route in ['markitdown','pymupdf-no-ocr']:
 call('reproduce.py',route,'--out','runs/'+route)
call('-m','pip','install','--no-compile','-r','requirements-with-ocr.txt')
call('reproduce.py','pymupdf-rapidocr','--out','runs/pymupdf-rapidocr')
sections=['# Independent Windows VM: three light routes',
          'Marker is not executed by this workflow. One synthetic English specimen only.']
for route in ['markitdown','pymupdf-no-ocr','pymupdf-rapidocr']:
 path=root/'runs'/route
 raw=(path/'raw.md').read_bytes()
 expected=hashlib.sha256((root/('historical-'+route+'.md')).read_bytes()).hexdigest()
 actual=hashlib.sha256(raw).hexdigest()
 status=json.loads((path/'process.json').read_text())
 assert status['exit_code']==0 and not status['timed_out'],(route,status)
 assert actual==expected,(route,actual,expected)
 section='\n## '+route+'\n\nSHA256: '+actual+'\n\nProcess: '+json.dumps(status)+'\n\nUntouched UTF-8 output:\n\n````markdown\n'+raw.decode('utf8')+'\n````\n'
 print(section,flush=True);sections.append(section)
freeze=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)
print(freeze,flush=True)
sections.append('\n## Final dependency environment\n\n```text\n'+freeze+'\n```')
summary=os.environ.get('GITHUB_STEP_SUMMARY')
if summary:Path(summary).write_text('\n'.join(sections),encoding='utf8')
print('Three routes returned, exited 0, and matched their published historical hashes. Marker remains unverified on this VM.')
