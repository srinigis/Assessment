# ---------------------------------------------------------------------------------------
# Test_getJsonOut.py
#
# Description:Unit Test Script to validate the json outcome of  main script

#               
# --------------------------------------------------------------------------------------

import json
import datetime

import unittest

# import the main script
import getJsonOut
 

# Csv file path
csvPath = r'F:\sample\Sample Data.csv'
logPath = r'F:\sample\RejectedAssets.log'

def validateJson(inpJsonString):
    try:
        json.loads(inpJsonString)
    except ValueError as err:
        return False
    return True

inpJsonString = getJsonOut.get_json(csvPath,logPath)

#validate the json output
actual = validateJson(inpJsonString)
#print (actual)


class TestJsonOutput(unittest.TestCase):
    def test_json(self):
        expected = True
        self.assertEqual(actual,expected) 
 
if __name__ == '__main__':
    unittest.main()
