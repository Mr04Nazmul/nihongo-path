import pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/'dist'
class Pages(unittest.TestCase):
 def test_every_destination_is_a_real_page_with_shared_app_and_ad_code(self):
  for page in ['index','lessons','n5','n4','n3','n2','review','progress']:
   s=(ROOT/(page+'.html')).read_text()
   for script in ['app.js','ads.js','ads-config.js','speech.js']:self.assertIn('src="'+script+'"',s)
   self.assertIn('ca-pub-3728341118830943',s)
 def test_navigation_is_not_gated_on_an_ad(self):
  s=(ROOT/'app.js').read_text()
  self.assertIn('href="${n.toLowerCase()}.html"',s)
  self.assertIn("/^n([2-5])\\.html$/",s)
  self.assertNotIn('preventDefault()',s)
if __name__=='__main__':unittest.main()
