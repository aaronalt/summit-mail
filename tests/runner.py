from __future__ import absolute_import
import unittest
import tests.test_output as output
import tests.test_creds as creds

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(output))
suite.addTest(loader.loadTestsFromModule(creds))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
print(result)
