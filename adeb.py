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
from math import sin,cos,sqrt,atan2,radians
import paho.mqtt.client as mqtt
from decimal import Decimal
import re
#import razorpay




from flask import Flask, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'





@app.route('/selectUserTypeMaster', methods=['GET'])
def selectUserTypeMaster():
    try:
        columns=" id, usertype "
        
        data = databasefile.SelectQueryMaxId("userTypeMaster",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output 


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
            email=inputdata['email']
            deviceKey=inputdata["deviceKey"]
            usertypeId="2"
            
          
            
            digits = "0123456789"
            otp = " "
            for i in range(4):
                otp += digits[math.floor(random.random() * 10)]

           

            UserId = (commonfile.CreateHashKey(mobileNo,usertypeId)).hex
            
            
            WhereCondition = " and mobileNo = '" + str(mobileNo) + "' or email ='" + str(email) + "' "
            count = databasefile.SelectCountQuery("userMaster",WhereCondition,"")
            
            if int(count) > 0:
                WhereCondition = " AND  mobileNo = '" + str(mobileNo) + "'"
                column = " otp = '" + str(otp)  + "'"
                updateOtp = databasefile.UpdateQuery("userMaster",column,WhereCondition)
                print(updateOtp,'updatedata')
                if updateOtp != "0":
                    column = '*'
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition)                  
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
                if 'name' in inputdata:
                    name=inputdata["name"]
                    column=column+" ,name"
                    values=values+"','"+str(name)



 
                currentLocationlatlong=""

                column="mobileNo,userId,otp,userTypeId,deviceKey"+column
                
                
                values=  "'"+str(mobileNo)+"','"+str(UserId)+"','"+str(otp)+"','"+str('2')+"','"+str(deviceKey)+values+ "'"
                data=databasefile.InsertQuery("userMaster",column,values)
             

                if data != "0":
                    column = '*'
                    
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition)
                    print(data)
                    Data = {"status":"true","message":"","result":data["result"]}                  
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
            whereCondition= "and   otp=" + otp+ " and mobileNo=" + mobileNo+""
            verifyOtp=databasefile.SelectQuery1(" userMaster ",column,whereCondition)
            print("verifyOtp======",verifyOtp)
            if  (verifyOtp["status"]!="false"): 
                return verifyOtp
            else:
            	data={"result":"","message":"Invalid Otp","status":"false"}
            	return data
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



#user Login
@app.route('/userLogin', methods=['POST'])
def userlogin():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['password','mobileNo']
        commonfile.writeLog("userLogin",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            mobileNo = inputdata["mobileNo"]
            password = inputdata["password"]
            column=  "us.mobileNo,us.name,us.userId,um.usertype as userTypeId"
            whereCondition= " and us.mobileNo = '" + str(mobileNo) + "' and us.password = '" + password + "' and us.userTypeId=um.id"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser['status']!='false'):   
                              
                return loginuser
            else:
                data={"status":"false","message":"Please enter correct Password & Email","result":""}
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
                
            
            whereCondition= " and  userId= '"+str(userId)+"' and userTypeId='2' "
          
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





