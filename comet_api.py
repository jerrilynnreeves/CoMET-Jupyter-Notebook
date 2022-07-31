import getpass
import requests
import json
from urllib.parse import urlparse
from sys import exit
from os.path import exists

session = requests.Session()
recordGroup = ''
uuid = ''
description = ''

def login ():
    LOGIN_URL = "https://data.noaa.gov/cedit/login/wsLogin"

    username = str(input("Enter Username: "))
    password = str(getpass.getpass(prompt='Enter password: '))

    PARAMS = {'username': username, 'password': password}

    resp = session.post(LOGIN_URL, params = PARAMS)

    print(resp.text)

    if resp.text == "success" :
        print(username + " successfully logged in")
    else :
        print("Please rerun this function; your login failed")

def search ():
    print(">> Searching " + recordGroup)

    SEARCH_URL = "https://data.noaa.gov/cedit/metadata/search"
    
    PARAMS = getParams ("/metadata/search", "get")
    
    resp = session.get(SEARCH_URL, params = PARAMS)
    return returnResponse (resp)

def validate ():
    global uuid 
    uuid = str(input('Enter a UUID: ' ))
    print(">> Validating " + uuid)

    VALIDATE_URL = "https://data.noaa.gov/cedit/metadata/validate/"

    PARAMS = getParams ("/metadata/validate/{uuid}", "get")
    
    resp = session.get(VALIDATE_URL+uuid, params=PARAMS)

    #reset the global UUID
    uuid = ''

    return returnResponse (resp)

def create ():
    global description
    IMPORT_URL = "https://data.noaa.gov/cedit/metadata/import"
    filename = "./uploads/"+input("Enter the filename (required): ")
    
    # if the file cannot be found, exit; otherwise ask for title and upload
    file_exists = exists(filename)
    if not file_exists:
        print("Could not locate the file: " + filename)
    else:
        print(">> Trying to upload "+filename)
        description = input("Enter a Title for this record (required): ")

        PARAMS = getParams ("/metadata/import", "post")
        headers = {'Content-Type': 'application/xml'}

        with open(filename, 'rb') as f:
            resp = session.post(IMPORT_URL, headers = headers, params = PARAMS, data = f)        
            
            # reset the description in case something else is uploaded
            description = ''
            
            return returnResponse (resp)

def delete ():
    global uuid 
    uuid = str(input('Enter a UUID: ' ))
    print(">> Deleting " + uuid)
    
    DELETE_URL = "https://data.noaa.gov/cedit/metadata/"

    PARAMS = getParams ("/metadata/{uuid}", "delete")

    resp = session.delete(DELETE_URL+uuid, params=PARAMS)

    #reset the global UUID
    uuid = ''

    return returnResponse (resp)

def update ():
    UPDATE_URL = "https://data.noaa.gov/cedit/metadata/"
    filename = "./uploads/"+input("Enter the filename (required): ")
    
    # if the file cannot be found, exit; otherwise ask for title and upload
    file_exists = exists(filename)
    if not file_exists:
        print("Could not locate the file: " + filename)
    else:
        global uuid 
        global description

        uuid = str(input("Enter UUID of record to update: "))
        print(">> Trying to update " + uuid +" with " + filename)

        PARAMS = getParams ("/metadata/{uuid}", "put")
        headers = {'Content-Type': 'application/xml'}

        with open(filename, 'rb') as f:
            resp = session.put(UPDATE_URL+uuid, headers=headers, params=PARAMS, data = f)
            
            # reset the global description and UUID
            description = ''
            uuid = ''
            
            return returnResponse (resp)

def export():
    EXPORT_URL = "https://data.noaa.gov/cedit/metadata/"
    global uuid
    uuid = input("Enter UUID of record to export: ")
    filename = input("Save file with this name: ")

    print(">> Exporting " + uuid)
    PARAMS = getParams ("/metadata/{uuid}", "get")
    
    resp = session.get(EXPORT_URL+uuid, params=PARAMS)
    domain = urlparse(resp.url).netloc

    # reset the global UUID
    uuid = ''

    if "auth" in domain:
        print("Your session expired...please login")
    else:
        print(resp.status_code)
        if resp.status_code == 200:
            with open("./exports/" + filename, 'wb') as f:
                f.write(resp.content)
                return(filename + " created in exports directory")
        else:
            print(resp.text)
    
def returnResponse (resp):
    domain = urlparse(resp.url).netloc

    if "auth" in domain:
        print("Your session expired...please login")
        login()
    else:
        print(resp.status_code)
        return(resp.text)

# ToDo: When API is on prod create a function that allows people to update the openapi.json file.
# API parameter functions
def getParams (endpoint, method):
    global uuid
    global recordGroup
    global description

    d = {}
    with open("openapi.json", 'r') as f:
        data = json.load(f)
        for i in data['paths'][endpoint][method]["parameters"]:
            param = (i["$ref"].split('/')[-1])
            # Parameter should be a query parameter, not a path parameter
            if str(data['components']["parameters"][param]["in"]) == "query":
                name = data['components']["parameters"][param]["name"]
                try:
                    default = data['components']["parameters"][param]["schema"]["default"]
                except:
                    default = ''
                
                if name == "description":
                    default = description
                
                if name == "recordGroup":
                    default = recordGroup

                d[name] = default
            
        PARAMS = d
        print(">> Starting query parameters: ", PARAMS)
        return modifyParams(PARAMS)

def modifyParams(PARAMS):
    # Find out if user wants to modify the parameters to be used
    changeParams = str(input("Would you like to change any of the params (y for yes n for no): "))
    
    if changeParams == 'y' :
        print(">> User requested changing query parameters")
        for k, v in PARAMS.items():
            value = changePrompt(k, v)
            PARAMS[k] = value
    
    # remove any params that are ''
    new_params = {key: val for key,
            val in PARAMS.items() if val != ''}

    print (">> Requested query parameters: ", new_params)
    return new_params

def changePrompt(key, value):
    if key != "description":
        userValue = str(input('To keep > {} < as "{}", type keep; press enter to delete, or type a new value to change '.format(key, value)));
    else:
        userValue = value

    if (userValue == "keep") :
        userValue = value
    
    return userValue

# When import is invoked set-up everthing we need a server session & a default record group (can be changed)
login()

recordGroup = str(input("Enter your Record Group "))
print("Record Group to be searched: " + recordGroup)