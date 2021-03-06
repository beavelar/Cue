# Realtime Support Scripts
The realtime support scripts can be utilized to write, delete, and retrieve parsed realtime unusual options activity data.

## Quick Links
- [Requirements](#requirements)
- [Scripts](#scripts)
  - [Delete Realtime](#delete-realtime)
  - [Get Realtime](#get-realtime)
  - [Write Realtime](#write-realtime)

----------------------------------

## Requirements
- PowerShell 7.2.0 (or higher)

----------------------------------

## Scripts
### **Delete Realtime**
The ***delete-realtime.ps1*** script can be utilized to delete all the data within the realtime collection in the database.  At the moment the script can't be utilized to delete a select time range of parsed realtime unusual options activity data.
- Navigate to the parent level ***Cue*** directory
- Open the ***.env*** file and modify the following environment variable
  - **REALTIME_PROXY_ENDPOINT**=***The realtime proxy endpoint. Ex. http://localhost:3001/realtime***
- In a PowerShell console execute the following command
  - `.\delete-realtime.ps1`

### **Get Realtime**
The ***get-realtime.ps1*** script can be utilized to get all the parsed realtime unusual options activity data or a select datetime range.  The retrieved data will be saved onto the location provided by the ***GET_REALTIME_OUTPUT*** environment variable.
- Open the ***.env*** file and modify the following environment variables
  - **REALTIME_PROXY_ENDPOINT**=***The realtime proxy endpoint. Ex. http://localhost:3001/realtime***
  - **GET_REALTIME_START**=***The realtime retrieval start time in seconds. Ex. 1641479400. This is only required if requesting a datetime range instead of the entire dataset***
  - **GET_REALTIME_STOP**=***The realtime retrieval stop time in seconds. Ex. 1641504600. This is only required if requesting a datetime range instead of the entire dataset***
  - **GET_REALTIME_OUTPUT**=***The location to store the retrieved parsed unusual options activity data. Ex. C:\Cue\data\options-recap\realtime\csv***
- In a PowerShell console execute the following command
  - `.\get-realtime.ps1`

### **Write Realtime**
The ***write-realtime.ps1*** script can be utilized parse and write unusual options activity data provided by Unusual Whales into the database.
- Open the ***.env*** file and modify the following environment variables
  - **REALTIME_PROXY_ENDPOINT**=***The realtime proxy endpoint. Ex. http://localhost:3001/realtime***
  - **WRITE_REALTIME_FILE**=***The csv or json filename to utilize without the extension.  If providing a csv, the csv will be parsed to create a json file.  If providing a json file, the json will be used as it.  Only use the json files generated by the script. Ex. 2022-01-06***
  - **WRITE_REALTIME_INPUT**=***The directory of the input csv file. Ex. C:\Cue\data\realtime-alerts\input***
  - **WRITE_REALTIME_OUTPUT**=***The directory of the output json file. Ex. C:\Cue\data\realtime-alerts\output***
- In a PowerShell console execute the following command
  - `.\write-realtime.ps1`