import unittest
from stream_events import Detector,Event
class TestDetector(unittest.TestCase):
    def ev(self,i,t,o='FAILURE',ip='1.2.3.4',user='alex'):
        return Event(str(i),float(t),user,ip,o)
    def test_threshold_and_lateness(self):
        d=Detector(window_seconds=40,allowed_lateness=10,threshold=4)
        for i,t in enumerate([0,10,8,12,25]): d.ingest(self.ev(i,t))
        assert any(a['type']=='BRUTE_FORCE' for a in d.finish())
    def test_duplicates_and_late(self):
        d=Detector(allowed_lateness=2)
        d.ingest(self.ev(1,100));d.ingest(self.ev(1,100));d.ingest(self.ev(2,50))
        self.assertEqual((d.duplicates,d.late_dropped),(1,1))
    def test_success_after_failure(self):
        d=Detector(threshold=3,allowed_lateness=5)
        for i,o in enumerate(['FAILURE','FAILURE','SUCCESS']): d.ingest(self.ev(i,i,o))
        self.assertTrue(any(a['type']=='SUCCESS_AFTER_FAILURES' for a in d.finish()))
if __name__=='__main__': unittest.main()
