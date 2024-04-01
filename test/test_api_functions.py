import unittest
from utils.tools import *

CSV_FILE_WITH_ADDRESS = "results_address.csv"


class TestApiFunctions(unittest.TestCase):

    def test_find_adress_in_dataframe(self):
        df = read_csv(CSV_FILE_WITH_ADDRESS)
        results = find_address(df, "address", "Ouessant", "29242")
        self.assertTrue(len(results.index) > 0 )
        
if __name__ == '__main__':
    unittest.main()