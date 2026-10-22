"""Fetch pinned upstream GGUF files and verify bytes; no credentials or conversion upload."""
from pathlib import Path
import argparse,hashlib,urllib.request
REV='6a3a4c30e5e74446d4f8b6afd05b2f2da970f470'
FILES={'surya-2.gguf':'1f18abe17b1ed8b4e47ee9b1ad0e274c93daf5efbb6b29a04ff1712e37051e05',
       'surya-2-mmproj.gguf':'98c0563673b1657ff6d021d1e5f04af06cbf61bb40c63ac613e8bb71b42fb2c0'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='.model-cache/gguf');a=p.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 for name,digest in FILES.items():
  target=out/name
  if not target.exists():
   url=f'https://huggingface.co/datalab-to/surya-ocr-2-gguf/resolve/{REV}/{name}'
   print('Downloading',name,flush=True);urllib.request.urlretrieve(url,target)
  with target.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
  if actual!=digest:raise SystemExit('Model hash mismatch; inspect incomplete download: '+str(target))
  print(name,actual,flush=True)
if __name__=='__main__':main()
