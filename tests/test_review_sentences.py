"""Regression checks for source details previously lost by draft translations."""
import json,pathlib,unittest
class SentenceReview(unittest.TestCase):
 def test_semantic_details(self):
  rows={e['id']:e for e in json.loads((pathlib.Path(__file__).resolve().parents[1]/'dist/data/n5.json').read_text())['vocab']}
  checks=[('d46ae79a26','bn',1,'পনির'),('8bfeb208b4','bn',0,'ছয় পাউন্ড'),('8bfeb208b4','ne',0,'छ पाउन्ड'),('8bfeb208b4','ne',1,'इस्त्री'),('4aab699864','ne',0,'दाइ'),('ac4706068b','ne',1,'सजिलो छैन'),('9f074820b1','bn',1,'এমন নয়'),('277a58c9df','ne',0,'भिज्नबाट जोगिएँ'),('2d55571300','ne',1,'खेल्नु हुँदैन')]
  for eid,lang,i,fragment in checks:
   with self.subTest(id=eid,lang=lang):self.assertIn(fragment,rows[eid]['locales'][lang]['examples'][i])
