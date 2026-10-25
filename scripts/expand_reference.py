"""Merge Hanabira grammar and dictionary-validated extended vocabulary.
Usage: python scripts/expand_reference.py HANABIRA_DIR JAPANESE_DATA_DIR
"""
import pathlib,json,re,sys,hashlib,collections,subprocess,shutil
p=pathlib.Path(__file__).resolve().parents[1];h,j=map(pathlib.Path,sys.argv[1:]);out=p/'dist/data'
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,separators=(',',':')))
db={n:read(out/f'{n.lower()}.json') for n in ['N5','N4','N3','N2','N1']}
for d in db.values():d['vocab']=[e for e in d['vocab'] if not e['id'].startswith('ref-')]
def norm(x):return re.sub(r'[^ぁ-ヿ一-龯]','',x).replace('～','').replace('〜','')
def title(x):return re.sub(r'\s*[（(][^()（）]*[A-Za-z][^()（）]*[)）]\s*$', '', x).strip()
gram=[e for d in db.values() for e in d['grammar']];ids={e['id']:e for e in gram};patterns={norm(e['pattern']):e for e in gram if norm(e['pattern'])};report={'grammar':[],'vocabulary':[],'placement_note':'Frequency additions without a source JLPT level appear as supplementary reference vocabulary under N1; this is a UI placement, not a JLPT classification.','sources':{'hanabira':subprocess.check_output(['git','rev-parse','HEAD'],cwd=h,text=True).strip(),'japanese-data':subprocess.check_output(['git','rev-parse','HEAD'],cwd=j,text=True).strip()}}
for n in db:
 for c in read(h/f'grammar_json/grammar_ja_{n}_full_alphabetical_0001.json'):
  pattern=title(c['title']);id='hana-'+hashlib.sha1((n+'|'+c['title']).encode()).hexdigest()[:12];e=ids.get(id) or (patterns.get(norm(pattern)) if norm(pattern) else None);rec={'level':n,'title':c['title']}
  if e:
   if e['id']==id:e['pattern']=pattern
   rec.update(status='covered',id=e['id'],at_level=e['level'])
  else:
   e={'id':id,'level':n,'pattern':pattern,'romaji':'','meaning':c['short_explanation'],'formation':c['formation'],'notes':c['long_explanation'],'examples':[{'ja':x['jp'],'en':x['en'],'romaji':x.get('romaji',''),'source':'hanabira.org'} for x in c['examples'] if x.get('jp') and x.get('en')],'source':'hanabira.org / tristcoil/hanabira.org-japanese-content','source_review_status':'community-reference'}
   db[n]['grammar'].append(e);ids[id]=e;patterns[norm(pattern)]=e;rec.update(status='added',id=id,at_level=n)
  report['grammar'].append(rec)
words=read(j/'data/core/words.json')['words'];lookup=collections.defaultdict(list)
for w in words:
 for form in w['kanji']+w['kana']:lookup[form['text']].append(w)
existing={(str(e.get('jmdict_id')),e['reading']):e for d in db.values() for e in d['vocab']}
# Three independently licensed frequency corpora. Require support in two, and
# a common dictionary spelling. Corpus rank is never represented as a JLPT level.
support=collections.defaultdict(list)
for name in ['frequency-web','frequency-subtitles','frequency-wikipedia']:
 for c in read(j/f'data/enrichment/{name}.json')['entries']:
  if c['rank']<=10000:
   for w in lookup.get(c['text'],[]):
    if any(k['text']==c['reading'] for k in w['kana']):support[(w['id'],c['reading'])].append({'corpus':name,'rank':c['rank'],'form':c['text']})
candidates={key:{'support':list({x['corpus']:x for x in evidence}.values())} for key,evidence in support.items() if len({x['corpus'] for x in evidence})>=2}
# Include lexemes explicitly named in Hanabira's N3 list; verb+noun suru
# variants map to the underlying dictionary word rather than inflating counts.
for f in (h/'sentences_json_japanese').glob('*N3*.json'):
 for c in read(f):
  for form in re.split(r'[/（(）)]',c['key'].strip('_')):
   for w in lookup.get(form,[]):
    kana=next((k for k in w['kana'] if k.get('common')),w['kana'][0]);candidates.setdefault((w['id'],kana['text']),{'support':[]})['hanabira_level']='N3'
