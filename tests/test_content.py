import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ContentChecks(unittest.TestCase):
 def test_curriculum_and_locales(self):
  expected={5:(679,103,84),4:(630,120,169),3:(1671,106,387),2:(1786,148,398)}
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
if __name__=='__main__':unittest.main()
