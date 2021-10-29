# ----------------------------------------------------------------------------------------------------------------------------
# getJsonOut.py
#
# Description: This python returns the json  output with csv file as an input with field mapping and data validations in place.
#
# Changes   :   1) Implemented the csv2json functionality as per TFL requirement
#               2) Implemented data validations and field mappings for json output
#               3) Implemented Error Handling & Logging 
#               4) ** Documentation needs to be created     [inProgress]     
#
# Author(s):    Srinivasan Ethiraj
#               
# ------------------------------------------------------------------------------------------------------------------------------

import csv
import json
import datetime
import os

# Csv file path
csvPath = r'F:\sample\Sample Data.csv'
logPath = r'F:\sample\RejectedAssets.log'

##########################################
# Error Logging                          #
##########################################

def generateErrorLog(logPath,errorDetails):
# Create a log file to write the logs
      if os.path.exists(logPath):
          append_write = 'a' # append if already exists
      else:
          append_write = 'w' # make a new file if not
      writeLog = open(logPath,append_write)
      writeLog.write(errorDetails + '\n')

##########################################
# Main Function to convert CSV to JSON   #
##########################################
def get_json(csvFilePath,logPath):
      
  try:   
     
    # create a dictionary , list
      dataList = []

       
    # Open a csv reader called DictReader
      with open(csvPath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        generateErrorLog(logPath, str(datetime.datetime.now()) + " - Start of Log" + '\n')
        # Convert each row into a dictionary and store it inside a new dictionary 'dataDict'
        for rows in csvReader:
            dataDict = {}
            # Create new column names with key and store the values in it
            strAssetId = rows['ID']
            dataDict['id'] = strAssetId
            dataDict['type'] = rows['TYPE']
            dataDict['typeDescription'] = rows['TYPE_DESC']            
            dataDict['easting'] = rows['EASTING']
            dataDict['northing'] = rows['NORTHING']

            # Infill null values with empty string for required fields
            dataDict['installationDate'] = rows['INSTALL_DATE']
            if rows['INSTALL_DATE'] is None:
                dataDict['installationDate'] = ""
            
            dataDict['location'] = rows['LOCATION']
            if rows['LOCATION'] is None:
                dataDict['location'] = ""
                
            dataDict['controlServer'] = rows['CELL']
            if rows['CELL'] is None:
                dataDict['controlServer'] = ""
                
            dataDict['signalGroup'] = rows['SIGNAL_GROUP']
            if rows['SIGNAL_GROUP'] is None:
                dataDict['signalGroup'] = ""

            dataDict['installedBy'] = rows['INSTALL_ENGINEER']
            if rows['INSTALL_ENGINEER'] is None:
                dataDict['installedBy'] = ""
                
            dataDict['status'] = rows['STATUS']
            
                        
            # validate and accept only valid records
            if (validateAssetId(rows['ID']) and validateAssetTypeCode(strAssetId,rows['TYPE']) and validateAssetTypeDesc(strAssetId,rows['TYPE_DESC']) and
                validateAssetInstDate(strAssetId,rows['INSTALL_DATE']) and
                validateEasting(strAssetId,rows['EASTING']) and validateNorthing(strAssetId,rows['NORTHING']) and
                validateAssetRoadAddress(strAssetId,rows['LOCATION']) and validateCell(strAssetId,rows['CELL']) and validateSignalGrpId(strAssetId,rows['SIGNAL_GROUP']) and
                validateAssetStatus(strAssetId,rows['STATUS']) and validateEngineerName(strAssetId,rows['INSTALL_ENGINEER'])):

                if rows['INSTALL_DATE'] != "":
                    # convert the instal date to  yyyy-mm-dd format for json output
                    dataDict['installationDate'] = datetime.datetime.strptime(rows['INSTALL_DATE'] ,'%d-%b-%Y').strftime('%Y-%m-%d')
                
                    #Append the each row of dictinary to a list
                    dataList.append(dataDict)
            else:
                     print ("Asset ID : " +   rows['ID'] + " has invalid data")
                     generateErrorLog(logPath,"Asset ID : " +   rows['ID'] + " has invalid data")
        generateErrorLog(logPath, '\n')              
        generateErrorLog(logPath, str(datetime.datetime.now()) + " - End of Log" + '\n')        
        return json.dumps(dataList, indent=4)
      
  except Exception as ex:
          print ("Could not generate a json output - ".format(ex))
          noData = {"result": ['No Data']}          
          return json.dumps(noData)

#################################################
# Functions to validate the incoming csv data   # 
#################################################

# validate Asset ID values 
def validateAssetId(valAssetId):
      
   try:   
       if valAssetId is not None:          
        if valAssetId[0:1].isnumeric():
           if  valAssetId[2] == '/':
               if valAssetId[3:8].isnumeric():
                   return True
   except Exception as ex:
          print ("Error while validating Asset Id - {0} with error desc : - {1}".format(valAssetId , ex))
          return False

# validate Asset Type Code values
def validateAssetTypeCode(valAssetId,valAssetTypeCode):
      
  try:    
      assetTypeCodeList = ['DC', 'MP', 'P', 'PD', 'TN']
      if valAssetTypeCode is not None:
        if valAssetTypeCode  in assetTypeCodeList:
           return True
  except Exception as ex:
         print ("Error while validating Asset Type Code - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valAssetTypeCode,ex))
         return False    
        
# validate Asset Type Description values
def validateAssetTypeDesc(valAssetId,valAssetTypeDesc):
                 
      try:         
          if valAssetTypeDesc is not None:
              if len(valAssetTypeDesc) < 12:
                 return True
      except Exception as ex:
             print ("Error while validating Asset Type Desc - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valAssetTypeDesc,ex))
             return False 

# validate Asset Instal Date is in format dd-MMM-yyyy,
def validateAssetInstDate(valAssetId,valAssetInstDate):
                 
       try:          
          if valAssetInstDate == "":
               return True        
          elif  datetime.datetime.strptime(valAssetInstDate,'%d-%b-%Y'):
               return True
       except Exception as ex:
              print ("Error while validating Asset Instal Date - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valAssetInstDate,ex))
              return False
                 
# validate Easting (BNG) Horizontal coordinate values
def validateEasting(valAssetId,valEasting):
                 
      try:         
          if valEasting is not None:
              if valEasting in range(500000, 560000):
                 return True
      except Exception as ex:
             print ("Error while validating Easting - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valEasting,ex))
             return False
                 

# validate Northing (BNG) Vertical coordinate values
def validateNorthing(valAssetId,valNorthing):
                 
        try:         
          if valNorthing is not None:
              if valNorthing in range(150000, 200000):
                 return True
        except Exception as ex:
               print ("Error while validating Northing - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valNorthing,ex))
               return False         

# validate Asset Road Address values
def validateAssetRoadAddress(valAssetId,valLocation):

   try:              
    if len(valLocation) < 101:
       return True
   except Exception as ex:
          print ("Error while validating Location - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valLocation,ex))
          return False              

# validate Asset Control Server values
def validateCell(valAssetId,valCell):
                 
   try:              
          cellCodeList = ['CNTR', 'EAST', 'NORT', 'OUTR', 'SOUT']
          if valCell  in cellCodeList:
             return True
   except Exception as ex:
          print ("Error while validating Cell values - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valCell,ex))
          return False
                 
# validate Asset Signal Group ID values
def validateSignalGrpId(valAssetId,valSgnlGrpId):
                 
     try:            
          if len(valSgnlGrpId) < 6:
             return True
     except Exception as ex:
            print ("Error while validating Signal Group Id - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valSgnlGrpId,ex))
            return False
                 
# validate Asset Status values
def validateAssetStatus(valAssetId,valstatus):

  try:               
          statusCodeList = ['Active', 'Proposed']
          if valstatus is not None:
              if valstatus  in statusCodeList:
                 return True
  except Exception as ex:
         print ("Error while validating Asset Status  - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valstatus,ex))
         return False
                 
# validate Instal Engineer Name values
def validateEngineerName(valAssetId,valEngrName):
                 
   try:
          if len(valEngrName) < 16:
             return True
   except Exception as ex:
          print ("Error while validating Engineer name  - {1} value for the Asset id - {0} with error : {2}".format(valAssetId,valEngrName,ex))
          return False 


 
if __name__ == "__main__":
      
    get_json(csvPath,logPath)
