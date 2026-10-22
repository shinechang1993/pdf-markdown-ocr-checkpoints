from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium
import json, hashlib

root=Path(__file__).resolve().parent
out=root/'regenerated'
out.mkdir(exist_ok=False)
def draw(c, page):
    c.setFont('Helvetica-Bold',24)
    c.drawString(54,720,'Cedar Lab Handover')
    c.setFont('Helvetica',12)
    lines = ([
      'Page 1 - selectable text',
      'Digital checkpoint: CEDAR BLUE 42',
      'The morning team checked the archive shelf.',
      'Three blue folders are ready for review.',
      'This page contains selectable PDF text.',
    ] if page==1 else [
      'Page 2 - raster-only handover note',
      'Scanned checkpoint: MAPLE GREEN 73',
      'The evening team moved the reference box.',
      'Seven green folders remain on shelf B.',
      'This page is an image without a text layer.',
    ])
    for i,line in enumerate(lines): c.drawString(54,665-i*40,line)
    c.setFont('Helvetica',10)
    c.drawString(54,90,'Original synthetic English specimen - PDF Markdown Kit - 20 October 2026')
    c.drawString(54,72,f'Page {page} of 2')
memory=BytesIO()
temp=canvas.Canvas(memory,pagesize=(612,792)); draw(temp,2);temp.save()
image=pdfium.PdfDocument(memory.getvalue())[0].render(scale=2).to_pil()
image.save(out/'raster-page-source.png')
c=canvas.Canvas(str(out/'mixed-text-scan.pdf'),pagesize=(612,792),invariant=1)
c.setTitle('Cedar Lab Handover - mixed text and raster PDF')
c.setAuthor('PDF Markdown Kit')
draw(c,1);c.showPage()
c.drawImage(ImageReader(image),0,0,width=612,height=792);c.showPage();c.save()
doc=pdfium.PdfDocument(out/'mixed-text-scan.pdf')
checks=[]
for i,page in enumerate(doc):
    page.render(scale=1).to_pil().save(out/f'page-{i+1}.png')
    checks.append({'page':i+1,'extracted_text':page.get_textpage().get_text_range()})
meta={'sample':'mixed-text-scan.pdf','created_date':'2026-10-20','language':'English',
      'sha256':hashlib.sha256((out/'mixed-text-scan.pdf').read_bytes()).hexdigest(),
      'page_text_layer_checks':checks}
(out/'sample-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta,indent=2))
