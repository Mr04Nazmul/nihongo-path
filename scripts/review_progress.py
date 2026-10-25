"""Count hash-bound semantic-review evidence, never equating authorship with review.
The ledger is populated only after a semantic pass; this script does not review text.
"""
import hashlib,json,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fields(root=ROOT):
 for n in [5,4,3,2,1]:
  for kind,rows in json.loads((root/f'dist/data/n{n}.json').read_text()).items():
   for e in rows:
    for lang in ['bn','ne']:
     l=e['locales'][lang]
     for field in ['meaning','formation','guidance']:
      if field not in l:continue
      source={'word':e.get('word',e.get('pattern')),'reading':e.get('reading'),'meaning':e.get('meaning',e.get('meanings'))}
      if field!='meaning':source.update(formation=e.get('formation'),notes=e.get('notes'))
      yield {'level':e['level'],'kind':kind,'id':e['id'],'language':lang,'field':field,'source':source,'translation':l[field]}
     for i,x in enumerate(e.get('examples',[])):
      yield {'level':e['level'],'kind':kind,'id':e['id'],'language':lang,'field':f'examples.{i}','source':{'ja':x['ja'],'en':x['en']},'translation':l['examples'][i]}
def key(f):return ':'.join(f[x] for x in ['level','kind','id','language','field'])
def valid(record,field):return record.get('status')=='ai-semantic-checked' and record.get('source_sha256')==digest(field['source']) and record.get('translation_sha256')==digest(field['translation'])
def report(root=ROOT):
 ledger=root/'translations/review-ledger.jsonl';records={key(r):r for line in ledger.read_text().splitlines() if (r:=json.loads(line))} if ledger.exists() else {}
 all_fields=list(fields(root));checked=[f for f in all_fields if key(f) in records and valid(records[key(f)],f)];by_level=collections.Counter(f['level'] for f in checked)
 pending=[{k:f[k] for k in ['level','kind','id','language','field']} for f in all_fields if key(f) not in records or not valid(records[key(f)],f)]
 result={'status':'in-progress' if pending else 'ai-semantic-pass-complete','reviewed_on':'2026-10-26','total_scoped_fields':len(all_fields),'ai_semantic_checked_fields':len(checked),'pending_fields':len(pending),'checked_by_level':dict(by_level),'authored_entry_glosses':len((root/'translations/entry-overrides.tsv').read_text().splitlines()),'native_speaker_review':'not performed','next_unreviewed_fields':pending[:20],'counting_note':'Strict source-and-translation-hash ledger; historical authored or machine labels do not by themselves prove semantic review. Counts are not directly comparable to the older machine-draft-only pending count.','latest_pass':'N5 vocabulary meanings 0–99; all examples of vocabulary 0–9; first five N5 grammar meanings, formation, guidance and examples. Idiomatic green, subject focus, Sunday, night-time, sister and negation checked.'}
 (root/'translations/review-progress.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');return result
if __name__=='__main__':print(json.dumps(report(),ensure_ascii=False))
