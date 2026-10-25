import json,pathlib,shutil,hashlib
p=pathlib.Path('dist/data');q=pathlib.Path('/workspace/scratch/japanese-data/data');o=pathlib.Path('/workspace/scratch/openjlpt/data/json')
selection={
'N5': 'i-adjective-nonpast i-adjective-past na-adjective-attributive counter-tsu counter-people-nin question-words-basic issho-ni-together i-adj-adverbial-ku mo-mo-both location-nouns-ue-shita ikutsu-how-many ikura-how-much nanji-what-time nanyoubi-day-of-week counter-ji-oclock counter-fun-minute counter-sai-age counter-en-money counter-hon-long counter-mai-flat mai-every-prefix jikan-time-duration',
'N4': 'noun-modifying-clause jidoushi-tadoushi kata-way-of-doing o-v-kudasai-polite-honor sonkeigo-reru-rareru humble-o-suru sou-iu-kou-iu yaru-casual-giving irassharu-honorific ossharu-honorific goran-ni-naru-honorific nasaru-honorific mairu-humble mousu-humble itadaku-humble-verb kudasaru-honorific-verb ga-wakaru ga-dekiru ga-kikoeru-mieru dakara-so sorede-and-then sorekara-after shikashi-but soredemo-even-so',
'N3': 'no-nominalizer ni-yotte nakucha-nakya ni-kawatte-instead muke-targeted-for muki-suitable-for to-itta-such-as chuu-during au-together komi-into igai-other-than n-da-kara-emphatic zuni-sumu ni-ataru-correspond',
'N2': 'yue-ni-because ba-koso-precisely-because you-to-mai-to made-mo-nai no-minarazu to-wa-ie ni-shite-mireba dake-mashi-da nai-made-mo zu-jimai nani-shiro nani-se kekka-result wo-hete wo-fumaete to-mieru tatte-even-casual atte-no-thanks-to datte-casual-because you-nara-if-looks naku-mo-nai sobireru-miss-chance ato-wa-rest dake-nara tsutsu-while ni-shitagatte shikamo-moreover hodo-dewa-nai'
}
gram={e['id']:e for e in json.loads((q/'grammar/grammar.json').read_text())['grammar_points']}
classifications=json.loads((q/'enrichment/jlpt-classifications.json').read_text())['classifications'];words={e['id']:e for e in json.loads((q/'core/words.json').read_text())['words']}
all_vocab=[e for n in range(2,6) for e in json.loads((p/f'n{n}.json').read_text())['vocab']];seq={str(e.get('jmdict_id')) for e in all_vocab};reading={e['reading'] for e in all_vocab}
report={}
for n,ids in selection.items():
 d=json.loads((p/(n.lower()+'.json')).read_text()); existing={e['id'] for e in d['grammar']};added=[]
 for id in ids.split():
  if 'supp-'+id in existing: continue
  if id not in gram: print('MISSING',id);continue
  e=gram[id]; d['grammar'].append({'id':'supp-'+id,'level':n,'pattern':e['pattern'],'romaji':'','meaning':e['meaning_en'],'formation':e['formation'],'notes':e['meaning_detailed'],'examples':[{'ja':x['japanese'],'en':x['english']} for x in e['examples']],'source':'jkindrix/japanese-language-data','source_review_status':e['review_status']});added.append(id)
 vc=[]
 for e in classifications:
  if e['kind']!='vocab' or e['level']!=n or e.get('jmdict_seq') in seq or e.get('reading') in reading:continue
  w=words.get(e.get('jmdict_seq'))
  if not w or e['reading'] not in [x['text'] for x in w['kana']]:continue
  validkanji=[x['text'] for x in w['kanji']];validkana=[x['text'] for x in w['kana']]
  if e['text'] not in validkanji+validkana: continue
  senses=[s for s in w['sense'] if '*' in s['appliesToKana'] or e['reading'] in s['appliesToKana']]
  meanings=list(dict.fromkeys(g['text'] for s in senses for g in s['gloss'] if g['lang']=='eng'))
  if not meanings:continue
  ex=[]
  for s in senses:
   for x in s.get('examples',[]):
    if x.get('english') and x.get('japanese'):ex.append({'ja':x['japanese'],'en':x['english']})
  v={'id':'extra-'+hashlib.sha1((e['text']+e['reading']).encode()).hexdigest()[:10],'word':e['text'],'reading':e['reading'],'romaji':'','meanings':meanings[:8],'level':n,'pos':list(dict.fromkeys(x for s in senses for x in s['partOfSpeech'])),'jmdict_id':int(w['id']),'examples':ex[:2],'source':'jkindrix/japanese-language-data'}
  d['vocab'].append(v);seq.add(w['id']);reading.add(e['reading']);vc.append([e['text'],e['reading']])
 d['kanji']=json.loads((o/f'kanji/{n.lower()}.json').read_text())
 for e in d['kanji']:e['id']=e['character'];e['word']=e['character'];e['reading']=' / '.join(e['onyomi']+e['kunyomi']);e['examples']=[]
 (p/(n.lower()+'.json')).write_text(json.dumps(d,ensure_ascii=False))
 report[n]={'grammar_added':added,'vocab_added':vc,'counts':{k:len(d[k]) for k in ['vocab','grammar','kanji']}}
pathlib.Path('data-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));shutil.copy('/workspace/scratch/japanese-data/LICENSE',p/'SUPPLEMENT-LICENSE');shutil.copy('/workspace/scratch/japanese-data/NOTICE.md',p/'SUPPLEMENT-NOTICE.md') if pathlib.Path('/workspace/scratch/japanese-data/NOTICE.md').exists() else None
print(json.dumps(report,ensure_ascii=False))