@app.route('/userProfile', methods=['POST'])
def userProfile():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['userId']
        commonfile.writeLog("userProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
        

            
            
            if 'userId' in inputdata:
                userId=inputdata["userId"]    
                
            
            whereCondition= " and userId= '"+str(userId)+"' and userTypeId='2' "
            column='userId,name,mobileNo,password,email,gender'

            
         
            data11=databasefile.SelectQuery1('userMaster',column,whereCondition)
         

            if data11['status'] != "false":
                Data = {"status":"true","message":"data Updated Successfully","result":data11['result']}                  
                return Data
            else:
                data={"status":"false","result":"","message":"Invalid User"}
                return data
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
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
            whereCondition= " and us.mobileNo = '" + str(mobileNo) + "'and us.userTypeId=um.id and us.userId='" + str(userId) + "'"
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
            whereCondition= " and us.mobileNo = '" + str(mobileNo) + "'and us.userTypeId=um.id and us.userId='" + str(userId) + "'"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            print(loginuser)
            if (loginuser!=0):
                money1=loginuser['result']['money']
                totalMoney=int(money1)+int(money)
                print(totalMoney,"+++++++++++")
                columns="walletBalance='"+str(totalMoney)+"'"
                whereCondition=  " and mobileNo = '" + str(mobileNo) + "' and userId='" + str(userId) + "' "
                addmoney=databasefile.UpdateQuery('userMaster',columns,whereCondition)


                                
                return addmoney
            else:
                data={"status":"false","message":"Login Failed","result":"Login Failed"}
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



@app.route('/generateOtp', methods=['POST'])
def generateOtp():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['email']
        print(inputdata,"B")
        commonfile.writeLog("generateOtp",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg =="1":
            email=str(inputdata["email"])

            digits = "0123456789"
            OTP = ""
            for i in range(4):
                OTP += digits[math.floor(random.random() * 10)]
            message = Mail(
                from_email = 'adeb@achievers.com',
                to_emails = str(email),
                subject = "Otp for Reset Password",
                html_content = '<strong> Otp To Reset Your Password is:' + str(OTP) + ' </strong> <br> <br> Thanks<br> <br> ADEB Team')
            sg = SendGridAPIClient('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')
            response = sg.send(message)
           


          
            column="otp='" + str(OTP)+ "'"
            whereCondition= "  and email = '" + str(email)+ "' "
            output=databasefile.UpdateQuery("userMaster",column,whereCondition)
            columns='otp'
            
            data=databasefile.SelectQuery("userMaster",columns,whereCondition,"",startlimit,endlimit)
            if data['result']!="":
                Data = {"status":"true","message":"","result":data["result"]}                  
                return Data
            else:
                return {"status":"false","message":"Invalid Email","result":""}  
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

@app.route('/updatePassword', methods=['POST'])
def updatePassword():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['email','password']
        print(inputdata,"B")
        commonfile.writeLog("updatePassword",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg =="1":
            email=str(inputdata["email"])
            password=str(inputdata["password"])
         
            column="password='" + password+ "'"
            whereCondition= "  and email = '" + str(email)+ "' "
            output=databasefile.UpdateQuery("userMaster",column,whereCondition)
                       
            if output!='0':
                Data = {"status":"true","message":commonfile.Successmessage('update'),"result":""}                   
                return Data
            else:
                return commonfile.Errormessage()    
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



@app.route('/enterOtp', methods=['POST'])
def verifyOtp1():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['otp','email']
        print(inputdata,"B")
        commonfile.writeLog("enterOtp",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg =="1":
            otp=str(inputdata['otp'])
            email=str(inputdata['email'])

            column="email"
            whereCondition= " and otp='" + otp+ "' and email='" + email+ "'  "
            data1=databasefile.SelectQuery1("userMaster",column,whereCondition)
            if  (data1["status"]!="false"):   
                Data = {"status":"true","message":"","result":data1["result"]}                  
                return Data
            else:
                data = {"status":"false","message":"Invalid OTP","result":""}
                return data      
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


@app.route('/updatepaymentType', methods=['POST'])
def updatepaymentType():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['paymentType','id']
        commonfile.writeLog("updatepaymentType",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            paymentType = inputdata["paymentType"]
            id = inputdata["id"]
            column= " * "
            whereCondition=" and id = '" + str(id)+ "'"
            data1 = databasefile.SelectQuery1("paymentTypeMaster",column,whereCondition)
            print(data1,"data1")
            if data1 != 0:
                column = ""
                whereCondition = ""
                column= " paymentType='" + str(paymentType) + "'"
                whereCondition=" and id = '" + str(id)+ "'"
                data = databasefile.UpdateQuery("paymentTypeMaster",column,whereCondition)
                print(data,'===')
                output = {"result":"Updated Successfully","status":"true"}
                return output
            else:
                output = {"result":"Data Not Found","status":"true"}
                return output
        else:
            return msg
    except KeyError :
        print("Key Exception---->")   
        output = {"result":"key error","status":"false"}
        return output  

    except Exception as e :
        print("Exception---->" +str(e))    
        output = {"result":"somthing went wrong","status":"false"}
        return output

@app.route('/paymentTypeMaster', methods=['GET'])
def paymentTypeMaster():
    try:
        msg = "1"
        if msg=="1":
            column="id ,paymentType"
            whereCondition=" "
            data=databasefile.SelectQueryMaxId("paymentTypeMaster",column,whereCondition)
        
            if (data!=0):           
                
                return data
            else:
                output = {"message":"No Data Found","result":"No Data Found","status":"false"}
                return output
        else:
            return msg
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output


@app.route('/addpaymentType', methods=['POST'])
def addpaymentType():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['paymentType']
        commonfile.writeLog("addpaymentType",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            paymentType = inputdata["paymentType"]
            column="*"
            whereCondition= " and paymentType='"+str(paymentType)+ "'"
            data=databasefile.SelectQuery1("paymentTypeMaster",column,whereCondition)
            print(data,'data')
            if data['status']=='false':
                column="paymentType"
                values="'"+str(paymentType)+"' "
                insertdata=databasefile.InsertQuery("paymentTypeMaster",column,values)
                column="*"
                whereCondition= " and  paymentType='"+str(paymentType)+ "'"
                data1=databasefile.SelectQuery1("paymentTypeMaster",column,whereCondition)

                output= {"result":"User Added Successfully","ambulance Details":data1['result'],"status":"true"}
                return output
            else:
                output = {"result":"User Already Added Existed ","status":"true","ambulance Details":data}
                return output
        else:
            return msg 
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output




@app.route('/deletepaymentTypeMaster', methods=['POST'])
def deletepaymentTypeMaster():
    try: 

        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        WhereCondition=""
  
        if len(inputdata) > 0:           
            commonfile.writeLog("paymentTypeMaster",inputdata,0)
        
        keyarr = ['id']
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if "id" in inputdata:
            if inputdata['id'] != "":
                Id =inputdata["id"] 
                WhereCondition=WhereCondition+" and id='"+str(Id)+"'" 
        if msg == "1":                        
            
            data = databasefile.DeleteQuery("paymentTypeMaster",WhereCondition)

            if data != "0":
                return data
            else:
                return commonfile.Errormessage()
        else:
            return msg

    except Exception as e :
        print("Exception--->" + str(e))                                  
        return commonfile.Errormessage()

#___________driver_

@app.route('/driverSignup', methods=['POST'])
def driverSignup():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['mobileNo','deviceKey']
        commonfile.writeLog("driverSignup",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
            column,values="",""
            
           
            
            mobileNo=inputdata["mobileNo"]
            deviceKey=inputdata["deviceKey"]
            usertypeId="3"
            
          
            
            digits = "0123456789"
            otp = " "
            for i in range(4):
                otp += digits[math.floor(random.random() * 10)]

           

            UserId = (commonfile.CreateHashKey(mobileNo,usertypeId)).hex
            
            
            WhereCondition = " and mobileNo = '" + str(mobileNo) + "'"
            count = databasefile.SelectCountQuery("userMaster",WhereCondition,"")
            
            if int(count) > 0:
                WhereCondition = " and mobileNo = '" + str(mobileNo) + "'"
                column = " otp = '" + str(otp)  + "'"
                updateOtp = databasefile.UpdateQuery("userMaster",column,WhereCondition)
                print(updateOtp,'updatedata')
                if updateOtp != "0":
                    column = '*'
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition)                  
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
                if 'name' in inputdata:
                    name=inputdata["name"]
                    column=column+" ,name"
                    values=values+"','"+str(name)



 
                currentLocationlatlong=""

                column="mobileNo,userId,otp,userTypeId,deviceKey"+column
                
                
                values=  "'"+str(mobileNo)+"','"+str(UserId)+"','"+str(otp)+"','"+str('2')+"','"+str(deviceKey)+values+ "'"
                data=databasefile.InsertQuery("userMaster",column,values)
             

                if data != "0":
                    column = '*'
                    
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition)
                    print(data)
                    Data = {"status":"true","message":"","result":data['result']}                  
                    return Data
                else:
                    return commonfile.Errormessage()
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/driverVerifyOtp', methods=['POST'])
def driververifyOtp():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['otp','mobileNo']
        print(inputdata,"B")
        commonfile.writeLog("driververifyOtp",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg =="1":
            otp=str(inputdata['otp'])
            mobileNo=str(inputdata['mobileNo'])

            column="mobileNo,otp,userId,userTypeId"
            whereCondition= "  and  otp=" + otp+ " 		and mobileNo= " + mobileNo+" "
            verifyOtp=databasefile.SelectQuery1(" userMaster ",column,whereCondition)
            print("verifyOtp======",verifyOtp)
            if  (verifyOtp["status"]!="false"): 
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




@app.route('/driverProfile', methods=['POST'])
def driverProfile():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['userId']
        commonfile.writeLog("driverProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
        

            
            
            if 'userId' in inputdata:
                userId=inputdata["userId"]    
                
            
            whereCondition= " and userId= '"+str(userId)+"' and userTypeId='3' "
            column='userId,name,mobileNo,password,email'

            
         
            data11=databasefile.SelectQuery1('userMaster',column,whereCondition)
         

            if data11['status'] != "false":
                Data = {"status":"true","message":"data Updated Successfully","result":data11['result']}                  
                return Data
            else:
                data={"status":"false","result":"","message":"Invalid User"}
                return data
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/updateDriverProfile', methods=['POST'])
def updateDriverProfile12():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ["name","email","password",'userId']
        commonfile.writeLog("updateDriverProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            name,email,password,userTypeId,mobileNo,gender="","","","","",""
            column,values="",""
            columns2,values2="",""
        

            
            if 'email' in inputdata:
                email=inputdata["email"]
                column=" email='"+str(email)+"' " 
            if 'name' in inputdata:
                name=inputdata["name"]
                column=column+" ,name='"+str(name)+"' "  
                column2= " name='"+str(name)+"' " 
            if 'password' in inputdata:
                password=inputdata["password"]
                column=column+" ,password= '"+str(password)+"' "                
            if 'mobileNo' in inputdata:
                mobileNo=inputdata["mobileNo"]
                column=column+" ,mobileNo='"+str(mobileNo)+"' "
                column2=column2+" ,mobileNo='"+str(mobileNo)+"' "  

            if 'userId' in inputdata:
                driverId=inputdata["userId"]    
                
            
            whereCondition= " and  driverId= '"+str(driverId)+"' "
            whereCondition2= " and  userId ='"+str(driverId)+"' "
          
            data=databasefile.UpdateQuery("driverMaster",column2,whereCondition)
            data11=databasefile.UpdateQuery('userMaster',column,whereCondition2)
         

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


#driver Login
@app.route('/driverLogin', methods=['POST'])
def driverlogin():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['password','mobileNo']
        commonfile.writeLog("driverLogin",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            mobileNo = inputdata["mobileNo"]
            password = inputdata["password"]
            column=  "us.mobileNo,us.name,us.userId,um.usertype,um.id as userTypeId"
            whereCondition= " and us.mobileNo = '" + str(mobileNo) + "' and us.password = '" + str(password) + "' and us.userTypeId=um.id"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):   
                              
                return loginuser
            else:
                data={"status":"false","message":"Please enter correct Password & mobileNo.","result":""}
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
       

@app.route('/driverWallet', methods=['POST'])
def driverWallet():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['mobileNo','userId']
        commonfile.writeLog("driverWallet",inputdata,0)
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

@app.route('/notifyRide', methods=['POST'])
def notifyRide():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ["driverId","bookingId","userId"]
        commonfile.writeLog("notifyRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            if "driverId" in inputdata:
                if inputdata['driverId'] != "":
                    ambulanceId =(inputdata["driverId"])
            if "bookingId" in inputdata:
                    if inputdata['bookingId'] != "":
                        bookingId =str(inputdata["bookingId"])

            if "userId" in inputdata:
                if inputdata['userId'] != "":
                    userId =str(inputdata["userId"])
            
            whereCondition=" driverId= '"+ str(driverId)+"' and bookingId='"+ str(bookingId)+"'"
            column=" status=1 "
            bookRide=databasefile.UpdateQuery("bookDriver",column,whereCondition)
            whereCondition222=  " driverId= '"+ str(driverId)+"' "
            columns= "onTrip=1 and onDuty=1"
            bookRide1=databasefile.UpdateQuery("driverRideStatus",columns,whereCondition222)
            if (bookRide!=0):   
                bookRide["message"]="ride notified Successfully"             
                topic=str(userId)+"/notifyRide"
                client.publish(topic, str(bookingDetails)) 
                return bookRide
            else:
                
                return bookRide
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




@app.route('/startRide', methods=['POST'])
def startRide():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ["driverId","bookingId","userId"]
        commonfile.writeLog("endRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":


            if "driverId" in inputdata:
                if inputdata['driverId'] != "":
                    ambulanceId =(inputdata["driverId"])
            if "bookingId" in inputdata:
                    if inputdata['bookingId'] != "":
                        bookingId =str(inputdata["bookingId"])

            if "userId" in inputdata:
                if inputdata['userId'] != "":
                    userId =str(inputdata["userId"])

            corporateBookingType=inputdata['corporateBookingType']
            
            whereCondition=" driverId= '"+ str(driverId)+"' and bookingId='"+ str(bookingId)+"'"
            column=" bookingTypeId"
            bookRide=databasefile.SelectQuery1("bookDriver",column,whereCondition)

            bookingTypeId= bookRide['result']['bookingId']
            if bookingTypeId ==1 or bookingTypeId =='1':

                column=" status=2 "
                bookRide=databasefile.UpdateQuery("bookDailyDriver",column,whereCondition)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")


                
            if bookingTypeId ==2 or bookingTypeId =='2':
                print('1')

            if bookingTypeId ==3 or bookingTypeId =='3':
                print('hourly')

                column=" status=2 "
                bookRide=databasefile.UpdateQuery("bookHourlyMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")

            if bookingTypeId ==4 or bookingTypeId =='4':
                
                column=" status=2 "
                bookRide=databasefile.UpdateQuery("bookOneMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
                
                print('one')
            
            if bookingTypeId == 5 or bookingTypeId =='5':
                print('round')

                column=" status=2 "
                bookRide=databasefile.UpdateQuery("bookRoundMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")


            




            whereCondition222=  " driverId= '"+ str(driverId)+"' "
            columns= "onTrip=1 and onDuty=1"
            bookRide1=databasefile.UpdateQuery("driverRideStatus",columns,whereCondition222)
            if (bookRide!=0):   
                bookingDetails["message"]="ride started Successfully"             
                topic=str(userId)+"/startRide"
                client.publish(topic, str(bookingDetails)) 
                return bookingDetails
            else:
                
                return bookRide
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




@app.route('/endRide', methods=['POST'])
def endRide():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ["driverId","bookingId"]
        commonfile.writeLog("endRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            dropLocationLat, dropLocationLong,dropLocationAddress="","",""


            if "dropLocationLat" in inputdata:
                if inputdata['dropLocationLat'] != "":
                    dropLocationLat =(inputdata["dropLocationLat"])
            if "dropLocationLong" in inputdata:
                if inputdata['dropLocationLong'] != "":
                    dropLocationLong =(inputdata["dropLocationLong"])
            if "dropLocationAddress" in inputdata:
                if inputdata['dropLocationAddress'] != "":
                    dropLocationAddress =str(inputdata["dropLocationAddress"])

            if "driverId" in inputdata:
                if inputdata['driverId'] != "":
                    ambulanceId =(inputdata["driverId"])
            if "bookingId" in inputdata:
                    if inputdata['bookingId'] != "":
                        bookingId =str(inputdata["bookingId"])

            if "userId" in inputdata:
                if inputdata['userId'] != "":
                    userId =str(inputdata["userId"])
            corporateBookingType=inputdata['corporateBookingType']

            whereCondition=" driverId= '"+ str(driverId)+"' and bookingId='"+ str(bookingId)+"'"
            column=" bookingTypeId"
            bookRide=databasefile.SelectQuery1("bookDriver",column,whereCondition)

            bookingTypeId= bookRide['result']['bookingId']

            if bookingTypeId ==1 or bookingTypeId =='1':

                column=" status=3 "
                bookRide=databasefile.UpdateQuery("bookDailyDriver",column,whereCondition)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")


                
            if bookingTypeId ==2 or bookingTypeId =='2':
                print('cc')
                # if   corporateBookingType ==1 or corporateBookingType =='1':
                #     print('1')
                #     select bookingId,morningTime,status=3,endTime(using pytz) from bookCorporateMaster then update into bookMorningCorporate(do this) 
                # else:
                #     select bookingId,morningTime,status=3,endTime(using pytz) from bookCorporateMaster then update into bookEveningCorporate(do this) 

            
            if bookingTypeId ==3 or bookingTypeId =='3':
                print('hourly')

                column=" status=3 "
                bookRide=databasefile.UpdateQuery("bookHourlyMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")

            if bookingTypeId ==4 or bookingTypeId =='4':
                
                column=" status=3 "
                bookRide=databasefile.UpdateQuery("bookOneMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
                
                print('one')
            
            if bookingTypeId == 5 or bookingTypeId =='5':
                print('round')

                column=" status=3 "
                bookRide=databasefile.UpdateQuery("bookRoundMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")

            whereCondition222=  " driverId= '"+ str(driverId)+"' "
            columns= "onTrip=0 and onDuty=1"
            bookRide1=databasefile.UpdateQuery("driverRideStatus",columns,whereCondition222)
            if (bookRide!=0):   
            	bookingDetails["message"]="ride started Successfully"             
            	topic=str(userId)+"/endRide"
            	client.publish(topic, str(bookingDetails)) 
            	return bookingDetails
            else:
                
                return bookRide
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


@app.route('/cancelRide', methods=['POST'])
def cancelRide():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ["driverId","bookingId","userId"]
        commonfile.writeLog("cancelRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            ambulanceId= inputdata["driverId"]
            bookingId=inputdata['bookingId']
            userId=inputdata['userId']
           
            whereCondition=" driverId= '"+ str(driverId)+"' and bookingId='"+ str(bookingId)+"'"
            column=" bookingTypeId"
            bookRide=databasefile.SelectQuery1("bookDriver",column,whereCondition)

            bookingTypeId= bookRide['result']['bookingId']
            if bookingTypeId ==1 or bookingTypeId =='1':

                column=" status=4 "
                bookRide=databasefile.UpdateQuery("bookDailyDriver",column,whereCondition)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")


                
            if bookingTypeId ==2 or bookingTypeId =='2':
                print('cc')
            
            if bookingTypeId ==3 or bookingTypeId =='3':
                print('hourly')

                column=" status=4 "
                bookRide=databasefile.UpdateQuery("bookHourlyMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22)
                print(bookingDetails,"================")

            if bookingTypeId ==4 or bookingTypeId =='4':
                
                column=" status=4 "
                bookRide=databasefile.UpdateQuery("bookOneMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
                
                print('one')
            
            if bookingTypeId == 5 or bookingTypeId =='5':
                print('round')

                column=" status=4 "
                bookRide=databasefile.UpdateQuery("bookRoundMaster",column,whereCondition)
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
                columns=columns+",bm.driverMobile"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
            whereCondition222=  " driverId= '"+ str(driverId)+"' "
            columns= "onTrip=0 and onDuty=1"
            bookRide1=databasefile.UpdateQuery("driverRideStatus",columns,whereCondition222)
            if (bookRide!=0):   
                bookingDetails["message"]="ride started Successfully"             
                topic=str(userId)+"/cancelRide"
                client.publish(topic, str(bookingDetails)) 
                return bookingDetails
            else:
                
                return bookRide
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


#______________________________________________




#________________________

#_________________-admin____________________-
#admin _______Login



@app.route('/adminLogin', methods=['POST'])
def adminLogin():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['email','password']
        commonfile.writeLog("adminLogin",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            email = inputdata["email"]
            password = inputdata["password"]
            column=  "us.mobileNo,us.name,us.userTypeId,um.usertype,us.userId"
            whereCondition= " and  us.email = '" + str(email) + "' and us.password = '" + str(password) + "'  and  us.userTypeId=um.id and us.userTypeId='1' "
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser['status']!='false'):   
            	return loginuser
            else:
            	loginuser = {"status":"False","message":"Please enter correct password & email","result":""}
            	return loginuser
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






@app.route('/selectallUsers', methods=['GET'])
def selectallUsers():
    try:
        columns=" us.usertype,um.name,um.walletBalance,um.email,um.status,um.password,um.mobileNo,um.gender,um.deviceKey  "
        whereCondition=" and um.usertypeId=us.id and um.usertypeId='2' "
        data = databasefile.SelectQuery4("userMaster as um ,usertypeMaster as us",columns,whereCondition)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output 








@app.route('/aboutUs', methods=['POST'])
def aboutUs(): 
    try: 
        startlimit,endlimit="",""   
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        aboutId = '2'
        keyarr = ['description','flag']
        commonfile.writeLog("aboutUs",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":      
            description = commonfile.EscapeSpecialChar(inputdata["description"])
            flag = inputdata["flag"]
            print('====',flag)
        
            WhereCondition = " "
            count = databasefile.SelectCountQuery("aboutUs",WhereCondition,"")
            
            if int(count) > 0 and flag == 'n':
                print('F')         
                return commonfile.aboutUsDescriptionAlreadyExistMsg()
            else:
                if flag == 'n':
                    columns = " description"          
                    values = " '" + str(description) + "'"       
                    data = databasefile.InsertQuery("aboutUs",columns,values)
                    if data != "0":
                        column = '*'
                        WhereCondition = " and description = '" + str(description) + "'"
                        
                        data11 = databasefile.SelectQuery1("aboutUs",column,WhereCondition,"",startlimit,endlimit)
                        return data11
                if flag == 'u':
                    WhereCondition = " and id='" + str(aboutId) + "'"
                    column = " description = '" + str(description) + "'"
                    data = databasefile.UpdateQuery("aboutUs",column,WhereCondition)
                    return data
                else:
                    return commonfile.Errormessage()
        else:
            return msg

    except Exception as e:
        print("Exception--->" + str(e))                                  
        return commonfile.Errormessage() 


@app.route('/deleteAboutUs', methods=['POST'])
def deleteAboutUs():
    try:


        inputdata =  commonfile.DecodeInputdata(request.get_data()) 

        WhereCondition=""
  
        if len(inputdata) > 0:           
            commonfile.writeLog("deleteAboutUs",inputdata,0)
        
        keyarr = ['id']
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if "id" in inputdata:
            if inputdata['id'] != "":
                Id =inputdata["id"] 
                WhereCondition=WhereCondition+" and id='"+str(Id)+"'" 
        if msg == "1":                        
            
            data = databasefile.DeleteQuery("aboutUs",WhereCondition)

            if data != "0":
                return data
            else:
                return commonfile.Errormessage()
        else:
            return msg

    except Exception as e :
        print("Exception--->" + str(e))                                  
        return commonfile.Errormessage()


@app.route('/allaboutUs', methods=['POST'])
def allaboutUs():
    try:
        columns=" * "
        
        data = databasefile.SelectQueryMaxId("aboutUs",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/allUserRating', methods=['POST'])
def allaboutUs222():
    try:
        columns=" driverId,bookingId,ratingId"
        
        data = databasefile.SelectQueryMaxId("userRating",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output


@app.route('/allDriverRating', methods=['POST'])
def allaboutUs99():
    try:
        columns="userId,ratingId,bookingId"
        
        data = databasefile.SelectQueryMaxId("driverRating",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output





@app.route('/allcorporateBookingType', methods=['POST'])
def allcorporateBookingType():
    try:
        columns=" id,name "
        
        data = databasefile.SelectQueryMaxId("corporateBookingType",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output



@app.route('/allbookingTypeMaster', methods=['POST'])
def allbookingTypeMaster():
    try:
        columns="id,bookingType "
        
        data = databasefile.SelectQueryMaxId("bookingTypeMaster ",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output



@app.route('/allCarType', methods=['POST'])
def allCarType():
    try:
        columns="id,name "
        
        data = databasefile.SelectQueryMaxId("gearType  ",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output



@app.route('/allGearType', methods=['POST'])
def allgearType():
    try:
        columns="id,name "
        
        data = databasefile.SelectQueryMaxId(" functionType   ",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output



@app.route('/updateDriverLatLong', methods=['POST'])
def updateDriverLatLong():
    try:
        
        inputdata=commonfile.DecodeInputdata(request.get_data())
       
        keyarr = ['driverId']
       
        
        startlimit,endlimit="",""

        commonfile.writeLog("updateDriverLatLong",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        #print(msg,'msg')
       
        if msg == "1":

            if 'lat' in inputdata:
                lat=inputdata["lat"]

            if 'lng' in inputdata:
                lng=inputdata["lng"]

            if 'driverId' in inputdata:
                driverId=inputdata["driverId"]

           
           
                
                
            WhereCondition2=" driverId= '" + str(ambulanceId) + "'"
            columns23="lat='" + str(lat) + "',lng='" + str(lng) + "'"
            data122=databasefile.UpdateQuery('driverRideStatus',columns23,WhereCondition2)
            print("333333333333")
            if data122 != "0":
                data11={"result":"","message":"Updated successfully","status":"true"}
                return data11

            else:
            	data={"result":"","message":"please enter keys lat,lng & driverId","status":"false"}
            	return data


                        
               
        else:
            return msg
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output


@app.route('/driverAvailability', methods=['POST'])
def driverAvialability():
    try:
        
        inputdata=commonfile.DecodeInputdata(request.get_data())
       
        keyarr = ['driverId']
       
        
        startlimit,endlimit="",""

        commonfile.writeLog("updateDriverLatLong",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        #print(msg,'msg')
       
        if msg == "1":

            if 'avial' in inputdata:
                avial=inputdata["avial"]

            

            if 'driverId' in inputdata:
                driverId=inputdata["driverId"]

           
           
                
                
            WhereCondition2=" driverId= '" + str(ambulanceId) + "'"
            columns23="onDuty='" + str(avial) + "'"
            data122=databasefile.UpdateQuery('driverRideStatus',columns23,WhereCondition2)
            print("333333333333")
            if data122 != "0":
                data11={"result":"","message":"Updated successfully","status":"true"}
                return data11

            else:
            	data={"result":"","message":"please enter keys lat,lng & driverId","status":"false"}
            	return data


                        
               
        else:
            return msg
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output


@app.route('/allratingMaster', methods=['POST'])
def allratingMaster():
    try:
        columns="id,name "
        
        data = databasefile.SelectQueryMaxId("ratingMaster",columns)
       

        if data:           
            Data = {"status":"true","message":"","result":data["result"]}
            return Data
        else:
            output = {"status":"false","message":"No Data Found","result":""}
            return output

    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"status":"false","message":"something went wrong","result":""}
        return output








@app.route('/addUserRating', methods=['POST'])
def addUserRating():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['driverId','bookingId','ratingId']
        commonfile.writeLog("addpaymentType",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            driverId = inputdata["driverId"]
            bookingId=inputdata['bookingId']
            ratingId=inputdata['ratingId']
            
           
            column="driverId,bookingId,ratingId"
            values="'"+str(driverId)+"' ,'"+str(bookingId)+"','"+str(ratingId)+"'"
            insertdata=databasefile.InsertQuery("userRating",column,values)
            

            output= {"result":"Rated Successfully","message":"Rated Successfully","status":"true"}
            return output
            
        else:
            return msg 
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output



@app.route('/addDriverRating', methods=['POST'])
def addDriverRating():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['userId','bookingId','ratingId']
        commonfile.writeLog("addpaymentType",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            userId = inputdata["userId"]
            bookingId=inputdata['bookingId']
            ratingId=inputdata['ratingId']
            
           
            column="userId,bookingId,ratingId"
            values="'"+str(userId)+"' ,'"+str(bookingId)+"','"+str(ratingId)+"'"
            insertdata=databasefile.InsertQuery("driverRating",column,values)
            

            output= {"result":"User Added Successfully","message":"","status":"true"}
            return output
            
        else:
            return msg 
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output



@app.route('/addFavDriver', methods=['POST'])
def addFavDriver():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['userId','driverId']
        commonfile.writeLog("addFavDriver",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            userId = inputdata["userId"]
            driverId=inputdata['driverId']
           
            
           
            column="userId,driverId"
            values="'"+str(userId)+"' ,'"+str(driverId)+"'"
            insertdata=databasefile.InsertQuery("favDriver",column,values)
            

            output= {"result":"User Added Successfully","message":"","status":"true"}
            return output
            
        else:
            return msg 
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output


#screendependency left
@app.route('/addDrivertest', methods=['POST'])
def addDrivertest():
    try:
        inputdata=request.form.get('data')
        print(inputdata,'inputdata')
        keyarr = ['mobileNo','name','userTypeId']
        inputdata=json.loads(inputdata)
        startlimit,endlimit="",""

        commonfile.writeLog("addDrivertest",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        print(msg,'msg')
       
        if msg == "1":
            mobileNo=inputdata['mobileNo']
            name=inputdata['name']
           
           
            column = " * "
            whereCondition= " mobileNo='"+str(mobileNo)+ "' and usertypeId='2' "
            data= databasefile.SelectQuery("userMaster",column,whereCondition)

            column11="id,driverId"

            whereCondition1= " mobileNo='"+str(mobileNo)+ "' "
            data1= databasefile.SelectQuery("driverMaster",column11,whereCondition1)

            print(data1,'data')

           
            mobileNo= inputdata["mobileNo"]
            driverId=data['result']['userId']
          
            if data1['status'] !='false':
                WhereCondition = " driverId = '" + str(driverId) + "'"
                column = " name='" + str(name) + "' ,dlNo = '" + str(DlNo) + "',dlFrontFilename = '" + str(dlFrontFilename) + "',dlFrontFilepath = '" + str(DlFrontPicPath) + "',dlBackFilename = '" + str(dlBackFilename) + "',dlBackFilepath = '" + str(DlBackPicPath) + "',cleanRecord='" + str(cleanRecord) + "'  ,backgroundCheck='" + str(backgroundCheck) + "',recommendiationLetter='" + str(recommendationLetter) + "',healthrecord='" + str(healthrecord) + "',misconduct='" + str(misconduct) + "',socialsecuritynumberTrace='" + str(socialsecuritynumberTrace) + "',trafficScreening ='" + str(trafficScreening) + "'"
                print(column,'column')
                data = databasefile.UpdateQuery("driverMaster",column,WhereCondition)
                print(data)
                return {"result":data,"status":"true"}

            else:

                data123={"result":"Test done","status":"false"}
                return data123
        
        else:
            return msg



    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output
            

@app.route('/driverInterview', methods=['POST'])
def driverinterview():
    try:
        inputdata=request.form.get('data')
        print(inputdata,'inputdata')
        keyarr = ['driverId']
        inputdata=json.loads(inputdata)
        startlimit,endlimit="",""

        commonfile.writeLog("driverInterview",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        print(msg,'msg')
       
        if msg == "1":
           driverId=inputdata['driverId']
           WhereCondition = " driverId = '" + str(driverId) + "'"
           column = " interviewStatus='1'"
           data = databasefile.UpdateQuery("driverMaster",column,WhereCondition)
           print(data)
           return {"result":"Updated successfully","message":"Updated Successfully","status":"true"}

        
        else:
            return msg



    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output
            


 

@app.route('/driverVerify', methods=['POST'])
def driverVerify():
    try:
        inputdata=request.form.get('data')
        print(inputdata,'inputdata')
        keyarr = ['driverId']
        inputdata=json.loads(inputdata)
        startlimit,endlimit="",""

        commonfile.writeLog("driverVerify",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        print(msg,'msg')
       
        if msg == "1":
           driverId=inputdata['driverId']
           status=inputdata['status']
           WhereCondition = " driverId = '" + str(driverId) + "'"
           column = " documentstatus='" + str(status) + "'"
           print(column,'column')
           data = databasefile.UpdateQuery("driverMaster",column,WhereCondition)
           print(data)
           return {"result":"Updated successfully","message":"Updated Successfully","status":"true"}

        
        else:
            return msg



    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output
            











@app.route('/getNearDriver', methods=['POST'])
def getNearDriver():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['startLocationLat','startLocationLong']
        commonfile.writeLog("getNearDriver",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg == "1":
            startlat ,startlng,userId= inputdata["startLocationLat"],inputdata["startLocationLong"],""#,inputdata["userId"]
            column=  "d.driverId,d.name, d.mobileNo, b.lat, b.lng,SQRT(POW(69.1 * (b.lat - "+str(startlat)+"), 2) +POW(69.1 * ("+str(startlng)+" - b.lng) * COS(b.lat / 57.3), 2)) AS distance "
            whereCondition= "and d.status=1 and b.onTrip=0 and b.onDuty=1 and b.driverId=b.driverId HAVING distance < 25 "
            orderby="  distance "
            nearByDriver=databasefile.SelectQueryOrderbyAsc("driverMaster d,driverRideStatus as b",column,whereCondition,"",orderby,"","")
            if (nearByDriver!=0):   
                        
                return nearByDriver
            else:
                nearByDriver["message"]="No Driver Found"
                return nearByDriver
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




@app.route('/bookRide', methods=['POST'])
def bookRide():
    try:
        print('A')
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        #inputdata={"ambulanceId":[1,2,3,4],"driverId":[13,14,15,16,17],'startLocationLat':28.583962,'startLocationLong':77.314345,"pickupLocationAddress":" Noida se 15",'dropLocationLat':28.535517,'dropLocationLong':77.391029,"dropLocationAddress":"fortis noida","userId":"8b0e338e522a11ea93d39ebd4d0189fc"}
        # inputdata1={}
        # inputdata1["pickupLocationAddress"]=inputdata["pickupLocationAddress"]
        # inputdata1["dropLocationAddress"]=inputdata["dropLocationAddress"]
        keyarr = ['startLocationLat','startLocationLong',"pickupLocationAddress",'dropLocationLat','dropLocationLong',"dropLocationAddress","userId"]
        client = mqtt.Client()
        client.connect("localhost",1883,60)

        for i in inputdata["driverId"]:

            #inputdata["driverId"]=str(i)
            #print(inputdata)
            
            
            topic=str(i)+"/booking"
            print(topic)
            print("1")
            #print("=================",topic)
            client.publish(topic, str(inputdata))
            print("2")
        client.disconnect()    
             
        return  {"result":"booking send","status":"True"}
    except KeyError as e:
        print("Exception---->" +str(e))        
        output = {"result":"Input Keys are not Found","status":"false"}
        return output    
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"result":"something went wrong","status":"false"}
        return output




@app.route('/acceptRide', methods=['POST'])
def acceptRide():
    try:
        print('A')
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        print(inputdata)
        startlimit,endlimit="",""
       
        print("1111")
        keyarr = ["driverId",'startLocationLat','startLocationLong',"pickupLocationAddress",'dropLocationLat','dropLocationLong',"dropLocationAddress","userId"]
        
        print("2")
        
        if "driverId" in inputdata:
                if inputdata['driverId'] != "":
                    driverId =str(inputdata["driverId"])
                    print(driverId)
        if "startLocationLat" in inputdata:
                if inputdata['startLocationLat'] != "":
                    startLocationLat =inputdata["startLocationLat"]
        if "startLocationLong" in inputdata:
                if inputdata['startLocationLong'] != "":
                    startLocationLong =inputdata["startLocationLong"]
        if "pickupLocationAddress" in inputdata:
                if inputdata['pickupLocationAddress'] != "":
                    pickupLocationAddress =str(inputdata["pickupLocationAddress"])
        
       
        if "userId" in inputdata:
            if inputdata['userId'] != "":
                userId =str(inputdata["userId"])

        bookingTypeId=inputdata['bookingTypeId']

        print("3")
        bookingId = (commonfile.CreateHashKey(driverId,userId)).hex


        commonfile.writeLog("acceptRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        
        if msg == "1":
            print('B')
            columns="mobileNo,name"
            whereCondition22="  and userId= '"+str(userId)+"' and userTypeId='2' "
            data1= databasefile.SelectQuery1("userMaster",columns,whereCondition22)
            print(data1,'data1')
            usermobile=data1['result']['mobileNo']
            userName=data1['result']['name']


            whereCondition222="  and driverId= '"+str(driverId)+"' "
            data11= databasefile.SelectQuery1("driverMaster",columns,whereCondition222)
            print(data11,'--data')
            driverName=data11['result']['name']
            drivermobile=data11['result']['mobileNo']

            if "dropLocationLat" in inputdata:
                if inputdata['dropLocationLat'] != "":
                    dropLocationLat =(inputdata["dropLocationLat"])
            
            if "dropLocationLong" in inputdata:
                if inputdata['dropLocationLong'] != "":
                    dropLocationLong =(inputdata["dropLocationLong"])
            
            if "dropLocationAddress" in inputdata:
                if inputdata['dropLocationAddress'] != "":
                    dropLocationAddress =str(inputdata["dropLocationAddress"])	
           




            #insertdata
            columnqq='userMobile,driverMobile,pickup,pickupLatitude,pickupLongitude,userId,driverId,bookingId,bookingTypeId,dropOff,dropOffLatitude,dropOffLongitude'
            values111 = " '"+ str(usermobile) +"','" + str(drivermobile)+"','" + str(pickupLocationAddress)+"','" + str(startLocationLat) +"','" + str(startLocationLong) 
            values111=values111+"','" + str(userId) +"','" + str(driverId) + "','" + str(bookingId)+ "','" + str(bookingTypeId) + "','" + str(dropLocationAddress) +"','" + str(dropLocationLong) +"','" + str(dropLocationLat) +"'" 

            data111=databasefile.InsertQuery('bookDriver',columnqq,values111)

            if bookingTypeId ==1 or bookingTypeId =='1':
                print('Daily Driver')
                finalAmount=  520 + 35

                if "pickUpTime" in inputdata:
                    if inputdata['pickUpTime'] != "":
                        pickUpTime =inputdata["pickUpTime"]
                
                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,pickUpTime,finalAmount"
                values= " '"+ str(bookingId)+"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)+"','" + str(dropLocationLong) +"','" + str(pickUpTime)+"','" + str(finalAmount)+"'"  
                insertdata=databasefile.InsertQuery('bookDaliyDriver',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookDaliyDriver  b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")







                

            if bookingTypeId ==2 or bookingTypeId =='2':
                print('Corporate')
                #disscussion pending
                
                if "startdate" in inputdata:
                    if inputdata['startdate'] != "":
                        startdate =inputdata["startdate"]
                if "enddate" in inputdata:
                    if inputdata['enddate'] != "":
                        enddate =inputdata["enddate"]

                if "dropLocationLat" in inputdata:
                    if inputdata['dropLocationLat'] != "":
                        dropLocationLat =(inputdata["dropLocationLat"])
                
                if "dropLocationLong" in inputdata:
                    if inputdata['dropLocationLong'] != "":
                        dropLocationLong =(inputdata["dropLocationLong"])
                
                if "dropLocationAddress" in inputdata:
                    if inputdata['dropLocationAddress'] != "":
                        dropLocationAddress =str(inputdata["dropLocationAddress"])

                if "morningTime" in inputdata:
                    if inputdata['morningTime'] != "":
                        morningTime =inputdata["morningTime"]
                if "eveningTime" in inputdata:
                    if inputdata['eveningTime'] != "":
                        eveningTime =inputdata["eveningTime"]

                column='bookingId,startdate,enddate,dropLocationLong,dropLocationLat,dropOff,morningTime,eveningTime'
                values=" '"+ str(bookingId) +"','" + str(startdate)+"','" + str(enddate)
                values=values+"','" + str(dropLocationLong) +"','" + str(dropLocationLat) +"','" + str(dropLocationAddress)

                values=values+"','" + str(morningTime) +"','" + str(eveningTime) +"'"
                insertdata=databasefile.InsertQuery('bookCorporateMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropLocationLat,b.dropLocationLong"
                columns=columns+",b.finalAmount,b.morningTime,b.eveningTime,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookCorporateMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")




                

                
            if bookingTypeId==3 or bookingTypeId =='3':
                print('hourly')

                if "totalHours" in inputdata:
                    if inputdata['totalHours'] != "":
                        totalHours =inputdata["totalHours"]

                



                finalAmount=  totalHours* 60 + 35

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalHours"
                values= " '"+ str(bookingId)+"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)+"','" + str(dropLocationLong) +"','" + str(finalAmount)+"','" + str(totalHours)+"'"
                insertdata=databasefile.InsertQuery('bookHourlyMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookHourlyMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")







                
            
            if bookingTypeId ==4 or bookingTypeId=='4':
                print('one')

                if "dropLocationLat" in inputdata:
                    if inputdata['dropLocationLat'] != "":
                        dropLocationLat =(inputdata["dropLocationLat"])
                if "dropLocationLong" in inputdata:
                    if inputdata['dropLocationLong'] != "":
                        dropLocationLong =(inputdata["dropLocationLong"])
                if "dropLocationAddress" in inputdata:
                    if inputdata['dropLocationAddress'] != "":
                        dropLocationAddress =str(inputdata["dropLocationAddress"])


                R = 6373.0
                print(R,'R')
                fromlongitude2= startLocationLong
                print(fromlongitude2,'fromlong',type(fromlongitude2))
                fromlatitude2 = startLocationLat
                # print(fromlongitude2,'fromlong')
                print('lat',fromlatitude2)
                distanceLongitude = dropLocationLong - fromlongitude2
                distanceLatitude = dropLocationLat - fromlatitude2
                a = sin(distanceLatitude / 2)**2 + cos(fromlatitude2) * cos(dropLocationLat) * sin(distanceLongitude / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                distance2=distance/100
                Distance=distance2*1.85
                d=round(Distance)
                d2 =str(d) +' Km'
                print(d2)


                finalAmount= d * 2.5 + 35

                print(finalAmount,'final')

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalDistance"
                values=  " '"+ str(bookingId) +"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)
                values=values+"','" + str(dropLocationLong) +"','" + str(finalAmount) +"','" + str(d2)+"'"
                insertdata=databasefile.InsertQuery('bookOneMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")



                

            if bookingTypeId ==5 or bookingTypeId=='5':
                print('Round')


                R = 6373.0
                print(R,'R')
                fromlongitude2= startLocationLong
                print(fromlongitude2,'fromlong',type(fromlongitude2))
                fromlatitude2 = startLocationLat
                # print(fromlongitude2,'fromlong')
                print('lat',fromlatitude2)
                distanceLongitude = dropLocationLong - fromlongitude2
                distanceLatitude = dropLocationLat - fromlatitude2
                a = sin(distanceLatitude / 2)**2 + cos(fromlatitude2) * cos(dropLocationLat) * sin(distanceLongitude / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                distance2=distance/100
                Distance=distance2*1.85
                d=round(Distance)
                print(d)
                d2 =str(d+d) +' Km'
                print(d2)


                
                finalAmount= (d * 2.5)*2 + 35

                print(finalAmount,'final')

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalDistance"
                values=  " '"+ str(bookingId) +"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)
                values=values+"','" + str(dropLocationLong) +"','" + str(finalAmount) +"','" + str(d2)+"'"
                insertdata=databasefile.InsertQuery('bookRoundMaster',column,values)


                
                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
                print("11111111")

            
            bookingDetails["result"]["driverName"]=driverName
            bookingDetails['result']['userName']=userName

            if (bookingDetails!='0'):  
                print('Entered')
                client = mqtt.Client()
                client.connect("localhost",1883,60)
                topic=str(userId)+"/booking"
                client.publish(topic, str(bookingDetails)) 
                #bookRide["message"]="ride booked Successfully" 
                client.disconnect()
                return bookingDetails
            else:
                data={"result":"","message":"No data Found","status":"false"}
                
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




@app.route('/userBookings', methods=['POST'])
def userBookings():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        whereCondition2=""
       
        commonfile.writeLog("userBookings",inputdata,0)
        msg="1"
        if msg == "1":
            if "startLimit" in inputdata:
                if inputdata['startLimit'] != "":
                    startlimit =str(inputdata["startLimit"])
                
            if "endLimit" in inputdata:
                if inputdata['endLimit'] != "":
                    endlimit =str(inputdata["endLimit"])

                 
            if "userId" in inputdata:
                if inputdata['userId'] != "":
                    userId =str(inputdata["userId"])

            if "bookingId" in inputdata:
                if inputdata['bookingId'] != "":
                    bookingId =str(inputdata["bookingId"])
                    whereCondition2=" and bm.bookingId= '"+ str(bookingId)+"'"

            if "bookingTypeId" in inputdata:
                if inputdata['bookingTypeId'] != "":
                    bookingTypeId =str(inputdata["bookingTypeId"])
                    whereCondition2=whereCondition2+" and bm.bookingTypeId= '"+ str(bookingTypeId)+"'"


            orderby="bm.id" 
            if bookingTypeId ==1 or bookingTypeId=='1':
                print('11')

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookDaliyDriver  b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('Dd')
            if bookingTypeId ==2 or bookingTypeId=='2':
            	print('corp')
            
            if bookingTypeId==3 or bookingTypeId=='3':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('hourly')
            if bookingTypeId ==4 or bookingTypeId =='4':
            	columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
            	columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
            	columns=columns+",bm.driverMobile,b.status"
            	whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
            	bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
            	print('one')
            
            if bookingTypeId ==5 or bookingTypeId=='5':
            	print('round') 
            	columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
            	columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
            	columns=columns+",bm.driverMobile,b.status"
            	whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
            	bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                        

                    



            if (bookingDetails['status']!='false'): 
                Data = {"result":bookingDetails['result'],"status":"true","message":""}

                          
                return Data
            else:
            	Data = {"result":"","status":"true","message":"No Rides"}
            	return Data
                
                
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

@app.route('/driverTrips', methods=['POST'])
def driverTrips():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        whereCondition2=""
       
        commonfile.writeLog("driverTrips",inputdata,0)
        msg="1"
        if msg == "1":
            if "startLimit" in inputdata:
                if inputdata['startLimit'] != "":
                    startlimit =str(inputdata["startLimit"])
                
            if "endLimit" in inputdata:
                if inputdata['endLimit'] != "":
                    endlimit =str(inputdata["endLimit"])

                 
            if "userId" in inputdata:
                if inputdata['userId'] != "":
                    userId =str(inputdata["userId"])

            if "bookingId" in inputdata:
                if inputdata['bookingId'] != "":
                    bookingId =inputdata["bookingId"]
                    whereCondition2=" and bm.bookingId= '"+ str(bookingId)+"'"


            if "bookingTypeId" in inputdata:
                if inputdata['bookingTypeId'] != "":
                    bookingTypeId =inputdata["bookingTypeId"]
                    whereCondition2=whereCondition2+" and bm.bookingTypeId= '"+ str(bookingTypeId)+"'"


            orderby="bm.id" 
            
            if bookingTypeId ==1 or bookingTypeId=='1':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookDailyDriver b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('Dd')
            if bookingTypeId ==2 or bookingTypeId=='2':
            	print('corp')
                
            
            if bookingTypeId==3 or bookingTypeId=='3':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('hourly')
            if bookingTypeId ==4 or bookingTypeId =='4':
            	columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
            	columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
            	columns=columns+",bm.driverMobile,b.status"
            	whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
            	bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
            	print('one')
            
            if bookingTypeId ==5 or bookingTypeId=='5':
            	print('round') 
            	columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
            	columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
            	columns=columns+",bm.driverMobile,b.status"
            	whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId "
            	bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                        

                    



            if (data['status']!='false'): 
                Data = {"result":bookingDetails['result'],"status":"true","message":""}

                          
                return Data
            else:
            	Data = {"result":"","status":"true","message":"No Rides"}
            	return Data
                
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


@app.route('/ActiveBooking', methods=['POST'])
def ActiveBooking():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
       
        commonfile.writeLog("endRide",inputdata,0)
        msg="1"
        if msg == "1":
            if "startLimit" in inputdata:
                if inputdata['startLimit'] != "":
                    startlimit =str(inputdata["startLimit"])
                
            if "endLimit" in inputdata:
                if inputdata['endLimit'] != "":
                    endlimit =str(inputdata["endLimit"])

           

            if "bookingId" in inputdata:
                if inputdata['bookingId'] != "":
                    bookingId =str(inputdata["bookingId"])
                    whereCondition2=" and bm.bookingId= '"+ str(bookingId)+"'"

            if "bookingTypeId" in inputdata:
                if inputdata['bookingTypeId'] != "":
                    bookingTypeId =str(inputdata["bookingTypeId"])
                    whereCondition2=whereCondition2+" and bm.bookingTypeId= '"+ str(bookingTypeId)+"'"


            orderby="bm.id" 
            if bookingTypeId ==1 or bookingTypeId=='1':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId  and b.status='2' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('Dd')
            if bookingTypeId ==2 or bookingTypeId=='2':
                print('corp')
            
            if bookingTypeId==3 or bookingTypeId=='3':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='2' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('hourly')
            if bookingTypeId ==4 or bookingTypeId =='4':
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='2' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('one')
            
            if bookingTypeId ==5 or bookingTypeId=='5':
                print('round') 
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='2' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                        

           
            if (data['status']!='false'): 
                Data = {"result":bookingDetails['result'],"status":"true","message":""}

                          
                return Data
            else:
                
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

@app.route('/acceptBooking', methods=['POST'])
def acceptBooking():
    try:
        print('A')
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        print(inputdata)
        startlimit,endlimit="",""
       
        print("1111")
        keyarr = ["driverId",'startLocationLat','startLocationLong',"pickupLocationAddress",'dropLocationLat','dropLocationLong',"dropLocationAddress","userId"]
        
        print("2")
        
        if "driverId" in inputdata:
                if inputdata['driverId'] != "":
                    driverId =str(inputdata["driverId"])
                    print(driverId)
        if "startLocationLat" in inputdata:
                if inputdata['startLocationLat'] != "":
                    startLocationLat =inputdata["startLocationLat"]
        if "startLocationLong" in inputdata:
                if inputdata['startLocationLong'] != "":
                    startLocationLong =inputdata["startLocationLong"]
        if "pickupLocationAddress" in inputdata:
                if inputdata['pickupLocationAddress'] != "":
                    pickupLocationAddress =str(inputdata["pickupLocationAddress"])
        
       
        if "userId" in inputdata:
            if inputdata['userId'] != "":
                userId =str(inputdata["userId"])

        bookingTypeId=inputdata['bookingTypeId']

        print("3")
        bookingId = (commonfile.CreateHashKey(driverId,userId)).hex


        commonfile.writeLog("acceptRide",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        
        if msg == "1":
            print('B')
            columns="mobileNo,name"
            whereCondition22="  and userId= '"+str(userId)+"' and userTypeId='2' "
            data1= databasefile.SelectQuery1("userMaster",columns,whereCondition22)
            print(data1,'data1')
            usermobile=data1['result']['mobileNo']
            userName=data1['result']['name']


            whereCondition222="  and driverId= '"+str(driverId)+"' "
            data11= databasefile.SelectQuery1("driverMaster",columns,whereCondition222)
            print(data11,'--data')
            driverName=data11['result']['name']
            drivermobile=data11['result']['mobileNo']

            if "dropLocationLat" in inputdata:
                if inputdata['dropLocationLat'] != "":
                    dropLocationLat =(inputdata["dropLocationLat"])
            
            if "dropLocationLong" in inputdata:
                if inputdata['dropLocationLong'] != "":
                    dropLocationLong =(inputdata["dropLocationLong"])
            
            if "dropLocationAddress" in inputdata:
                if inputdata['dropLocationAddress'] != "":
                    dropLocationAddress =str(inputdata["dropLocationAddress"])	
           




            #insertdata
            columnqq='userMobile,driverMobile,pickup,pickupLatitude,pickupLongitude,userId,driverId,bookingId,bookingTypeId,dropOff,dropOffLatitude,dropOffLongitude'
            values111 = " '"+ str(usermobile) +"','" + str(drivermobile)+"','" + str(pickupLocationAddress)+"','" + str(startLocationLat) +"','" + str(startLocationLong) 
            values111=values111+"','" + str(userId) +"','" + str(driverId) + "','" + str(bookingId)+ "','" + str(bookingTypeId) + "','" + str(dropLocationAddress) +"','" + str(dropLocationLong) +"','" + str(dropLocationLat) +"'" 

            data111=databasefile.InsertQuery('bookDriver',columnqq,values111)

            if bookingTypeId ==1 or bookingTypeId =='1':
                print('Daily Driver')
                finalAmount=  520 + 35

                if "pickUpTime" in inputdata:
                    if inputdata['pickUpTime'] != "":
                        pickUpTime =inputdata["pickUpTime"]
                
                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,pickUpTime,finalAmount"
                values= " '"+ str(bookingId)+"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)+"','" + str(dropLocationLong) +"','" + str(pickUpTime)+"','" + str(finalAmount)+"'"  
                insertdata=databasefile.InsertQuery('bookDaliyDriver',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookDaliyDriver  b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")







                

            if bookingTypeId ==2 or bookingTypeId =='2':
                print('Corporate')
                #disscussion pending
                
                if "startdate" in inputdata:
                    if inputdata['startdate'] != "":
                        startdate =inputdata["startdate"]
                if "enddate" in inputdata:
                    if inputdata['enddate'] != "":
                        enddate =inputdata["enddate"]

                if "dropLocationLat" in inputdata:
                    if inputdata['dropLocationLat'] != "":
                        dropLocationLat =(inputdata["dropLocationLat"])
                
                if "dropLocationLong" in inputdata:
                    if inputdata['dropLocationLong'] != "":
                        dropLocationLong =(inputdata["dropLocationLong"])
                
                if "dropLocationAddress" in inputdata:
                    if inputdata['dropLocationAddress'] != "":
                        dropLocationAddress =str(inputdata["dropLocationAddress"])

                if "morningTime" in inputdata:
                    if inputdata['morningTime'] != "":
                        morningTime =inputdata["morningTime"]
                if "eveningTime" in inputdata:
                    if inputdata['eveningTime'] != "":
                        eveningTime =inputdata["eveningTime"]

                column='bookingId,startdate,enddate,dropLocationLong,dropLocationLat,dropOff,morningTime,eveningTime'
                values=" '"+ str(bookingId) +"','" + str(startdate)+"','" + str(enddate)
                values=values+"','" + str(dropLocationLong) +"','" + str(dropLocationLat) +"','" + str(dropLocationAddress)

                values=values+"','" + str(morningTime) +"','" + str(eveningTime) +"'"
                insertdata=databasefile.InsertQuery('bookCorporateMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropLocationLat,b.dropLocationLong"
                columns=columns+",b.finalAmount,b.morningTime,b.eveningTime,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.userMobile"
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookCorporateMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")




                

                
            if bookingTypeId==3 or bookingTypeId =='3':
                print('hourly')

                if "totalHours" in inputdata:
                    if inputdata['totalHours'] != "":
                        totalHours =inputdata["totalHours"]

                



                finalAmount=  totalHours* 60 + 35

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalHours"
                values= " '"+ str(bookingId)+"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)+"','" + str(dropLocationLong) +"','" + str(finalAmount)+"','" + str(totalHours)+"'"
                insertdata=databasefile.InsertQuery('bookHourlyMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22=" and  dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookHourlyMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")







                
            
            if bookingTypeId ==4 or bookingTypeId=='4':
                print('one')

                if "dropLocationLat" in inputdata:
                    if inputdata['dropLocationLat'] != "":
                        dropLocationLat =(inputdata["dropLocationLat"])
                if "dropLocationLong" in inputdata:
                    if inputdata['dropLocationLong'] != "":
                        dropLocationLong =(inputdata["dropLocationLong"])
                if "dropLocationAddress" in inputdata:
                    if inputdata['dropLocationAddress'] != "":
                        dropLocationAddress =str(inputdata["dropLocationAddress"])


                R = 6373.0
                print(R,'R')
                fromlongitude2= startLocationLong
                print(fromlongitude2,'fromlong',type(fromlongitude2))
                fromlatitude2 = startLocationLat
                # print(fromlongitude2,'fromlong')
                print('lat',fromlatitude2)
                distanceLongitude = dropLocationLong - fromlongitude2
                distanceLatitude = dropLocationLat - fromlatitude2
                a = sin(distanceLatitude / 2)**2 + cos(fromlatitude2) *  cos(dropLocationLat) * sin(distanceLongitude / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                distance2=distance/100
                Distance=distance2*1.85
                d=round(Distance)
                d2 =str(d) +' Km'
                print(d2)


                finalAmount= d * 2.5 + 35

                print(finalAmount,'final')

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalDistance"
                values=  " '"+ str(bookingId) +"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)
                values=values+"','" + str(dropLocationLong) +"','" + str(finalAmount) +"','" + str(d2)+"'"
                insertdata=databasefile.InsertQuery('bookOneMaster',column,values)

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")



                

            if bookingTypeId ==5 or bookingTypeId=='5':
                print('Round')


                R = 6373.0
                print(R,'R')
                fromlongitude2= startLocationLong
                print(fromlongitude2,'fromlong',type(fromlongitude2))
                fromlatitude2 = startLocationLat
                # print(fromlongitude2,'fromlong')
                print('lat',fromlatitude2)
                distanceLongitude = dropLocationLong - fromlongitude2
                distanceLatitude = dropLocationLat - fromlatitude2
                #a = sin(distanceLatitude / 2)**2 + cos(fromlatitude2)  cos(dropLocationLat)  sin(distanceLongitude / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                distance2=distance/100
                Distance=distance2*1.85
                d=round(Distance)
                print(d)
                d2 =str(d+d) +' Km'
                print(d2)


                
                finalAmount= (d * 2.5)*2 + 35

                print(finalAmount,'final')

                column="bookingId,dropOff,dropOffLatitude,dropOffLongitude,finalAmount,totalDistance"
                values=  " '"+ str(bookingId) +"','" + str(dropLocationAddress)+"','" + str(dropLocationLat)
                values=values+"','" + str(dropLocationLong) +"','" + str(finalAmount) +"','" + str(d2)+"'"
                insertdata=databasefile.InsertQuery('bookRoundMaster',column,values)


                
                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile"
                whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and bm.bookingId= '"+str(bookingId)+"'"
                bookingDetails= databasefile.SelectQuery1("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22)
                print(bookingDetails,"================")
                print("11111111")

            
            bookingDetails["result"]["driverName"]=driverName
            bookingDetails['result']['userName']=userName

            if (bookingDetails!='0'):  
                print('Entered')
                client = mqtt.Client()
                client.connect("localhost",1883,60)
                topic=str(userId)+"/booking"
                client.publish(topic, str(bookingDetails)) 
                #bookRide["message"]="ride booked Successfully" 
                client.disconnect()
                return bookingDetails
            else:
                data={"result":"","message":"No data Found","status":"false"}
                
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


@app.route('/cancelledBooking', methods=['POST'])
def cancelledBooking():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
       
        commonfile.writeLog("endRide",inputdata,0)
        msg="1"
        if msg == "1":
            if "startLimit" in inputdata:
                if inputdata['startLimit'] != "":
                    startlimit =str(inputdata["startLimit"])
                
            if "endLimit" in inputdata:
                if inputdata['endLimit'] != "":
                    endlimit =str(inputdata["endLimit"])

            if "bookingId" in inputdata:
                if inputdata['bookingId'] != "":
                    bookingId =str(inputdata["bookingId"])
                    whereCondition2=" and bm.bookingId= '"+ str(bookingId)+"'"

            if "bookingTypeId" in inputdata:
                if inputdata['bookingTypeId'] != "":
                    bookingTypeId =str(inputdata["bookingTypeId"])
                    whereCondition2=whereCondition2+" and bm.bookingTypeId= '"+ str(bookingTypeId)+"'"


            orderby="bm.id" 
            if bookingTypeId ==1 or bookingTypeId=='1':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId  and b.status='4' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('Dd')
            if bookingTypeId ==2 or bookingTypeId=='2':
                print('corp')
            
            if bookingTypeId==3 or bookingTypeId=='3':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='4' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('hourly')
            if bookingTypeId ==4 or bookingTypeId =='4':
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='4' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('one')
            
            if bookingTypeId ==5 or bookingTypeId=='5':
                print('round') 
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='4' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                        

           
            if (data['status']!='false'): 
                Data = {"result":bookingDetails['result'],"status":"true","message":""}
                          
                return Data
            else:
                
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

@app.route('/CompletedBooking', methods=['POST'])
def CompletedBooking():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
       
        commonfile.writeLog("endRide",inputdata,0)
        msg="1"
        if msg == "1":
            if "startLimit" in inputdata:
                if inputdata['startLimit'] != "":
                    startlimit =str(inputdata["startLimit"])
                
            if "endLimit" in inputdata:
                if inputdata['endLimit'] != "":
                    endlimit =str(inputdata["endLimit"])

            if "bookingId" in inputdata:
                if inputdata['bookingId'] != "":
                    bookingId =str(inputdata["bookingId"])
                    whereCondition2=" and bm.bookingId= '"+ str(bookingId)+"'"

            if "bookingTypeId" in inputdata:
                if inputdata['bookingTypeId'] != "":
                    bookingTypeId =str(inputdata["bookingTypeId"])
                    whereCondition2=whereCondition2+" and bm.bookingTypeId= '"+ str(bookingTypeId)+"'"


            orderby="bm.id" 
            if bookingTypeId ==1 or bookingTypeId=='1':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile"
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId  and b.status='3' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookDailyDriver b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('Dd')

            if bookingTypeId ==2 or bookingTypeId=='2':
                print('corp')
            
            if bookingTypeId==3 or bookingTypeId=='3':

                columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='3' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus ar",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('hourly')
            if bookingTypeId ==4 or bookingTypeId =='4':
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='3' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                print('one')
            
            if bookingTypeId ==5 or bookingTypeId=='5':
                print('round') 
                columns="(dr.lat)driverLat,(dr.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
                columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
                columns=columns+",bm.driverMobile,b.status"
                whereCondition22=" dr.driverId=bm.driverId and bm.bookingId=b.bookingId and b.status='3' "
                bookingDetails= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                        


           
            if (data['status']!='false'): 
                Data = {"result":bookingDetails['result'],"status":"true","message":""}
                          
                return Data
            else:
                
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


@app.route('/userProfile1', methods=['POST'])
def userProfile1():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['userId']
        commonfile.writeLog("driverProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
        

            
            
            if 'userId' in inputdata:
                driverId=inputdata["userId"]    
                
            
            whereCondition= " userId= '"+str(driverId)+"' and userTypeId='2' "
            column='userId,name,mobileNo,password,email,profilePic'

            
         
            data11=databasefile.SelectQuery('userMaster',column,whereCondition)
         

            if data11['status'] != "false":
                if data11["result"]["profilePic"]==None:
                    data11["result"]["profilePic"]=str(ConstantData.GetBaseURL())+"/profilePic/profilePic.jpg"
                else:
                    data11["result"]["profilePic"]=str(ConstantData.GetBaseURL())+str(data11["result"]["profilePic"])
                
                Data = {"status":"true","message":"data Updated Successfully","result":data11['result']}                  
                return Data
            else:
                data={"status":"false","result":"","message":"Invalid userID"}
                return data
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output             

@app.route('/updateUserProfile1', methods=['POST'])
def updateDriverProfile11():
    try:
        inputdata = request.form.get('data') 
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata)
        startlimit,endlimit="",""
        keyarr = ["name","email","password",'userId']
        commonfile.writeLog("updateUserProfile1",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            name,email,password,userTypeId,mobileNo,gender="","","","","",""
            filename,PicPath="",""
            column,values="",""
            columns2,values2="",""
        

            
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
                

            if 'userId' in inputdata:
                userId=inputdata["userId"] 


            if 'postImage' in request.files:  
                print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                file = request.files.get('postImage')        
                filename = file.filename or ''  
                print(filename)               
                filename= str(userId)+".png"
                #filename = filename.replace("'","") 

                #folder path to save campaign image
                FolderPath = ConstantData.GetProfilePicPath(filename)  

                filepath = '/profilePic/' + filename    
                print(filepath,"filepath================")
                print(FolderPath,"FolderPathFolderPathFolderPathFolderPath")
                file.save(FolderPath)
                PicPath = filepath 
                column= column +" ,profilePic= '" + str(PicPath) + "' "       
                
            
            
            whereCondition2= " userId ='"+str(userId)+"' "
          
            
            data11=databasefile.UpdateQuery('userMaster',column,whereCondition2)
         

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


@app.route('/driverProfile1', methods=['POST'])
def DriverProfile1122():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""
        keyarr = ['userId']
        commonfile.writeLog("driverProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            
        

            
            
            if 'userId' in inputdata:
                driverId=inputdata["userId"]    
                
            
            whereCondition= " userId= '"+str(driverId)+"' and userTypeId='3' "
            column='userId,name,mobileNo,password,email,profilePic'

            
         
            data11=databasefile.SelectQuery('userMaster',column,whereCondition)
         

            if data11['status'] != "false":
                if data11["result"]["profilePic"]==None:
                    data11["result"]["profilePic"]=str(ConstantData.GetBaseURL())+"/profilePic/profilePic.jpg"
                else:
                    data11["result"]["profilePic"]=str(ConstantData.GetBaseURL())+str(data11["result"]["profilePic"])
                
                Data = {"status":"true","message":"data Updated Successfully","result":data11['result']}                  
                return Data
            else:
                data={"status":"false","result":"","message":"Invalid userID"}
                return data
                        
        else:
            return msg 
    except Exception as e :
        print("Exception---->" +str(e))           
        output = {"status":"false","message":"something went wrong","result":""}
        return output             

@app.route('/updateDriverProfile1', methods=['POST'])
def updateDriverProfile212():
    try:
        inputdata = request.form.get('data') 
        print("===========================",inputdata)      
        inputdata = json.loads(inputdata)
        startlimit,endlimit="",""
        keyarr = ["name","email","password",'userId']
        commonfile.writeLog("updateDriverProfile",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
       
        if msg == "1":
            name,email,password,userTypeId,mobileNo,gender="","","","","",""
            filename,PicPath="",""
            column,values="",""
            columns2,values2="",""
        

            
            if 'email' in inputdata:
                email=inputdata["email"]
                column=" email='"+str(email)+"' " 
            if 'name' in inputdata:
                name=inputdata["name"]
                column=column+" ,name='"+str(name)+"' "  
                column2= " name='"+str(name)+"' " 
            if 'password' in inputdata:
                password=inputdata["password"]       
                column=column+" ,password= '"+str(password)+"' "                
            if 'mobileNo' in inputdata:
                mobileNo=inputdata["mobileNo"]
                column=column+" ,mobileNo='"+str(mobileNo)+"' "
                column2=column2+" ,mobileNo='"+str(mobileNo)+"' "  

            if 'userId' in inputdata:
                driverId=inputdata["userId"] 


            if 'postImage' in request.files:  
                print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                file = request.files.get('postImage')        
                filename = file.filename or ''  
                print(filename)               
                filename= str(driverId)+".png"
                #filename = filename.replace("'","") 

                #folder path to save campaign image
                FolderPath = ConstantData.GetProfilePicPath(filename)  

                filepath = '/profilePic/' + filename    
                print(filepath,"filepath================")
                print(FolderPath,"FolderPathFolderPathFolderPathFolderPath")
                file.save(FolderPath)
                PicPath = filepath 
                column= column +" ,profilePic= '" + str(PicPath) + "' "       
                
            
            whereCondition= " driverId= '"+str(driverId)+"' "
            whereCondition2= " userId ='"+str(driverId)+"' "
          
            data=databasefile.UpdateQuery("driverMaster",column2,whereCondition)
            data11=databasefile.UpdateQuery('userMaster',column,whereCondition2)
         

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




@app.route('/myFavDrivers', methods=['POST'])
def myFavDrivers():
    try:
        inputdata =  commonfile.DecodeInputdata(request.get_data())
        startlimit,endlimit="",""
        keyarr = ['userId']
        commonfile.writeLog("myFavDriver",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            userId = inputdata["userId"]
        
           
            
           
            column="dr.driverId,us.profilePic,us.userName,us.mobileNo"
            whereCondition=" fv.userId='"+str(userId)+"' and fv.driverId=dr.driverId and dr.driverId-us.userId"
            data=databasefile.SelectQuery4("favDriver as fv,driverMaster as dr,userMaster as us",column,whereCondition)
            if data['status'] !='false':
                output= {"result":data['result'],"message":"","status":"true"}
                return output
            else:
                output= {"result":"","message":"No Fav Drivers Till Now","status":"false"}
                return output
            
        else:
            return msg 
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output  




@app.route('/addDriverDocs', methods=['POST'])
def addDriverDocs():
    try:
        print('Hello')
        print('Hello')
        inputdata=request.form.get('data')
        print(inputdata,'inputdata')
        keyarr = ['mobileNo','key','name','userTypeId']
        inputdata=json.loads(inputdata)
        # inputdata =  commonfile.DecodeInputdata(request.get_data()) 
        startlimit,endlimit="",""

        commonfile.writeLog("addDrivertest",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        print(msg,'msg')
       
        if msg == "1":
            mobileNo=inputdata['mobileNo']
            key = inputdata["key"]
            column = " * "
            whereCondition= " mobileNo='"+str(mobileNo)+ "' and usertypeId='3' "
            data= databasefile.SelectQuery4("userMaster",column,whereCondition)
            name=data['result'][0]['name']

            column11="id,driverId"

            whereCondition1= " mobileNo='"+str(mobileNo)+ "' and driverTypeId='"+str(driverTypeId)+ "'"
            data1= databasefile.SelectQuery4("driverMaster",column11,whereCondition1)

            print(data1,'data--------------------------')

           
            mobileNo= inputdata["mobileNo"]
            driverId=data['result'][0]['userId']
            
            DlNo,dlFrontFilename,DlFrontPicPath,dlBackFilename,DlBackPicPath,PIDType,PIDNo,PIDFrontFilename,PIDFrontPicPath,PIDBackFilename,PIDBackPicPath,TransportType,TransportModel,Color,AmbulanceRegistrationFuel,TypeNo,AIFilename,AIPicPath,AmbulanceModeId,AmbulanceId="","","","","","","","","","","","","","","","","","","0","0"

            if 'DlNo' in inputdata:
                DlNo=inputdata["DlNo"]

            if 'DlFrontImage' in request.files:
                    print("immmmmmmmmmmmmmmmm")
                    file = request.files.get('DlFrontImage')        
                    filename = file.filename or ''  
                    print(filename)               
                    dlFrontFilename= str(str(data['result']["userId"])+"Front"+".png")
                    
                    print(dlFrontFilename,'Changed_filename')
                    DlFrontFolderPath = ConstantData.GetdlImagePath(dlFrontFilename)
                    DlFrontfilepath = '/DLImage/' + dlFrontFilename 
                    file.save(DlFrontFolderPath)
                    DlFrontPicPath = DlFrontfilepath
                    print(DlFrontPicPath)
                    

            if 'DlBackImage' in request.files:
                    print("immmmmmmmmmmmmmmmm")
                    file = request.files.get('DlBackImage')        
                    filename = file.filename or ''  
                    print(filename)               
                    dlBackFilename=  str(str(data['result']["userId"])+"Back"+".png")
                  
                    DlBackFolderPath = ConstantData.GetdlImagePath(dlBackFilename)
                    DlBackfilepath = '/DLImage/' + dlBackFilename 
                    file.save(DlBackFolderPath)
                    DlBackPicPath = DlBackfilepath
                    print(DlBackPicPath)

            if 'PIDType' in inputdata:
                PIDType=inputdata["PIDType"]

            if 'PIDNo' in inputdata:
                PIDNo=inputdata["PIDNo"]

            if 'PIDFrontImage' in request.files:
                    print("immmmmmmmmmmmmmmmm")
                    file = request.files.get('PIDFrontImage')        
                    filename = file.filename or ''  
                    print(filename)               
                    PIDFrontFilename= str(str(data['result']["userId"])+"Front"+".png")
                  
                    print(PIDFrontFilename,'Changed_filename')
                    PIDFrontFolderPath = ConstantData.GetPIDImagePath(PIDFrontFilename)
                    PIDFrontfilepath = '/PIDImage/' + PIDFrontFilename 
                    file.save(PIDFrontFolderPath)
                    PIDFrontPicPath = PIDFrontfilepath
                    print(PIDFrontPicPath)
                    

            if 'PIDBackImage' in request.files:
                    print("immmmmmmmmmmmmmmmm")
                    file = request.files.get('PIDBackImage')        
                    filename = file.filename or ''  
                    print(filename)               
                    PIDBackFilename= str(str(data['result']["userId"])+"Back"+".png")
                  
                    PIDBackFolderPath = ConstantData.GetPIDImagePath(PIDBackFilename)
                    PIDBackfilepath = '/PIDImage/' + PIDBackFilename 
                    file.save(PIDBackFolderPath)
                    PIDBackPicPath = PIDBackfilepath
                    print(PIDBackPicPath)



            if 'DOB' in inputdata:
                DOB=inputdata["DOB"]

            if 'AmbulanceNo' in inputdata:
                AmbulanceNo=inputdata["AmbulanceNo"]

            if 'AmbulanceTypeId' in inputdata:
                AmbulanceId=inputdata["AmbulanceTypeId"]

            if 'lat' in inputdata:
                lat=inputdata["lat"]

            if 'lng' in inputdata:
                lng=inputdata["lng"]


            if 'HealthReport' in request.files:
                    print("immmmmmmmmmmmmmmmm")
                    file = request.files.get('HealthReport')        
                    filename = file.filename or ''  
                    print(filename)               
                    AIFilename=  str(str(data['result']["userId"])+".png")
                   
                    AIFolderPath = ConstantData.GetAmbulanceImagePath(AIFilename)
                    AIfilepath = '/HealthReport/' + AIFilename 
                    file.save(AIFolderPath)
                    AIPicPath = AIfilepath
                    print(AIPicPath)

            if data['status']!='false':
                
                if data1['status'] == 'false':
                    print('11')
                    if key == 1:
                        columns = "name,mobileNo,dlNo,dlFrontFilename,dlFrontFilepath,dlBackFilename,dlBackFilepath,driverId"          
                        values = " '" + str(name)+ "','"+str(mobileNo)  + "','" + str(DlNo) + "','" + str( dlFrontFilename) + "','" + str(DlFrontPicPath) + "','" + str(dlBackFilename) + "', "            
                        values = values + " '" + str(DlBackPicPath) + "','" + str(driverId) + "'"
                        data = databasefile.InsertQuery("driverMaster",columns,values)
                        data = databasefile.InsertQuery("driverMaster",columns,values)
                        if data != "0":
                            column = '*'
                            WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"

                            
                            data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)
                            print(data11,"+++++++++++++++++++")
                            y={'documentStatus':"false"}
                            data11.update(y)
                                   
                            return data11

                    if (key == 2) or (key =='2'):
                        
                        columns = " name,mobileNo,pIDType,pIDNo,pIDFrontFilename,pIDFrontFilepath,pIDBackFilename,pIDBackFilepath,driverId,DOB"          
                        values = " '" + str(name) + "','" + str(mobileNo) + "','" + str(PIDType) + "','" + str(PIDNo) + "','" + str(PIDFrontFilename) + "','" + str(PIDFrontPicPath) + "','" + str(PIDBackFilename) + "', "            
                        values = values + " '" + str(PIDBackPicPath)+ "','" + str(driverId) + "','" + str(DOB) + "'"
                        data = databasefile.InsertQuery("driverMaster",columns,values)
                        if data != "0":
                            column = '*'
                            WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"
                            
                            data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)
                            y={'documentStatus':"false"}
                            data11.update(y)
                                   
                            return data11
                    
                    if (key == 3) or (key =='3'):

                        columns = " name,mobileNo,driverId,driverTypeId"          
                        values = " '" + str(name) + "','" + str(mobileNo) + "','" + str(driverId) + "','" + str(driverTypeId) + "'"
                        
                        data = databasefile.InsertQuery("driverMaster",columns,values)

                        columns222="driverId"
                        whereCondition2222=" mobileNo = '" + str(mobileNo) +  "' "
                        data99=databasefile.SelectQuery1('driverMaster',columns222,whereCondition2222)
                        data111=data99[-1]
                        driverid=data111["driverId"]

                        # columns2= "ambulanceNo,transportType,transportModel,color,ambulanceRegistrationFuel,typeNo,ambulanceFilename,ambulanceFilepath,ambulanceModeId,ambulanceTypeId,driverId,driverTypeId"
                        # values2="'" + str(AmbulanceNo) + "','" + str( TransportType)  + "','" + str(TransportModel) + "','" + str(Color) + "','" + str(AmbulanceRegistrationFuel) + "','" + str(TypeNo) + "','" + str(AIFilename) + "','" + str(AIPicPath) + "','" + str(AmbulanceModeId) + "', "            
                        # values2 = values2 + " '" + str(AmbulanceId) + "','" + str(driverid) + "','" + str(driverTypeId) + "'"
                        # data122=databasefile.InsertQuery("ambulanceMaster",columns2,values2)
                        data122="1"
                        
                        

                        if data122 != "0":

                            column = '*'
                            WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"
                            whereCondition="   driverId='" + str(driverid) +  "' "
                            columns22="ambulanceId,transportType,transportModel,color,ambulanceRegistrationFuel,typeNo,ambulanceFilename,ambulanceFilepath,ambulanceModeId,ambulanceTypeId,ambulanceNo,driverTypeId"
                            
                            data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)
                            print(data11['result'],"______--")
                            print(data11['result']['dlNo'],"+++++++++")


                            data12=databasefile.SelectQuery("ambulanceMaster",columns22,whereCondition)

                            ambulanceId=data12['result']['ambulanceId']
                            columns23='ambulanceId,lat,lng'
                            values23 = " '" + str(ambulanceId) + "','" + str(lat) + "','" + str(lng) + "'"
                            data122=databasefile.InsertQuery('ambulanceRideStatus',columns23,values23)
                            whereCondition222= " ambulanceId=  '" + str(ambulanceId) +  "' "
                            columns239="lat,lng,onDuty,onTrip"
                            data12333=databasefile.SelectQuery1('ambulanceRideStatus',columns239,whereCondition222)



                            y={'documentStatus':"false"}
                            data11.update(y)

                                


                            return data11
                
                
                else:
                    if (key == 1) or (key =='1'):
                        print('A')
                        columns="dlNo"
                        WhereCondition = " mobileNo = '" + str(mobileNo) + "'"
                        data19 = databasefile.SelectQuery1("driverMaster",columns,WhereCondition)
                        if data19['result']['dlNo'] == None:

                            column = " name='" + str(name) + "' ,dlNo = '" + str(DlNo) + "',dlFrontFilename = '" + str(dlFrontFilename) + "',dlFrontFilepath = '" + str(DlFrontPicPath) + "',dlBackFilename = '" + str(dlBackFilename) + "',dlBackFilepath = '" + str(DlBackPicPath) + "'"
                            print(column,'column')
                            data = databasefile.UpdateQuery("driverMaster",column,WhereCondition)
                            print(data,'updatedata')
                            column = '*'
                            WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"

                            
                            data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)
                            if data11['result']['pIDType'] == None:
                               
                                    y={'documentStatus':"false"}
                                    data11.update(y)
                                
                            else:
                                columns='ambulanceNo'
                                whereCondition=" driverId='"+str(driverId)+"'"
                                data1111=databasefile.SelectQuery1('ambulanceMaster',columns,whereCondition)
                                if data1111['status']=='false':
                                    y={'documentStatus':"false"}
                                    data11.update(y)
                                else:
                                    y={'documentStatus':"true"}
                                    data11.update(y)

                            return data11
                        else:
                            data={"result":"","message":"Already Uploaded","status":"false"}
                            return data

                    if (key == 2) or (key =='2'):
                        print('B')
                        columns='pIDType,pIDNo'
                        WhereCondition = " mobileNo = '" + str(mobileNo) + "'"
                        data19 = databasefile.SelectQuery1("driverMaster",columns,WhereCondition)
                        if data19['result']['pIDType'] == None:
                            column = "name='" + str(name) + "', pIDType = '" + str(PIDType) + "',pIDNo = '" + str(PIDNo) + "',pIDFrontFilename = '" + str(PIDFrontFilename) + "',pIDFrontFilepath = '" + str(PIDFrontPicPath) + "',pIDBackFilename = '" + str(PIDBackFilename) + "',pIDBackFilepath = '" + str(PIDBackPicPath) + "',DOB='" + str(DOB) + "'"
                            print(column,'column')
                            data = databasefile.UpdateQuery("driverMaster",column,WhereCondition)
                            print(data,'updatedata')
                            column = '*'
                            WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"
                            
                            data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)
                            if data11['result']['dlNo'] == None:
                                y={'documentStatus':"false"}
                                data11.update(y)

                            else:
                                columns='ambulanceNo'
                                whereCondition=" driverId= '"+str(driverId)+"'"
                                data1111=databasefile.SelectQuery1('ambulanceMaster',columns,whereCondition)
                                if data1111['status']=='false':
                                    y={'documentStatus':"false"}
                                    data11.update(y)
                                else:
                                    y={'documentStatus':"true"}
                                    data11.update(y)

                            
                            return data11
                        
                        else:
                            data={"result":"","message":"Already Uploaded","status":"false"}
                            return data



                    if (key == 3) or (key =='3'):
                        driver_Id=data1['result']['driverId']
                        columns="ambulanceId"
                        WhereCondition = " driverId = '" + str(driver_Id) + "'"
                        data111=databasefile.SelectQuery1('ambulanceMaster',columns,WhereCondition)
                        if data111['status'] == 'false':
                            
                            columns2= "ambulanceNo,transportType,transportModel,color,ambulanceRegistrationFuel,typeNo,ambulanceFilename,ambulanceFilepath,ambulanceModeId,ambulanceTypeId,driverId,driverTypeId"

                            values2="'" + str(AmbulanceNo) + "','" + str( TransportType) + "','" + str(TransportModel) + "','" + str(Color) + "','" + str(AmbulanceRegistrationFuel) + "','" + str(TypeNo) + "','" + str(AIFilename) + "','" + str(AIPicPath) + "','" + str(AmbulanceModeId) + "', "            
                            values2 = values2 + " '" + str(AmbulanceId) + "','" + str(driver_Id) + "','" + str(driverTypeId) + "'"
                            data122=databasefile.InsertQuery("ambulanceMaster",columns2,values2)
                            print(data122,'+++++++++++++++++++')
                            
                            

                            if data122 != "0":
                                column = '*'
                                WhereCondition = " mobileNo = '" + str(mobileNo) +  "'"
                                whereCondition="   driverId='" + str(driver_Id) +  "' "
                                columns22="ambulanceId,transportType,transportModel,color,ambulanceRegistrationFuel,typeNo,ambulanceFilename,ambulanceFilepath,ambulanceModeId,ambulanceTypeId,ambulanceNo"
                                
                                data11 = databasefile.SelectQuery1("driverMaster",column,WhereCondition)


                                data12=databasefile.SelectQuery1("ambulanceMaster",columns22,whereCondition)

                                ambulanceId=data12['result']['ambulanceId']
                                columns23='ambulanceId,lat,lng'
                                values23 = " '" + str(ambulanceId) + "','" + str(lat) + "','" + str(lng) + "'"
                                data122=databasefile.InsertQuery('ambulanceRideStatus',columns23,values23)
                                whereCondition222= " ambulanceId=  '" + str(ambulanceId) +  "' "
                                columns239="lat,lng,onDuty,onTrip"
                                data12333=databasefile.SelectQuery1('ambulanceRideStatus',columns239,whereCondition222)



                                data11['result'].update(data12['result'])
                                data11['result'].update(data12333['result'])
                                
                                if data11['result']['dlNo'] == None:
                                    y={'documentStatus':"false"}
                                    data11.update(y)
                                   

                                
                                if data11['result']['pIDNo'] == None:
                                    y={'documentStatus':"false"}
                                    data11.update(y)
                                
                                if (data11['result']['dlNo'] != None) and (data11['result']['pIDNo'] != None) :
                                    y={'documentStatus':"true"}
                                    data11.update(y)

                                        


                                return data11

                            print('q')
                        else:
                            data11={"result":"","message":"Already Uploaded","status":"false"}
                            return data11

            else:
                data={"result":"","message":"Invalid mobileNo","status":"false"}
                return data
                        
               
        else:
            return msg
    except Exception as e :
        print("Exception---->" + str(e))    
        output = {"result":"something went wrong","status":"false"}
        return output



if __name__ == "__main__":
    CORS(app, support_credentials=True)
    app.run(host='0.0.0.0',port=5034,debug=True)













