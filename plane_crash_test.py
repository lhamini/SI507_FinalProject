import unittest
import plane_crash as pci

# SI 507 Winter 2020
# Final Project

class Test_Part1(unittest.TestCase):
    def setUp(self):
        self.year_url = pci.build_crash_year_url_dict()

    def test_1_1_return_type(self):
        self.assertEqual(type(self.year_url), dict)

    def test_1_2_return_length(self):
        self.assertEqual(len(self.year_url), 101)

    def test_1_3_contents(self):
        self.assertEqual(self.year_url['1936'], 'http://www.planecrashinfo.com/1936/1936.htm')
        self.assertEqual(self.year_url['2017'], 'http://www.planecrashinfo.com/2017/2017.htm')



























if __name__ == '__main__':
    unittest.main()
