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
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
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
                    
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition,"",startlimit,endlimit)
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
            whereCondition= "  otp='" + otp+ "' and mobileNo='" + mobileNo+"'"
            verifyOtp=databasefile.SelectQuery1(" userMaster ",column,whereCondition)
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
                
            
            whereCondition= " userId= '"+str(userId)+"' and userTypeId='2' "
            column='userId,name,mobileNo,password,email'

            
         
            data11=databasefile.SelectQuery('userMaster',column,whereCondition)
         

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
            column=  "us.mobileNo,us.name,us.userId,um.name as userName"
            whereCondition= "us.mobileNo = '" + str(mobileNo) + "' and us.password = '" + password + "' and us.userTypeId=um.id"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):   
                              
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


                                
                return loginuser
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
            data1=databasefile.SelectQuery1("userMaster",column,whereCondition,"",startlimit,endlimit)
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
            whereCondition="id = '" + str(id)+ "'"
            data1 = databasefile.SelectQuery1("paymentTypeMaster",column,whereCondition)
            print(data1,"data1")
            if data1 != 0:
                column = ""
                whereCondition = ""
                column= " paymentType='" + str(paymentType) + "'"
                whereCondition="id = '" + str(id)+ "'"
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
            whereCondition=""
            data=databasefile.SelectQuery("paymentTypeMaster",column,whereCondition)
        
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
            whereCondition= "paymentType='"+str(paymentType)+ "'"
            data=databasefile.SelectQuery1("paymentTypeMaster",column,whereCondition)
            print(data,'data')
            if data['status']=='false':
                column="paymentType"
                values="'"+str(paymentType)+"' "
                insertdata=databasefile.InsertQuery("paymentTypeMaster",column,values)
                column="*"
                whereCondition= " paymentType='"+str(paymentType)+ "'"
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
                    
                    data = databasefile.SelectQuery1("userMaster",column,WhereCondition,"",startlimit,endlimit)
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
            whereCondition= "  otp='" + otp+ "' and mobileNo='" + mobileNo+"'"
            verifyOtp=databasefile.SelectQuery1(" userMaster ",column,whereCondition)
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
                
            
            whereCondition= " userId= '"+str(userId)+"' and userTypeId='3' "
            column='userId,name,mobileNo,password,email'

            
         
            data11=databasefile.SelectQuery('userMaster',column,whereCondition)
         

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
            column=  "us.mobileNo,us.name,us.userId,um.name as userName"
            whereCondition= "us.mobileNo = '" + str(mobileNo) + "' and us.password = '" + password + "' and us.userTypeId=um.id"
            loginuser=databasefile.SelectQuery1("userMaster as us,usertypeMaster as um",column,whereCondition)
            if (loginuser!=0):   
                              
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
            whereCondition= " us.email = '" + str(email) + "' and us.password = '" + str(password) + "'  and  us.userTypeId=um.id"
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
        whereCondition=" and um.usertypeId=us.id"
        data = databasefile.SelectQuery4("userTypeMaster",columns)
       

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
        aboutId = '1'
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
        keyarr = ['driverId',bookingId,ratingId]
        commonfile.writeLog("addpaymentType",inputdata,0)
        msg = commonfile.CheckKeyNameBlankValue(keyarr,inputdata)
        if msg=="1":
            driverId = inputdata["driverId"]
            bookingId=inputdata['bookingId']
            ratingId=inputdata['ratingId']
            
           
            column="driverId,bookingId,ratingId"
            values="'"+str(driverId)+"' ,'"+str(bookingId)+"','"+str(ratingId)+"'"
            insertdata=databasefile.InsertQuery("userRating",column,values)
            

            output= {"result":"User Added Successfully","message":"","status":"true"}
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
        keyarr = ['userId',bookingId,ratingId]
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


@app.route('/addDrivertest', methods=['POST'])
def addDrivertest():
    try:
        print('Hello')
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
            driverTypeId=int(inputdata['userTypeId'])
           
            column = " * "
            whereCondition= " mobileNo='"+str(mobileNo)+ "' and usertypeId='3' "
            data= databasefile.SelectQuery("userMaster",column,whereCondition)

            column11="id,driverId"

            whereCondition1= " mobileNo='"+str(mobileNo)+ "' and driverTypeId='"+str(driverTypeId)+ "'"
            data1= databasefile.SelectQuery("driverMaster",column11,whereCondition1)

            print(data1,'data')

           
            mobileNo= inputdata["mobileNo"]
            driverId=data['result']['userId']
          
            if data1['status'] == 0:
                WhereCondition = " mobileNo = '" + str(mobileNo) + "'"
                column = " name='" + str(name) + "' ,dlNo = '" + str(DlNo) + "',dlFrontFilename = '" + str(dlFrontFilename) + "',dlFrontFilepath = '" + str(DlFrontPicPath) + "',dlBackFilename = '" + str(dlBackFilename) + "',dlBackFilepath = '" + str(DlBackPicPath) + "',driverTypeId='" + str(driverTypeId) + "',cleanRecord='" + str(cleanRecord) + "'  ,backgroundCheck='" + str(backgroundCheck) + "',recommendiationLetter='" + str(recommendationLetter) + "',healthrecord='" + str(healthrecord) + "',misconduct='" + str(misconduct) + "',socialsecuritynumberTrace='" + str(socialsecuritynumberTrace) + "',trafficScreening ='" + str(trafficScreening) + "',status='1'"
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
            











if __name__ == "__main__":
    CORS(app, support_credentials=True)
    app.run(host='0.0.0.0',port=5034,debug=True)















