"""Merge two licensed community inventories, preserving existing entry IDs and translations.
Usage: python scripts/expand_n1.py OPENJLPT_DIR JAPANESE_DATA_DIR
Level conflicts retain the existing teaching level; variants remain searchable.
"""
import json,pathlib,re,sys,hashlib,subprocess,collections
root=pathlib.Path(__file__).resolve().parents[1];a,b=map(pathlib.Path,sys.argv[1:3]);out=root/'dist/data'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
levels=['N5','N4','N3','N2','N1'];db={n:read(out/(n.lower()+'.json')) if (out/(n.lower()+'.json')).exists() else {} for n in levels}
report={'sources':{},'vocabulary':[],'grammar':[],'kanji':[],'scope':'Two community inventories, not an official exhaustive JLPT syllabus. Existing level assignments retained on conflicts.'}
for name,path in [('OpenJLPT',a),('Japanese Language Data',b)]:report['sources'][name]=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip()
# Exact source IDs ensure every OpenJLPT entry is represented.
for n,d in db.items():
 for kind in ['vocab','grammar','kanji']:
  rows=d.setdefault(kind,[]);ids={e.get('id',e.get('character')) for e in rows}
  for e in read(a/f'data/json/{kind}/{n.lower()}.json'):
   if kind=='kanji':e.update(id=e['character'],word=e['character'],reading=' / '.join(e['onyomi']+e['kunyomi']),examples=[])
   if e['id'] not in ids:rows.append(e);ids.add(e['id'])
words={str(e['id']):e for e in read(b/'data/core/words.json')['words']}
dictionary_pairs={}
for w in words.values():
 for spelling in w['kanji']+w['kana']:
  for kana in w['kana']:
   if spelling['text'] in [x['text'] for x in w['kana']] or '*' in kana['appliesToKanji'] or spelling['text'] in kana['appliesToKanji']:dictionary_pairs.setdefault((spelling['text'],kana['text']),[]).append(w)
classes=read(b/'data/enrichment/jlpt-classifications.json')['classifications']
vocab=[e for d in db.values() for e in d['vocab']]
# Compare dictionary identity AND reading. Never collapse unrelated homophones.
pairs={(str(e.get('jmdict_id')),e['reading']):e for e in vocab}
for c in classes:
 if c['kind']!='vocab':continue
 key=(str(c.get('jmdict_seq')),c['reading']);rec={'text':c['text'],'reading':c['reading'],'level':c['level']}
 if key in pairs:
  e=pairs[key];forms=e.setdefault('other_forms',[])
  if c['text']!=e['word'] and c['text'] not in forms:forms.append(c['text'])
  rec.update(status='covered',id=e['id'],at_level=e['level']);report['vocabulary'].append(rec);continue
 w=words.get(key[0]);reason=None
 candidates=dictionary_pairs.get((c['text'],c['reading']),[])
 if (not w or not any(x['text']==c['reading'] for x in w['kana'])) and len(candidates)==1:
  w=candidates[0];key=(str(w['id']),c['reading']);rec['dictionary_id_repaired']=w['id']
  if key in pairs:
   e=pairs[key];rec.update(status='covered',id=e['id'],at_level=e['level']);report['vocabulary'].append(rec);continue
 if not w:reason='JMdict identity absent'
 elif c['text'] not in [x['text'] for x in w['kanji']+w['kana']]:reason='spelling not validated by JMdict'
 elif c['reading'] not in [x['text'] for x in w['kana']]:reason='reading not validated by JMdict'
 else:
  kana=next(x for x in w['kana'] if x['text']==c['reading'])
  if w['kanji'] and c['text'] not in [x['text'] for x in w['kana']] and '*' not in kana['appliesToKanji'] and c['text'] not in kana['appliesToKanji']:reason='reading restricted to a different spelling'
 if reason:rec.update(status='excluded',reason=reason);report['vocabulary'].append(rec);continue
 senses=[s for s in w['sense'] if ('*' in s['appliesToKana'] or c['reading'] in s['appliesToKana']) and ('*' in s['appliesToKanji'] or c['text'] in s['appliesToKanji'] or c['text'] in [x['text'] for x in w['kana']])]
 glosses=list(dict.fromkeys(g['text'] for s in senses for g in s['gloss'] if g['lang']=='eng'))
 if not glosses:rec.update(status='excluded',reason='no applicable English dictionary sense');report['vocabulary'].append(rec);continue
 examples=[{'ja':x['japanese'],'en':x['english'],'source':x.get('source','JMdict example'),'source_sentence_id':x.get('sentence_id')} for s in senses for x in s.get('examples',[]) if x.get('japanese') and x.get('english')]
 e={'id':'dict-'+hashlib.sha1(('|'.join(key)).encode()).hexdigest()[:12],'word':c['text'],'reading':c['reading'],'romaji':'','meanings':glosses,'level':c['level'],'jmdict_id':int(w['id']),'pos':list(dict.fromkeys(p for s in senses for p in s['partOfSpeech'])),'other_forms':[x['text'] for x in w['kanji']+w['kana'] if x['text']!=c['text']],'examples':examples[:2],'source':'jkindrix/japanese-language-data / JMdict','source_review_status':'dictionary-validated'}
 db[c['level']]['vocab'].append(e);pairs[key]=e;rec.update(status='added',id=e['id']);report['vocabulary'].append(rec)