byid={w['id']:w for w in words}
for key,info in sorted(candidates.items()):
 w=byid[key[0]];reading=key[1];rec={'jmdict_id':key[0],'reading':reading,**info}
 if key in existing:
  e=existing[key];rec.update(status='covered',id=e['id'],at_level=e['level'],word=e['word'],supplementary=e.get('curriculum_status')=='supplementary');report['vocabulary'].append(rec);continue
 kana=next(k for k in w['kana'] if k['text']==reading)
 if not info.get('hanabira_level') and (not kana.get('common') or len(reading)<2 or any(t in kana.get('tags',[]) for t in ['ok','rk','ik'])):
  rec.update(status='excluded',reason='uncommon, historical or single-kana reading; frequency matches may be ambiguous');report['vocabulary'].append(rec);continue
 writings=[k['text'] for k in w['kanji'] if k.get('common') and ('*' in kana['appliesToKanji'] or k['text'] in kana['appliesToKanji'])]
 if not writings and not kana.get('common'):rec.update(status='excluded',reason='no common dictionary spelling for this reading');report['vocabulary'].append(rec);continue
 word=writings[0] if writings else reading
 senses=[s for s in w['sense'] if not any(t in s.get('misc',[]) for t in ['arch','obs','rare']) and ('*' in s['appliesToKana'] or reading in s['appliesToKana']) and ('*' in s['appliesToKanji'] or word in s['appliesToKanji'] or word==reading)]
 meanings=list(dict.fromkeys(g['text'] for s in senses for g in s['gloss'] if g['lang']=='eng'))
 if not meanings:rec.update(status='excluded',reason='no applicable English sense');report['vocabulary'].append(rec);continue
 level=w.get('jlpt_waller') or info.get('hanabira_level') or 'N1';supplementary=not w.get('jlpt_waller') and not info.get('hanabira_level')
 examples=[{'ja':x['japanese'],'en':x['english'],'source':x.get('source'),'source_sentence_id':x.get('sentence_id')} for s in senses for x in s.get('examples',[]) if x.get('japanese') and x.get('english')]
 e={'id':'ref-'+hashlib.sha1(('|'.join(key)).encode()).hexdigest()[:12],'level':level,'word':word,'reading':reading,'romaji':'','meanings':meanings,'pos':list(dict.fromkeys(x for s in senses for x in s['partOfSpeech'])),'jmdict_id':int(w['id']),'other_forms':[x['text'] for x in w['kanji']+w['kana'] if x['text']!=word],'examples':examples[:2],'source':'jkindrix/japanese-language-data / JMdict; Hanabira N3 index or multi-corpus reference','source_review_status':'dictionary-validated','curriculum_status':'supplementary' if supplementary else 'community-level','level_assignment':'N1 reference placement; JLPT level unclassified' if supplementary else 'community source classification','frequency_support':info['support'],'validation':'common dictionary spelling and reading; applicable modern senses'}
 db[level]['vocab'].append(e);existing[key]=e;rec.update(status='added',id=e['id'],level=level,word=word,supplementary=supplementary);report['vocabulary'].append(rec)
for n,d in db.items():save(out/f'{n.lower()}.json',d)
if (out/'coverage.json').exists():
 coverage=read(out/'coverage.json');coverage['counts']={n:{k:len(d[k]) for k in d} for n,d in db.items()};save(out/'coverage.json',coverage)
report['extension_totals']={'grammar':sum(e['id'].startswith('hana-') for d in db.values() for e in d['grammar']),'vocabulary':sum(e['id'].startswith('ref-') for d in db.values() for e in d['vocab']),'supplementary_vocabulary':sum(e.get('curriculum_status')=='supplementary' for d in db.values() for e in d['vocab'])};report['counts']={n:{k:len(d[k]) for k in d} for n,d in db.items()};report['summary']={k:dict(collections.Counter(e['status'] for e in report[k])) for k in ['grammar','vocabulary']};save(out/'reference-audit.json',report);shutil.copy(h/'LICENSE',out/'HANABIRA-LICENSE');(out/'HANABIRA-ATTRIBUTION.md').write_text('# Hanabira attribution\n\nGrammar content adapted from https://hanabira.org and https://github.com/tristcoil/hanabira.org-japanese-content under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Changes: schema conversion, matching, Bengali/Nepali draft translations. Community source, not certified teaching material. Source revision: '+report['sources']['hanabira']+'\n\nDictionary and corpus sources retain their attribution in SUPPLEMENT-ATTRIBUTION.md. Additional vocabulary supported by at least two of Leeds web, OpenSubtitles/FrequencyWords and KFTT Wikipedia inventories; a corpus rank is not a JLPT classification.\n');print(json.dumps({'counts':report['counts'],'summary':report['summary']},indent=2))
