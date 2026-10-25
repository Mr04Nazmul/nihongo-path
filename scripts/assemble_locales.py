import json,pathlib,re
p=pathlib.Path(__file__).resolve().parents[1];cache=json.loads((p/'translation-cache.json').read_text());over={};grammar={};examples={}
for line in (p/'translations/word-overrides.tsv').read_text().splitlines():
 a=line.split('\t')
 if len(a)==3: over[a[0].lower()]=a[1:]
for line in (p/'translations/example-overrides.tsv').read_text().splitlines():
 a=line.split('\t')
 if len(a)==3:examples[a[0]]=a[1:]
for file in (p/'translations').glob('grammar-n*.tsv'):
 for line in file.read_text().splitlines():
  a=line.split('\t')
  if len(a)==3:grammar[a[0].strip()]=a[1:]
terms={
'bn':{'nai':'ない','ta-form':'た-রূপ','te-form':'て-রূপ','Noun':'বিশেষ্য','noun':'বিশেষ্য','Verb':'ক্রিয়া','verb':'ক্রিয়া','Plain form':'সাধারণ রূপ','plain form':'সাধারণ রূপ','dictionary form':'অভিধান রূপ','dict-form':'অভিধান রূপ','dict':'অভিধান রূপ','stem':'মূলাংশ','non-past':'বর্তমান/ভবিষ্যৎ','past':'অতীত','negative':'নঞর্থক','i-adjective':'い-বিশেষণ','na-adjective':'な-বিশেষণ','i-adj':'い-বিশেষণ','na-adj':'な-বিশেষণ','adjective':'বিশেষণ','Number':'সংখ্যা','number':'সংখ্যা','Time period':'সময়কাল','time noun':'সময়বাচক বিশেষ্য','Place':'স্থান','Animate':'মানুষ/প্রাণী','Receiver':'গ্রহীতা','Giver':'দাতা','Object':'কর্ম','Quoted phrase':'উদ্ধৃত বাক্যাংশ','Clause':'উপবাক্য','clause':'উপবাক্য','Phrase':'বাক্যাংশ','root':'মূল','form':'রূপ','or':'অথবা','optional':'ঐচ্ছিক','polite':'ভদ্র','casual':'কথ্য','respectful':'সম্মানসূচক','humble':'বিনয়সূচক','Volitional':'ইচ্ছাসূচক','volitional':'ইচ্ছাসূচক','ます-stem':'ます বাদ দেওয়া মূলাংশ','名詞':'বিশেষ্য'},
'ne':{'nai':'ない','ta-form':'た-रूप','te-form':'て-रूप','Noun':'नाम','noun':'नाम','Verb':'क्रिया','verb':'क्रिया','Plain form':'साधारण रूप','plain form':'साधारण रूप','dictionary form':'शब्दकोश रूप','dict-form':'शब्दकोश रूप','dict':'शब्दकोश रूप','stem':'मूलांश','non-past':'वर्तमान/भविष्य','past':'भूतकाल','negative':'नकारात्मक','i-adjective':'い-विशेषण','na-adjective':'な-विशेषण','i-adj':'い-विशेषण','na-adj':'な-विशेषण','adjective':'विशेषण','Number':'संख्या','number':'संख्या','Time period':'समयावधि','time noun':'समय जनाउने नाम','Place':'स्थान','Animate':'मानिस/जनावर','Receiver':'प्राप्तकर्ता','Giver':'दाता','Object':'कर्म','Quoted phrase':'उद्धृत वाक्यांश','Clause':'उपवाक्य','clause':'उपवाक्य','Phrase':'वाक्यांश','root':'मूल','form':'रूप','or':'वा','optional':'वैकल्पिक','polite':'शिष्ट','casual':'बोलचाल','respectful':'आदरसूचक','humble':'विनम्र','Volitional':'इच्छार्थक','volitional':'इच्छार्थक','ます-stem':'ます हटाइएको मूलांश','名詞':'नाम'}}
def formation(s,lang):
 for k,v in sorted(terms[lang].items(),key=lambda a:-len(a[0])):s=re.sub(r'(?<![A-Za-z])'+re.escape(k)+r'(?![A-Za-z])',lambda m:v,s)
 return s
entry_overrides={}
for line in (p/'translations/entry-overrides.tsv').read_text().splitlines():
 a=line.split('\t')
 if len(a)==3:entry_overrides[a[0]]=a[1:]
report={};missing=[]
for n in [5,4,3,2,1]:
 d=json.loads((p/f'dist/data/n{n}.json').read_text());report['N'+str(n)]={k:len(v) for k,v in d.items()}
 for kind,rows in d.items():
  for e in rows:
   e.setdefault('examples',[])
   e['locales']={}
   for index,lang in enumerate(['bn','ne']):
    def translate(s):
     if s.lower() in over:return over[s.lower()][index]
     v=cache[lang].get(s.strip())
     if not v: missing.append([lang,kind,e['id'],s]);return s
     return v
    if kind=='grammar':
     m=grammar[e['id']][index] if e['id'] in grammar else translate(e['meaning'])
     local={'meaning':m,'formation':formation(e['formation'],lang),'guidance':('এই গঠনটি “'+m+'” বোঝাতে ব্যবহার করুন। নিচের বাক্যে গঠনটি কীভাবে বসেছে দেখুন।' if lang=='bn' else 'यो संरचना “'+m+'” जनाउन प्रयोग हुन्छ। तलका वाक्यमा यसको प्रयोग हेर्नुहोस्।'),'translation_method':'authored-meaning-and-formation' if e['id'] in grammar else 'machine-draft'}
    else:local={'meaning':'; '.join(dict.fromkeys(translate(s) for s in e['meanings'])),'translation_method':'offline-machine-with-curated-core-glosses'}
    if e['id'] in entry_overrides:local.update(meaning=entry_overrides[e['id']][index],translation_method='authored-entry-gloss')
    local['examples']=[examples[x['en']][index] if x['en'] in examples else translate(x['en']) for x in e.get('examples',[])]
    local['example_methods']=['authored' if x['en'] in examples else 'machine-draft' for x in e.get('examples',[])]
    e['locales'][lang]=local
 (p/f'dist/data/n{n}.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
report['totals']={k:sum(x[k] for x in report.values() if isinstance(x,dict) and k in x) for k in ['vocab','grammar','kanji']}
coverage=json.loads((p/'dist/data/coverage.json').read_text());report['added_beyond_primary_source']={k:report['totals'][k]-sum(len(d[k]) for d in coverage['primary_inventory'].values()) for k in ['vocab','grammar','kanji']};report['missing_translation_fields']=len(missing);report['translation_note']='Base grammar glosses authored in Bangla/Nepali; supplementary grammar, vocabulary, kanji glosses and examples include labeled offline SMaLL-100 drafts with curated core overrides. Full native-speaker review is outstanding.'
(p/'dist/data/audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(p/'translation-missing.json').write_text(json.dumps(missing,ensure_ascii=False));print(json.dumps(report,ensure_ascii=False))

(p/'dist/data/index.json').write_text(json.dumps({n:{**report[n],'extra_vocab':sum(e.get('curriculum_status')=='supplementary' for e in json.loads((p/f'dist/data/{n.lower()}.json').read_text())['vocab'])} for n in ['N5','N4','N3','N2','N1']},separators=(',',':')))
