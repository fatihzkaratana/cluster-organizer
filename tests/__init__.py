# coding: utf-8
"""
The MIT License (MIT)

Copyright (c) 2013 Fatih Karatana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@package 
@date 19/06/14
@author fatih
@version 1.0.0
"""

__author__ = 'fatih'
__date__ = '19/06/14'
__version__ = ''

import unittest
import sys
import os

# Set parent directory to import required files, packages or objects
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '%s' % PARENT_DIR)

# import Statistics class to call its method and test them.
from app import Statistics


class TestStatistics(unittest.TestCase):
    """
    Test statistics app tests
    """
    statistics = Statistics()
    malformed_host_file = PARENT_DIR + "/statistics/tests/data/HostState.txt"
    malformed_instance_file = PARENT_DIR + "/statistics/tests/data/InstanceState.txt"

    def testHostFileFormer(self):
        """
        Check file format is former or malformed
        @return void
        """
        with open(self.statistics.host_file) as file_to_test:
            self.assertTrue(self.statistics.check_file(file_to_test.read()))

    def testInstanceFileFormer(self):
        """
        Check file format is former or malformed
        @return void
        """
        with open(self.statistics.instance_file) as file_to_test:
            self.assertTrue(self.statistics.check_file(file_to_test.read()))

    def testMalformedHostFile(self):
        """
        Check file format is former or malformed
        @return void
        """
        with open(self.malformed_host_file) as file_to_test:
            self.assertFalse(self.statistics.check_file(file_to_test.read()))

    def testMalformedInstanceFile(self):
        """
        Check file format is former or malformed
        @return void
        """
        with open(self.malformed_instance_file) as file_to_test:
            self.assertFalse(self.statistics.check_file(file_to_test.read()))

    def testWriteTarget(self):
        """
        Check if targeted file is written
        @return void
        """
        dummy_content = ["HostClustering: 8, 0.75","DatacentreClustering: 8, 0.36","AvailableHosts: 3,2,5,10,6"]
        self.assertTrue(self.statistics.write_target(dummy_content))


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatistics)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatistics)
    unittest.TextTestRunner(verbosity=2).run(suite)