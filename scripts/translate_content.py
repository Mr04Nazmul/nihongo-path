"""Offline, resumable translation. No lesson text is sent to a translation service."""
import json,pathlib,time,re,os
import ctranslate2,sentencepiece
root=pathlib.Path(__file__).resolve().parents[1];model=pathlib.Path('/workspace/scratch/small100');cachepath=root/'translation-cache.json'
tr=ctranslate2.Translator(str(model),device='cpu',compute_type='int8_float32',intra_threads=6,inter_threads=1)
sp=sentencepiece.SentencePieceProcessor(model_file=str(model/'sentencepiece.bpe.model'))
try:cache=json.loads(cachepath.read_text())
except FileNotFoundError:cache={'bn':{},'ne':{}}
strings=[]
for n in [5,4,3,2]:
 d=json.loads((root/f'dist/data/n{n}.json').read_text())
 for k,rows in d.items():
  for e in rows:
   if k in ['vocab','kanji']:strings.extend(e['meanings'])
   for x in e.get('examples',[]):strings.append(x['en'])
strings=list(dict.fromkeys(x.strip() for x in strings if x.strip()));print('unique strings',len(strings),flush=True)
for lang in ['bn','ne']:
 pending=[s for s in strings if s not in cache[lang]];start=time.time()
 # Short entries first for quickly reusable checkpoints.
 pending.sort(key=len)
 for i in range(0,len(pending),32):
  batch=pending[i:i+32];tokens=[[f'__{lang}__']+sp.encode(s,out_type=str)+['</s>'] for s in batch]
  results=tr.translate_batch(tokens,beam_size=4,max_decoding_length=180,no_repeat_ngram_size=3,max_batch_size=32)
  for s,r in zip(batch,results):cache[lang][s]=sp.decode(r.hypotheses[0]).strip()
  if i%320==0 or i+32>=len(pending):
   tmp=cachepath.with_suffix('.tmp');tmp.write_text(json.dumps(cache,ensure_ascii=False));tmp.replace(cachepath)
   print(lang,min(i+32,len(pending)),'/',len(pending),'seconds',round(time.time()-start),flush=True)
print('DONE',flush=True)
