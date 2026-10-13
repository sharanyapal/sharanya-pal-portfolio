import tempfile,unittest
from pathlib import Path
from PIL import Image
from image_forensics import compare,strip_metadata
class Tests(unittest.TestCase):
 def test_same_and_clean(self):
  with tempfile.TemporaryDirectory() as d:
   x,y,z=[str(Path(d)/v) for v in ('a.png','b.png','c.png')]
   im=Image.new('RGB',(40,40),'red');im.save(x);im.save(y)
   self.assertTrue(compare(x,y)['exact_same_sha256'])
   self.assertEqual(compare(x,y)['perceptual_distance'],0)
   strip_metadata(x,z);self.assertTrue(Path(z).exists())
if __name__=='__main__':unittest.main()
