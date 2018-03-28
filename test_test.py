# test_tests.py

import unittest
try:
    from unittest.mock import patch #python 3.x
except:
    from mock import patch #python 2.7

import test

class TestCleanRun(unittest.TestCase):
    def testRun(self):

        directory = 'csv_files'
        filenames = ['1.csv','2.csv','3.csv']

        #process each file, one at a time
        for filename in filenames:
            p = test.Parser(directory,filename)
            p.pp()
        self.assertEqual(1,1)

class TestExceptions(unittest.TestCase):
    def testDir(self):
        directory = 'csv_files_missing'
        filename = '1.csv'
        self.assertRaises(IOError, test.Parser,directory,filename)

    def testFile(self):
        directory = 'csv_files'
        filename = '4.csv'
        self.assertRaises(IOError, test.Parser,directory,filename)

class TestData(unittest.TestCase):
    @patch('test.Parser.readfile',return_value = {} )
    def testNoData(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        self.assertRaises(KeyError, test.Parser,directory,filename)

    @patch('test.Parser.readfile',return_value = {'mon-fri': 1, 'description':'egDesc'} )
    def testEgRangeStartData(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['mon'])
        expected_mon = "{'day': 'mon', 'description': 'egDesc 1', 'square': 1, 'value': 1 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon-fri': 1, 'description':'egDesc'} )
    def testEgRangeMidData(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['wed'])
        expected_mon = "{'day': 'wed', 'description': 'egDesc 1', 'square': 1, 'value': 1 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon-fri': 1, 'description':'egDesc'} )
    def testEgRangeEndData(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['fri'])
        expected_mon = "{'day': 'fri', 'description': 'egDesc 2', 'double': 2, 'value': 1 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon': 1, 'tue-fri':2, 'description':'egDesc'} )
    def testEgEplicitPre(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['mon'])
        expected_mon = "{'day': 'mon', 'description': 'egDesc 1', 'square': 1, 'value': 1 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon-thu': 1, 'fri':2, 'description':'egDesc'} )
    def testEgExplicitPost(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['fri'])
        expected_mon = "{'day': 'fri', 'description': 'egDesc 4', 'double': 4, 'value': 2 }"
        self.assertEqual(mon,expected_mon)


class TestCalcs(unittest.TestCase):
    @patch('test.Parser.readfile',return_value = {'mon-fri': 5, 'description':'egDesc'} )
    def testSquare(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['mon'])
        expected_mon = "{'day': 'mon', 'description': 'egDesc 25', 'square': 25, 'value': 5 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon-fri': 5, 'description':'egDesc'} )
    def testDouble(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        p = test.Parser(directory,filename)
        mon = str(p.weeks_data['fri'])
        expected_mon = "{'day': 'fri', 'description': 'egDesc 10', 'double': 10, 'value': 5 }"
        self.assertEqual(mon,expected_mon)

    @patch('test.Parser.readfile',return_value = {'mon': 1, 'tue': 1, 'thu': 1, 'description':'egDesc'} )
    def testMissingDays(self,mock_readfile):
        directory = 'csv_files'
        filename = '1.csv'
        self.assertRaises(Exception, test.Parser,directory,filename)


def get_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestCleanRun))
    suite.addTest(loader.loadTestsFromTestCase(TestExceptions))
    suite.addTest(loader.loadTestsFromTestCase(TestData))
    suite.addTest(loader.loadTestsFromTestCase(TestCalcs))
    return suite

if __name__ == '__main__':
    suite = get_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
