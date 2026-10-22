"""Verify published historical bytes and inspect new route outputs without rewriting them."""
from pathlib import Path
import argparse,csv,hashlib,json
root=Path(__file__).resolve().parent
expected={
 'mixed-text-scan.pdf':'e6a345602d61f47d81400c4dd23b12d7a20dcbda91e81574ad35c8b8d3f0caa8',
 'historical-markitdown.md':'667e0b45026d56135a86f91e6dd04ad6262481ac2ac7c4f856d40c2bf6ee2960',
 'historical-pymupdf-no-ocr.md':'ba25cb8f9dfa9c5c95321e14e9d229dcbc05b405ae691c42096873d94d3260c9',
 'historical-pymupdf-rapidocr.md':'41337b557a4704b1d17f622c50eae20fe5b926696a27b0a16846e1bf37ebc1eb',
 'historical-marker.md':'9d9a9be5b49d764fe81ee98097b150ca79c7e42065df6cb0561fc9ea9322facb'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--run',action='append',default=[]);a=p.parse_args()
 for name,digest in expected.items():
  actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
  if actual!=digest:raise SystemExit('Historical byte mismatch: '+name)
 print('Historical source and four raw-output SHA256 checks passed')
 for name in a.run:
  path=Path(name);text=(path/'raw.md').read_text(encoding='utf8')
  print(json.dumps({'run':str(path),'page1_checkpoint':'CEDAR BLUE 42' in text,'page2_checkpoint':'MAPLE GREEN 73' in text,'sha256':hashlib.sha256((path/'raw.md').read_bytes()).hexdigest(),'process':json.loads((path/'process.json').read_text())}))
if __name__=='__main__':main()
