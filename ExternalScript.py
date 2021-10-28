# ------------------------------------------------------------------------------------------------------
# ExternalScript.py
#
# Description: Test Script to call the main script to return json output

#               
# ------------------------------------------------------------------------------------------------------

import json
import datetime

# import the main script
import getJsonOut
 

# Csv file path
csvPath = r'F:\sample\Sample Data.csv'
logPath = r'F:\sample\RejectedAssets.log'
 
# Call the get_json function
print(getJsonOut.get_json(csvPath,logPath))
