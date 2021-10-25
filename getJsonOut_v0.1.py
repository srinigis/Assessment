# ----------------Draft version----------------------------------------------------------
# getJsonOut.py
#
# Description: This python returns the json string output with csv file as an input
#
# Changes   :   1) Implemented a basic script which converts the csv to json output
#                    2) Based on the pdf, mapping needs to be done [Next set of development]
#              
#
# Author(s):    Srinivasan Ethiraj
#               
# ------------------------------------------------------------------------------------------------------

import csv
import json
 
 
# Function to convert CSV to JSON

def get_json(csvFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvPath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assigning ID column to be the primary key
            key = rows['ID']
            data[key] = rows
        return json.dumps(data, indent=4)   
 

# Csv file path
csvPath = r'F:\sample\Sample Data.csv'

 
# Call the get_json function
print(get_json(csvPath))
