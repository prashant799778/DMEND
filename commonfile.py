
from datetime import datetime,timedelta
import pytz 
import json
import config
import hashlib
import random
import uuid
 
#current datetime time zone india


def CurrentDatetime():
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(tz=ist)
    ist_f_time = str(ist_time.strftime("%Y-%m-%d %H:%M:%S"))

    return ist_f_time

def AddDaysInCurrentDate(noofdays):
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(tz=ist)
    ist_time = ist_time + timedelta(days=noofdays)
    ist_f_time = str(ist_time.strftime("%Y-%m-%d %H:%M:%S"))

    return ist_f_time

def Errormessage():
    data = {"status":"false","message":"Somthing went wrong please contact system admin","result":""}
    return data

def NoRecordFoundmessage():
    data = {"status":"false","message":"No Record Found","result":[]}
    return data   

def IncorrectUserPasswordMsg():
    data = {"status":"false","message":"Enter Correct UserID Password","result":""}
    return data    

def EmailAlreadyExistMsg():
    data = {"status":"false","message":"Email Already Exists","result":""}
    return data


def likeAlreadyExistMsg():
    data = {"status":"false","message":"You have  Already liked","result":""}
    return data


def EventInterstAlreadyExistMsg():
    data = {"status":"false","message":"You have  Already Interested Event","result":""}
    return data



def CountryAlreadyExistMsg():
    data = {"status":"false","message":"Country Already Exists","result":""}
    return data 


def QualificationAlreadyExistMsg():
    data = {"status":"false","message":"Qualification Already Exists","result":""}
    return data 


def UniversityAlreadyExistMsg():
    data = {"status":"false","message":"UniversityAlready Exists","result":""}
    return data        



def EmailMobileAlreadyExistMsg():
    data = {"status":"false","message":"Email Or MobileNo Already Exists","result":""}
    return data  

def postTitlepostDescriptionAlreadyExistMsg():
    data = {"status":"false","message":"postTitle Or postDescription Already Exists","result":""}
    return data      

def aboutUsDescriptionAlreadyExistMsg():
    data = {"status":"false","message":"aboutUs Description Already Exists","result":""}
    return data      

def MobileNoNotFound():
    data = {"status":"false","message":"MobileNo Not Exists","result":""}
    return data   

def truemessage():
    data = {"status":"true","message":"","result":""}
    return data   

def RecordExistMsg():
    data = {"status":"false","message":"Record Already Exists","result":""}
    return data 

def InputKeyNotFoundMsg():
    data = {"status":"false","message":"Input Keys Not Found","result":""}
    return data 

def ResponceWithInputresult(result):
    data = {"status":"true","message":"","result":result}
    return data

def ResponceWithInputmessage(msg,status):
    data = {"status":status,"message":msg,"result":""}
    return data

#success message for crud operation
def Successmessage(type):
    if type == "insert":
        output ="Record Inserted Successfully"
    elif type == "update":
        output ="Record Updated Successfully"
    elif type == "delete":
        output ="Record Deleted Successfully"

    return output

def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data

def CreateHashKey(FirstKey,SecoundKey):
    # hash = hashlib.sha256()
    # hash.update(('%s%s' % (FirstKey,SecoundKey)).encode('utf-8'))
    Hashkey = uuid.uuid1()

    return Hashkey

def createShareurl(FirstKey,SecoundKey):
    
    inputtext = (FirstKey + SecoundKey)
    
    hash = hashlib.sha256()
    hash.update(inputtext.encode('utf-8'))  
    url = hash.hexdigest()
       
    return url

def GetRandomNo():
    RandomNo = str(random.randint(100000,999999))      

    return RandomNo

def MandatoryKeyMessage(KeyName):
    data = {"status":"false","message": KeyName + " Not Found","result":""}
    return data  
    
def CheckKeyNameBlankValue(Keyvalue,inputdata):
        
    for keyname in Keyvalue:               
        if keyname not in inputdata:                                   
            msg = MandatoryKeyMessage(keyname)
            return msg
        else:
            if inputdata[keyname] == "": 
                msg = MandatoryKeyMessage(keyname)
                return msg
    return "1"

def CheckIfAnyOneExists(Keyvalue,inputdata):
    
    for keyname in Keyvalue:               
        if keyname in inputdata and inputdata[keyname] != "":                                                
            return "1"        

    data = {"status":"false","message": "Enter Any One value in " + str(Keyvalue),"result":""}
    return data

def Saveimage(file):
                   
    # filename = file.filename or ''                 
    # filename = filename.replace("'","") 

    # #folder path to save campaign image
    # FolderPath = ConstantData.GetCampaignImagePath(filename)  

    # filepath = '/CampImages/' + filename    

    # file.save(FolderPath)
    # CampImagePath = filepath


    return "1"

def EscapeSpecialChar(string):

    newstr = string.translate(str.maketrans({"-":r"\-","]":r"\]","\\":r"\\","^":r"\^","$":r"\$","*":r"\*",".":r"\.","'":r"\'"}))

    return newstr

def writeLog(apiName,data,flag):
    try:
       
        ist = pytz.timezone('Asia/Kolkata')
        ist_time = datetime.now(tz=ist)
        ist_f_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")
       
        data["time"] = str(ist_f_time)
        data["api"] = str(apiName)
       
        if flag == 0:
            log = open("/var/www/medParliament/backend/med_parliament/request.log", "a")
        elif flag == 1:
            log = open("/var/www/medParliament/backend/med_parliament/response.log", "a")
    
        log.write(str(data) + "\n")
        log.close()

        return 1
    except Exception as e:
        print("Error--->" + str(e))   
        return 0

   
# def ValidateUser():

# def ValidateAdminUser():



