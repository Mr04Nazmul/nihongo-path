import pathlib,sys,unittest,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from review_progress import fields,key,valid
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ReviewEvidence(unittest.TestCase):
 def test_current_ledger_and_invalidation(self):
  lookup={key(f):f for f in fields()};records=[json.loads(l) for l in (ROOT/'translations/review-ledger.jsonl').read_text().splitlines()]
  self.assertGreaterEqual(len(records),300)
  # Historical revisions remain in the ledger; report() uses the last record per field.
  latest={key(r):r for r in records}
  for r in records:self.assertIn(key(r),lookup)
  for r in latest.values():self.assertTrue(valid(r,lookup[key(r)]))
  r=next(iter(latest.values()));f=lookup[key(r)];self.assertFalse(valid(r,{**f,'translation':f['translation']+' changed'}));self.assertFalse(valid(r,{**f,'source':{**f['source'],'meaning':'different'}}))
 def test_negation_time_roles_and_idiom(self):
  d=json.loads((ROOT/'dist/data/n5.json').read_text());g={e['id']:e for e in d['grammar']};v={e['word']:e for e in d['vocab'][:100]}
  self.assertIn('খুলছিল না',v['開く']['locales']['bn']['examples'][1]);self.assertIn('खुलेन',v['開く']['locales']['ne']['examples'][1])
  self.assertIn('অনভিজ্ঞ',v['青い']['locales']['bn']['examples'][0]);self.assertIn('अनुभवहीन',v['青い']['locales']['ne']['examples'][0])
  self.assertIn('राति दस',g['ni-destination']['locales']['ne']['examples'][1]);self.assertIn('বড় বোন',g['ni-destination']['locales']['bn']['examples'][2]);self.assertIn('आइतबार',g['ni-time']['locales']['ne']['examples'][1])
  one=next(e for e in d['vocab'] if e['word']=='一日' and e['reading']=='いちにち');self.assertNotIn('first of month',one['meanings'])
if __name__=='__main__':unittest.main()
