from flask import Flask,request,abort
from flask import Flask, send_from_directory, abort
import uuid
import json
import json
import math, random
import numpy as np
import pymysql
import requests
import json
import pymysql
from flask_cors import CORS
from datetime import datetime
from config import Connection
import databasefile
from config import Connection
import commonfile
import ConstantData
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
import razorpay



from flask import Flask, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'




@app.route('/userSignup', methods=['POST'])
def userSignup():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['mobileNo','deviceKey']
        commonfile.writeLog("userSignup",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
            column,values="",""
            
           
            
            mobileNo=inputdata["mobileNo"]
            deviceKey=inputdata["deviceKey"]
            usertypeId="2"
            
          
            
            digits = "0123456789"
            otp = " "
            for i in range(4):
                otp += digits[math.floor(random.random() * 10)]

           

            UserId = (commonfile.CreateHashKey(mobileNo,userTypeId)).hex
            
            
            WhereCondition = " and mobileNo = '" + str(mobileNo) + "'"
            count = databasefile.SelectCountQuery("userMaster",WhereCondition,"")
            
            if int(count) > 0:
                WhereCondition = " mobileNo = '" + str(mobileNo) + "'"
                column = " otp = '" + str(otp)  + "'"
                updateOtp = databasefile.UpdateQuery("userMaster",column,WhereCondition)
                print(updateOtp,'updatedata')
                if updateOtp != "0":
                    column = '*'
                    data = databasefile.SelectQuery("userMaster",column,WhereCondition)                  
                    print(data,"===================")
                    return data
                else:
                    return commonfile.Errormessage()
                
            else:
               

                if 'email' in inputdata:
                    email=inputdata["email"]
                    column=column+" ,email"
                    values=values+"','"+str(email)
                if 'password' in inputdata:
                    password=inputdata["password"]
                    column=column+" ,password"
                    values=values+"','"+str(password)


 
                currentLocationlatlong=""

                column="mobileNo,userId,otp,userTypeId,deviceKey"+column
                
                
                values=  "'"+str(mobileNo)+"','"+str(UserId)+"','"+str(otp)+"','"+str('2')+"','"+str(deviceKey)+values+ "'"
                data=databasefile.InsertQuery("userMaster",column,values)
             

                if data != "0":
                    column = '*'
                    
                    data = databasefile.SelectQuery2("userMaster",column,WhereCondition,"",startlimit,endlimit)
                    print(data)
                    Data = {"status":"true","message":"","result":data["result"][0]}                  
                    return Data
                else:
                    return commonfile.Errormessage()
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/userVerifyOtp', methods=['POST'])
def userverifyOtp():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['otp','mobileNo']
        print(inputdata,"B")
        commonfile.writeLog("userverifyOtp",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg =="1":
            otp=str(inputdata['otp'])
            mobileNo=str(inputdata['mobileNo'])

            column="mobileNo,otp,userId,userTypeId"
            whereCondition= "  otp='" + otp+ "' and mobileNo='" + mobileNo+"'"
            verifyOtp=databasefile.SelectQuery(" userMaster ",column,whereCondition)
            print("verifyOtp======",verifyOtp)
            if  (verifyOtp["status"]!="false") or verifyOtp!=None: 
                return verifyOtp
            else:
                return verifyOtp 
        else:
            return msg         
 
    except KeyError :
        print("Key Exception---->")   
        output = {"result":"key error","status":"false"}
        return output  

    except Exception as e :
        print("Exceptio`121QWAaUJIHUJG n---->" +str(e))    
        output = {"result":"somthing went wrong","status":"false"}
        return output


@app.route('/updateuserProfile', methods=['POST'])
def updateDriverProfile():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ["name","email","password",'userId']
        commonfile.writeLog("updateuserProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            name,email,password,userTypeId,mobileNo,gender="","","","","",""
            column,values="",""
            
          

            
            if 'email' in inputdata:
                email=inputdata["email"]
                column=" email='"+str(email)+"' " 
            if 'name' in inputdata:
                name=inputdata["name"]
                column=column+" ,name='"+str(name)+"' "  
            if 'password' in inputdata:
                password=inputdata["password"]
                column=column+" ,password= '"+str(password)+"' "                
            if 'mobileNo' in inputdata:
                mobileNo=inputdata["mobileNo"]
                column=column+" ,mobileNo='"+str(mobileNo)+"' "

            if 'gender' in inputdata:
                gender=inputdata["gender"]
                column=column+" ,gender='"+str(gender)+"' "   

            if 'userId' in inputdata:
                userId=inputdata["userId"]    
                
            
            whereCondition= " userId= '"+str(userId)+"' and userTypeId='2' "
          
            data=databasefile.UpdateQuery("userMaster",column,whereCondition)
         

            if data != "0":
                Data = {"status":"true","message":"data Updated Successfully","result":"data Updated Successfully"}                  
                return Data
            else:
                return commonfile.Errormessage()
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output        





#user Login
@app.route('/userLogin', methods=['POST'])
def userlogin():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['password','mobileNo']
        commonfile.writeLog("Login",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            mobileNo = inputdata["mobileNo"]
            password = inputdata["password"]
            column=  "us.mobileNo,us.name,us.userId,um.name as userName"
            whereCondition= "us.mobileNo = '" + str(mobileNo) + "' and us.password = '" + password + "' and us.userTypeId=um.id"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):   
                Data = {"result":loginuser,"status":"true"}                  
                return Data
            else:
                data={"status":"Failed","result":"Login Failed"}
                return data

        else:
            return msg 
    except KeyError as e:
        print("Exception---->" +str(e))        
        output = {"result":"Input Keys are not Found","status":"false"}
        return output    
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"result":"something went wrong","status":"false"}
        return output

#user can see his wallet Balance         

@app.route('/userWallet', methods=['POST'])
def userWallet():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['mobileNo','userId']
        commonfile.writeLog("userWallet",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            mobileNo = inputdata["mobileNo"]
            userId=inputdata['userId']
           
            column=  "us.walletBalance  as money"
            whereCondition= "us.mobileNo = '" + str(mobileNo) + "'and us.userTypeId=um.id and us.userId='" + str(mobileNo) + "'"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):
                Data = {"result":loginuser,"status":"true"}                  
                return Data
            else:
                data={"status":"Failed","result":"Login Failed"}
                return data

        else:
            return msg 
    except KeyError as e:
        print("Exception---->" +str(e))        
        output = {"result":"Input Keys are not Found","status":"false"}
        return output    
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"result":"something went wrong","status":"false"}
        return output

#user Can add Money to his wallet

@app.route('/addMoney', methods=['POST'])
def addmoney():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['mobileNo','userId']
        commonfile.writeLog("userWallet",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            mobileNo = inputdata["mobileNo"]
            userId=inputdata['userId']
            money=inputdata['money']
           
            column=  "us.walletBalance  as money"
            whereCondition= "us.mobileNo = '" + str(mobileNo) + "'and us.userTypeId=um.id and us.userId='" + str(mobileNo) + "'"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):
                money1=loginuser1['money']
                totalMoney=money1+money
                columns="walletBalance='"+str(totalMoney)+"'"
                whereCondition=  " mobileNo = '" + str(mobileNo) + "' and userId='" + str(mobileNo) + "' "
                addmoney=databasefile.UpdateQuery('userMaster',columns,whereCondition)


                Data = {"result":loginuser,"status":"true"}                  
                return Data
            else:
                data={"status":"Failed","result":"Login Failed"}
                return data

        else:
            return msg 
    except KeyError as e:
        print("Exception---->" +str(e))        
        output = {"result":"Input Keys are not Found","status":"false"}
        return output    
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"result":"something went wrong","status":"false"}
        return output



















if __name__ == "__main__":
    CORS(app, support_credentials=True)
    app.run(host='0.0.0.0',port=5033,debug=True)















