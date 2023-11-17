"""Tests functions in the utilities module.

"""
import os
import unittest
from thornpy import utilities
from test import *


class Test_Utilities(unittest.TestCase):

    def setUp(self):
        return

    def test_num_to_ith(self):
        ordinals = [utilities.num_to_ith(num) for num in TEST_INTEGERS]
        self.assertEqual(ordinals, TEST_EXPECTED_ORDINALS)
    
    def test_read_data_string_with_headers(self):
        data = utilities.read_data_string(TEST_DATA_STRING)
        self.assertListEqual(data, TEST_EXPECTED_DATA_DICT_WITH_HEADERS)

    def test_read_data_string_without_headers(self):
        data = utilities.read_data_string(TEST_DATA_STRING, has_headerline=False)
        self.assertListEqual(data, TEST_EXPECTED_DATA_DICT_WITHOUT_HEADERS)
    
    def test_convert_path_windows(self):
        """Tests that utilities.convert_path works as expected.

        """
        filepath = 'home/thorn241/test'
        converted_filepath = utilities.convert_path(filepath)
        expected_converted_filepath = os.path.join('home', 'thorn241', 'test')
        self.assertEqual(converted_filepath, expected_converted_filepath)        

    def tearDown(self):
        return
        
class Test_NumToStr_PositiveLargeNumbers(unittest.TestCase):

    NUM = 1e2

    def test_zeros_after_decimal_when_not_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=False)
        self.assertEqual(string, '100.000')
        
    def test_no_zeros_after_decimal_when_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=False)
        self.assertEqual(string, '100')

    def test_zeros_after_decimal_when_not_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=True)
        self.assertEqual(string, '1.000e+02')

        
    def test_no_zeros_after_decimal_when_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=True)
        self.assertEqual(string, '1e+02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e2)
        self.assertEqual(string, '1.000e+02')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e2)
        self.assertEqual(string, '1e+02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e3)
        self.assertEqual(string, '100.000')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e3)
        self.assertEqual(string, '100')

        
class Test_NumToStr_NegativeLargeNumbers(unittest.TestCase):

    NUM = -1e2

    def test_zeros_after_decimal_when_not_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=False)
        self.assertEqual(string, '-100.000')
        
    def test_no_zeros_after_decimal_when_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=False)
        self.assertEqual(string, '-100')

    def test_zeros_after_decimal_when_not_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=True)
        self.assertEqual(string, '-1.000e+02')

        
    def test_no_zeros_after_decimal_when_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=True)
        self.assertEqual(string, '-1e+02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e2)
        self.assertEqual(string, '-1.000e+02')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e2)
        self.assertEqual(string, '-1e+02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e3)
        self.assertEqual(string, '-100.000')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e3)
        self.assertEqual(string, '-100')

        
class Test_NumToStr_PositiveSmallNumbers(unittest.TestCase):

    NUM = 1e-2

    def test_zeros_after_decimal_when_not_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=False)
        self.assertEqual(string, '0.010')
        
    def test_no_zeros_after_decimal_when_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=False)
        self.assertEqual(string, '0.01')

    def test_zeros_after_decimal_when_not_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=True)
        self.assertEqual(string, '1.000e-02')

        
    def test_no_zeros_after_decimal_when_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=True)
        self.assertEqual(string, '1e-02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e-1)
        self.assertEqual(string, '1.000e-02')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e-1)
        self.assertEqual(string, '1e-02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e-3)
        self.assertEqual(string, '0.010')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e-3)
        self.assertEqual(string, '0.01')

        
class Test_NumToStr_NegativeSmallNumbers(unittest.TestCase):

    NUM = -1e-2

    def test_zeros_after_decimal_when_not_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=False)
        self.assertEqual(string, '-0.010')
        
    def test_no_zeros_after_decimal_when_allow_less(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=False)
        self.assertEqual(string, '-0.01')

    def test_zeros_after_decimal_when_not_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=True)
        self.assertEqual(string, '-1.000e-02')

        
    def test_no_zeros_after_decimal_when_allow_less_scientific(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=True)
        self.assertEqual(string, '-1e-02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e-1)
        self.assertEqual(string, '-1.000e-02')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e-1)
        self.assertEqual(string, '-1e-02')

    def test_zeros_after_decimal_when_not_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=False, use_scientific=1e-3)
        self.assertEqual(string, '-0.010')

        
    def test_no_zeros_after_decimal_when_allow_less_with_scientific_threshold_not_exceeded(self):
        string = utilities.num_to_str(self.NUM, 3, allow_less=True, use_scientific=1e-3)
        self.assertEqual(string, '-0.01')