# Restore source sentence identifiers on previously imported supplemental entries.
for d in db.values():
 for e in d['vocab']:
  if 'jkindrix' not in e.get('source',''):continue
  w=words.get(str(e.get('jmdict_id')))
  if not w:continue
  lookup={(x.get('japanese'),x.get('english')):x for sense in w['sense'] for x in sense.get('examples',[])}
  for example in e.get('examples',[]):
   x=lookup.get((example['ja'],example['en']))
   if x:example.update(source=x.get('source','JMdict example'),source_sentence_id=x.get('sentence_id'))
def norm(s):return re.sub(r'[^ぁ-ヿ一-龯]','',s).replace('〜','')
gram=[e for d in db.values() for e in d['grammar']];byid={e['id'].removeprefix('supp-'):e for e in gram};bynorm={norm(e['pattern']):e for e in gram if norm(e['pattern'])}
for c in read(b/'data/grammar/grammar.json')['grammar_points']:
 rec={'source_id':c['id'],'pattern':c['pattern'],'level':c['level']};e=byid.get(c['id']) or (bynorm.get(norm(c['pattern'])) if norm(c['pattern']) else None)
 if e:rec.update(status='covered',id=e['id'],at_level=e['level'])
 else:
  e={'id':'supp-'+c['id'],'pattern':c['pattern'],'romaji':'','level':c['level'],'meaning':c['meaning_en'],'formation':c['formation'],'notes':c['meaning_detailed'],'examples':[{'ja':x['japanese'],'en':x['english']} for x in c['examples']],'source':'jkindrix/japanese-language-data','source_review_status':c['review_status']}
  db[c['level']]['grammar'].append(e);byid[c['id']]=e;bynorm[norm(c['pattern'])]=e;rec.update(status='added',id=e['id'])
 report['grammar'].append(rec)
# All OpenJLPT kanji imported above; audit the second source by character.
chars={e['character']:e for d in db.values() for e in d['kanji']}
kdata=read(b/'data/core/kanji.json');krows=kdata['kanji'];kmap={e['character']:e for e in krows}
for c in classes:
 if c['kind']!='kanji':continue
 rec={'character':c['text'],'level':c['level']}
 if c['text'] in chars:rec.update(status='covered',at_level=chars[c['text']]['level'])
 else:
  k=kmap.get(c['text'])
  if not k or not k['meanings'].get('en'):rec.update(status='excluded',reason='no validated KANJIDIC entry')
  else:
   e={'id':k['character'],'character':k['character'],'word':k['character'],'reading':' / '.join(k['readings']['on']+k['readings']['kun']),'level':c['level'],'strokes':k['stroke_count'],'grade':k['grade'],'freq':k['frequency'],'radical':'','radical_number':k['radical']['classical'],'onyomi':k['readings']['on'],'kunyomi':k['readings']['kun'],'meanings':k['meanings']['en'],'words':[],'examples':[],'source':'jkindrix/japanese-language-data / KANJIDIC2'}
   db[c['level']]['kanji'].append(e);chars[c['text']]=e;rec.update(status='added')
 report['kanji'].append(rec)
for n,d in db.items():save(out/(n.lower()+'.json'),d)
report['primary_inventory']={n:{k:[e.get('id',e.get('character')) for e in read(a/f'data/json/{k}/{n.lower()}.json')] for k in ['vocab','grammar','kanji']} for n in levels}
report['counts']={n:{k:len(d[k]) for k in d} for n,d in db.items()};report['summary']={k:dict(collections.Counter(e['status'] for e in report[k])) for k in ['vocabulary','grammar','kanji']}
save(out/'coverage.json',report);print(json.dumps({'counts':report['counts'],'summary':report['summary']},indent=2))
