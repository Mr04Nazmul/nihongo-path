import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class AudioAssets(unittest.TestCase):
 def test_every_calendar_day_has_a_clip_in_each_level(self):
  manifest=json.loads((ROOT/'dist/audio/manifest.json').read_text())
  for n in [5,4,3,2]:
   words=json.loads((ROOT/f'dist/data/n{n}.json').read_text())['vocab']
   for day in range(1,32):self.assertIn(words[day%len(words)]['word'],manifest)
  self.assertIn('あんな',manifest)
  for name in manifest.values():
   p=ROOT/'dist/audio'/name
   self.assertTrue(p.is_file());self.assertGreater(p.stat().st_size,500)
   data=p.read_bytes()[:3];self.assertTrue(data==b'ID3' or data[0]==255)
if __name__=='__main__':unittest.main()
