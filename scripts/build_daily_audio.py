"""Pre-render the 31 daily-word slots per level; no speech service needed during playback."""
import asyncio,json,pathlib,hashlib,os,time
import edge_tts,edge_tts.communicate
root=pathlib.Path(__file__).resolve().parents[1];out=root/'dist/audio';out.mkdir(exist_ok=True)
if os.environ.get('SSL_CERT_FILE'):edge_tts.communicate._SSL_CTX.load_verify_locations(cafile=os.environ['SSL_CERT_FILE'])
manifest=json.loads((out/'manifest.json').read_text());words={}
for n in [5,4,3,2,1]:
 d=json.loads((root/f'dist/data/n{n}.json').read_text())
 for e in d['vocab'][:32]:words[e['word']]=e['reading']
words['あんな']='あんな'
sem=asyncio.Semaphore(4);completed=0;failures=[];start=time.time()
async def save(word,reading):
 global completed
 async with sem:
  name=hashlib.sha256(word.encode()).hexdigest()[:20]+'.mp3';p=out/name
  try:
   if not p.exists():await asyncio.wait_for(edge_tts.Communicate(reading,'ja-JP-NanamiNeural',rate='-10%').save(str(p)),timeout=35)
   if p.stat().st_size<500:raise ValueError('empty clip')
   manifest[word]=name;completed+=1
   if completed%16==0:print('clips',completed,'/',len(words),'seconds',round(time.time()-start),flush=True)
  except Exception as e:
   failures.append([word,type(e).__name__]);p.unlink(missing_ok=True)
async def main():
 await asyncio.gather(*(save(w,r) for w,r in words.items()));(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False));print('DONE',completed,'failures',failures,flush=True)
asyncio.run(main())
