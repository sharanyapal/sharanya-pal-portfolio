import unittest
from quant_risk import ema,strategy,bootstrap_var,drawdown
class Tests(unittest.TestCase):
 def test_ema_constant(self):self.assertEqual(ema([10]*30,8),[10]*30)
 def test_strategy_identity(self):
  prices=[100+i*.5 for i in range(55)];r=strategy(prices)
  self.assertAlmostEqual(r['equity'][0],10000);self.assertTrue(r['max_drawdown']>=0)
 def test_dd(self):self.assertAlmostEqual(drawdown([100,120,90]),.25)
 def test_seeded_var(self):self.assertEqual(bootstrap_var([-.02,.01,.03,-.04]),bootstrap_var([-.02,.01,.03,-.04]))
if __name__=='__main__':unittest.main()
