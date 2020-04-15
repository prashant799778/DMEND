import paho.mqtt.client as mqtt
import json
import databasefile
from math import sin,cos,sqrt,atan2,radians


def on_connect(client, userdata, flags, rc):
  print("-------Connected-------")
  print(client, userdata, flags, rc)
  client.subscribe("ambulanceLiveLocation")


def on_message(client, userdata, msg):    
  data = msg.payload.decode('utf-8')
  print(data,"===============",type(data))
  data = json.loads(data)
  
  
  try:
    

    lat=data["lat"]
    lng=data["lng"]
    userId=data['driverId']
    R = 6373.0
    bookingId=data['bookingId']
    columns=" bm.bookingTypeId,bm.bookingId,bm.driverId,bm.dropOff,bm.dropOffLatitude,bm.dropOffLongitude"
    columns=columns+",bm.finalAmount,bm.pickup,bm.status,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
    columns=columns+",bm.driverMobile"
    whereCondition22=" d.driverId=bm.driverId  and bm.endStatus='1' and bookingId= '"+str(bookingId)+"' "
    bookingDetails= databasefile.SelectQuery("bookDriver bm,driverMaster am",columns,whereCondition22)
    print(bookingDetails,"================")
    if bookingDetails['status']=='false':
      bookingTypeId=bookingDetails['result']['bookingTypeId']
      if bookingTypeId ==1 or bookingTypeId=='1':
        print('11')
        columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
        columns=columns+",b.finalAmount,b.pickUpTime,b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.userMobile"
        columns=columns+",bm.driverMobile,b.status"
        whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and  bm.bookingId= '"+str(bookingId)+"' "
        bookingDetails1= databasefile.SelectQueryOrderby("bookDriver bm,bookDaliyDriver  b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
        print('Dd')
      if bookingTypeId ==2 or bookingTypeId=='2':
        print('corp')

      
      if bookingTypeId==3 or bookingTypeId=='3':
        columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
        columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,b.totalHours,bm.userMobile "
        columns=columns+",bm.driverMobile,b.status"
        whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and  bm.bookingId= '"+str(bookingId)+"'  "
        bookingDetails1= databasefile.SelectQueryOrderby("bookDriver bm,bookHourlyMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
        print('hourly')
      
      if bookingTypeId ==4 or bookingTypeId =='4':
        columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
        columns=columns+",bm.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
        columns=columns+",bm.driverMobile,b.status"
        whereCondition22=" and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and  bm.bookingId= '"+str(bookingId)+"'  "
        bookingDetails1= databasefile.SelectQueryOrderby("bookDriver bm,bookOneMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
        print('one')
      
      if bookingTypeId ==5 or bookingTypeId=='5':
        print('round') 
        columns="(dr.lat)driverLat,(dr.lng)driverLng,bm.bookingId,bm.driverId,b.dropOff,b.dropOffLatitude,b.dropOffLongitude"
        columns=columns+",b.finalAmount,bm.pickup,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile "
        columns=columns+",bm.driverMobile,b.status"
        whereCondition22="  and dr.driverId=bm.driverId and bm.bookingId=b.bookingId and  bm.bookingId= '"+str(bookingId)+"'  "
        bookingDetails1= databasefile.SelectQueryOrderby("bookDriver bm,bookRoundMaster b,driverRideStatus dr",columns,whereCondition22,"",startlimit,endlimit,orderby)
                      

                    


   
    
    
   
    userLat=bookingDetails1['result']['dropOffLatitude']
    userLng=bookingDetails1['result']['dropOffLongitude']
    fromlongitude2= lng
    print(fromlongitude2,'fromlong',type(fromlongitude2))
    fromlatitude2 = lat
    print('lat',fromlatitude2)
    distanceLongitude = userLng- fromlongitude2
    distanceLatitude = userLat - fromlatitude2
    a = sin(distanceLatitude / 2)**2 + cos(fromlatitude2) * cos(userLat) * sin(distanceLongitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    distance2=distance/100
    Distance=distance2*1.85
    if Distance < 100:
        bookingDetails["message"]="driver Reached"  
        if (bookingDetails['status']!='false'):

            column="  endindStatus  = '0' "
            whereCondition=" bookingId ='"+str(bookingId)+"'"
            a=databasefile.UpdateQuery('bookDriver',column,whereCondition)
            topic=str(userId)+"/endstatus"
            print(topic,"+++++++++++++++++++=")
            #print(topic,"topic==================")
            data1 = json.dumps(data)
            #print("11111111111111")
            #print(data)        
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish(topic,bookingDetails1)
            client.disconnect()
            return bookingDetails1
        else:
            data={"result":"","message":"Already Reached to driver","status":"false"}
            return data


    else:
        data={"result":"","message":"Already Reached to driver","status":"false"}
        return data
  except Exception as e :
    print("Exception---->" + str(e))    
    output = {"result":"something went wrong","status":"false"}
     
  
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()


          

    
  