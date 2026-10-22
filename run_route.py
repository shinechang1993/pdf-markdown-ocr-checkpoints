"""Run exactly one local conversion; never edit a historical output."""
from pathlib import Path
import argparse, datetime, hashlib, importlib.util, importlib.metadata, json, os, traceback

SOURCE_HASH = 'e6a345602d61f47d81400c4dd23b12d7a20dcbda91e81574ad35c8b8d3f0caa8'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('route',choices=['markitdown','pymupdf-no-ocr','pymupdf-rapidocr','marker'])
    parser.add_argument('--out',required=True)
    parser.add_argument('--llama-server')
    parser.add_argument('--model')
    parser.add_argument('--mmproj')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    source=root/'mixed-text-scan.pdf'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_HASH,'Input specimen changed'
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=False)
    record={'utc_started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'route':args.route,
            'source_sha256':SOURCE_HASH,'sample_created':'2026-10-20','execution_is_new':True}
    try:
        if args.route=='markitdown':
            from markitdown import MarkItDown
            record.update(package_version=importlib.metadata.version('markitdown'),mode='pdf extra, enable_plugins=False, no LLM client')
            text=MarkItDown(enable_plugins=False).convert_local(str(source)).markdown
        elif args.route.startswith('pymupdf-'):
            has_ocr=any(importlib.util.find_spec(name) is not None for name in ['rapidocr','rapidocr_onnxruntime'])
            if args.route=='pymupdf-no-ocr':
                assert not has_ocr,'This is the no-extra-OCR baseline; use a fresh baseline venv'
            else:
                assert has_ocr,'Install requirements-with-ocr.txt for this separate follow-up'
            import pymupdf4llm
            record.update(package_version=importlib.metadata.version('pymupdf4llm'),mode='default to_markdown(path), default OCR enabled; optional engine availability recorded',rapidocr_installed=has_ocr)
            text=pymupdf4llm.to_markdown(str(source))
        else:
            for value in [args.llama_server,args.model,args.mmproj]:
                assert value and Path(value).is_file(),'Marker requires local llama-server, model and mmproj paths'
            cache=Path(os.environ.get('PDF_REPRO_CACHE',str(root/'.model-cache'))).resolve()
            for name,value in {'HF_HOME':str(cache/'huggingface'),'MODEL_CACHE_DIR':str(cache/'datalab'),
                'TORCH_HOME':str(cache/'torch'),'LLAMA_CPP_BINARY':str(Path(args.llama_server).resolve()),
                'LLAMA_CPP_NGL':'0','LLAMA_CPP_EXTRA_ARGS':'--threads 2 --threads-batch 2',
                'SURYA_GGUF_LOCAL_MODEL_PATH':str(Path(args.model).resolve()),
                'SURYA_GGUF_LOCAL_MMPROJ_PATH':str(Path(args.mmproj).resolve()),
                'SURYA_INFERENCE_BACKEND':'llamacpp','SURYA_INFERENCE_PARALLEL':'1',
                'SURYA_INFERENCE_KEEP_ALIVE':'false','OMP_NUM_THREADS':'2'}.items():os.environ[name]=value
            import torch
            torch.set_num_threads(2)
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.output import text_from_rendered
            record.update(package_version=importlib.metadata.version('marker-pdf'),mode='CPU fast; local Surya OCR enabled; use_llm=False; threads2; concurrency1')
            converter=PdfConverter(artifact_dict=create_model_dict(),config={'mode':'fast','use_llm':False})
            rendered=converter(str(source))
            text,_,images=text_from_rendered(rendered)
            record['image_count']=len(images)
            for name,img in images.items():
                target=out/Path(name).name
                img.save(target)
        data=text.encode('utf8');(out/'raw.md').write_bytes(data)
        record.update(converter_returned=True,output_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                      page1_checkpoint='CEDAR BLUE 42' in text,page2_checkpoint='MAPLE GREEN 73' in text)
    except Exception:
        record.update(converter_returned=False,exception=traceback.format_exc())
        traceback.print_exc()
    finally:
        # Persist before upstream atexit cleanup; a returned string is not proof of clean exit.
        (out/'conversion.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    print(json.dumps(record),flush=True)
    return 0 if record['converter_returned'] else 1

if __name__=='__main__':raise SystemExit(main())
