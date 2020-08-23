import unittest

import sys
import os
sys.path.append(os.path.abspath("../src/pyxm"))
from client import PyXMClient
from bd1 import BD1Manipulator

class BD1ManipulatorTest(unittest.TestCase):
    def setUp(self):
        self.client=PyXMClient()
        self.manipulator=BD1Manipulator(self.client,filepath="./test.bd1")
    def tearDown(self):
        self.client.shutdown()

    def test_get_num_blocks(self):
        num_blocks=self.manipulator.get_num_blocks()
        self.assertEqual(98,num_blocks)

if __name__=="__main__":
    unittest.main()
