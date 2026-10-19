import unittest
from scamshield.engine import analyze_message,analyze_many
class EngineTests(unittest.TestCase):
 def test_upfront_fee_flagged(self):
  r=analyze_message("Guaranteed loan approval! Pay a processing fee now. No documents required."); self.assertEqual(r["label"],"Scam-like"); self.assertGreaterEqual(r["risk_score"],25); self.assertTrue(r["signals"])
 def test_empty_message(self):
  r=analyze_message(""); self.assertEqual(r["label"],"Likely safe"); self.assertEqual(r["risk_score"],0)
 def test_url_detected(self):
  r=analyze_message("Visit https://example.test for information"); self.assertTrue(r["has_url"]); self.assertTrue(any("URL" in s for s in r["signals"]))
 def test_batch_length(self): self.assertEqual(len(analyze_many(["Pay a release fee","Hello"])),2)
if __name__=="__main__": unittest.main()
