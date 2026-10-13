import unittest
from retriever import Retriever
class TestRetrieval(unittest.TestCase):
 def setUp(self):self.r=Retriever({'IAM.md':'Identity access reviews are quarterly. Privileged access needs approval.',
 'helpdesk.txt':'Password reset requires identity verification.'},chunk_words=12,overlap=2)
 def test_evidence(self):
  a=self.r.answer('When are access reviews?')
  self.assertFalse(a['abstained']);self.assertTrue(any(x['source']=='IAM.md' for x in a['citations']))
 def test_no_evidence(self):self.assertTrue(self.r.answer('quantum banana propulsion')['abstained'])
 def test_bad_chunks(self):
  with self.assertRaises(ValueError):Retriever({'a':'hi'},chunk_words=4,overlap=4)
if __name__=='__main__':unittest.main()
