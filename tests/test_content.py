import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ContentChecks(unittest.TestCase):
 def test_curriculum_and_locales(self):
  expected={int(n[1]):tuple(d[k] for k in ['vocab','grammar','kanji']) for n,d in json.loads((ROOT/'dist/data/coverage.json').read_text())['counts'].items()}
  for n,counts in expected.items():
   d=json.loads((ROOT/f'dist/data/n{n}.json').read_text())
   self.assertEqual(tuple(len(d[k]) for k in ['vocab','grammar','kanji']),counts)
   for kind,rows in d.items():
    self.assertEqual(len({e['id'] for e in rows}),len(rows))
    for e in rows:
     self.assertTrue(e.get('word') or e.get('pattern'))
     for lang in ['bn','ne']:
      self.assertTrue(e['locales'][lang]['meaning'].strip())
      self.assertEqual(len(e['locales'][lang]['examples']),len(e['examples']))
      self.assertTrue(all(x.strip() for x in e['locales'][lang]['examples']))
 def test_negation_and_japanese_formation(self):
  d=json.loads((ROOT/'dist/data/n2.json').read_text());e=next(x for x in d['grammar'] if x['id']=='zaru-o-enai')
  self.assertEqual(e['locales']['bn']['meaning'],'করা ছাড়া কোনো উপায় নেই')
  self.assertEqual(e['locales']['ne']['meaning'],'गर्नुबाहेक अरू उपाय छैन')
  for lang in ['bn','ne']:self.assertIn('ざるを得ない',e['locales'][lang]['formation'])
 def test_no_missing_cache_fields(self):
  self.assertEqual(json.loads((ROOT/'dist/data/audit.json').read_text())['missing_translation_fields'],0)
 def test_ads_identifiers(self):
  s=(ROOT/'dist/ads-config.js').read_text();self.assertIn('ca-pub-3728341118830943',s);self.assertIn("slot:'2007625275'",s)
 def test_source_inventory_and_second_source_resolutions(self):
  audit=json.loads((ROOT/'dist/data/coverage.json').read_text())
  db={n:json.loads((ROOT/('dist/data/'+n.lower()+'.json')).read_text()) for n in audit['counts']}
  for n,inventory in audit['primary_inventory'].items():
   for kind,ids in inventory.items():self.assertTrue(set(ids).issubset({e['id'] for e in db[n][kind]}))
  self.assertEqual(len(audit['grammar']),595)
  self.assertEqual(len(audit['kanji']),2211)
  self.assertEqual(len(audit['vocabulary']),8293)
  for kind,name in [('grammar','grammar'),('vocabulary','vocab')]:
   for entry in audit[kind]:
    if entry['status']=='excluded':self.assertTrue(entry.get('reason'));continue
    self.assertIn(entry['id'],{e['id'] for e in db[entry.get('at_level',entry['level'])][name]})
  for e in audit['kanji']:self.assertIn(e['character'],{x['character'] for d in db.values() for x in d['kanji']})
 def test_n1_authored_grammar_and_draft_labels(self):
  d=json.loads((ROOT/'dist/data/n1.json').read_text())
  authored=[e for e in d['grammar'] if e['locales']['bn']['translation_method']=='authored-meaning-and-formation']
  self.assertGreaterEqual(len(authored),123)
  for n in range(1,6):
   for rows in json.loads((ROOT/f'dist/data/n{n}.json').read_text()).values():
    for e in rows:
     for lang in ['bn','ne']:self.assertEqual(len(e['examples']),len(e['locales'][lang]['example_methods']))
 def test_extended_grammar_and_dictionary_reference_audit(self):
  audit=json.loads((ROOT/'dist/data/reference-audit.json').read_text())
  db={n:json.loads((ROOT/('dist/data/'+n.lower()+'.json')).read_text()) for n in audit['counts']}
  self.assertEqual(len(audit['grammar']),828)
  for entry in audit['grammar']:
   self.assertIn(entry['id'],{e['id'] for e in db[entry['at_level']]['grammar']})
  extra=[e for d in db.values() for e in d['vocab'] if e.get('curriculum_status')=='supplementary']
  self.assertGreaterEqual(len(extra),4000)
  for e in extra:
   self.assertIn('unclassified',e['level_assignment'])
   self.assertGreaterEqual(len({x['corpus'] for x in e['frequency_support']}),2)
  for d in db.values():
   for e in d['grammar']:
    self.assertTrue(e['pattern'].strip('~〜～ '))
    if e['id'].startswith('hana-'):self.assertRegex(e['pattern'],r'[ぁ-ヿ一-龯]')
 def test_ambiguous_cast_gloss_is_corrected_by_entry(self):
  rows=[e for n in range(1,6) for e in json.loads((ROOT/f'dist/data/n{n}.json').read_text())['vocab']]
  e=next(e for e in rows if e['word']=='鋳る' and e['reading']=='いる')
  self.assertIn('ঢালাই',e['locales']['bn']['meaning'])
  self.assertIn('ढाल्नु',e['locales']['ne']['meaning'])
if __name__=='__main__':unittest.main()
