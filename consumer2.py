import paho.mqtt.client as mqtt
import json
import databasefile
from math import sin,cos,sqrt,atan2,radians


def on_connect(client, userdata, flags, rc):
  print("-------Connected-------")
  print(client, userdata, flags, rc)
  client.subscribe("ambulanceLiveLocation")
  #client.publish("#", "Hello world!");

def on_message(client, userdata, msg):    
  data = msg.payload.decode('utf-8')
  print(data,"===============",type(data))
  data = json.loads(data)
  # print(msg,"===============")
  # print(data,"============",msg.topic)
  #topic=str(msg.topic)#+"/ambulanceLiveLocation"
 
  #print("2")
  #print("qqqqqqqqqqqqqqqqqqqqqqqqqqqq")
  
  try:
    #data={"userId":"0726dd0e4f2911ea93d39ebd4d0189f1","driverId":["0726dd0e4f2911ea93d39ebd4d0189f1"],"startLocationLat":29.2261234,"startLocationLong":77.6294229,"pickupLocationAddress":"Unnamed Road, Uttar Pradesh, India, null","dropLocationLat":28.6185,"dropLocationLong":77.3726,"dropLocationAddress":"Fortis Hospital sec-62, Noida","lat":29.3309517,"lng":77.6171017,"ambulanceId":"1","bookingId":"5f415bb277ed11ea93d49ebd4d0189fc"}
    ambulanceId=data["ambulanceId"]

    lat=data["lat"]
    lng=data["lng"]
    userId=data['driverId']
    bookingId=data['bookingId']
    columns="(ar.lat)driverLat,(ar.lng)driverLng, bm.ambulanceId,bm.bookingId,bm.driverId,bm.dropOff,bm.dropOffLatitude,bm.dropOffLongitude"
    columns=columns+",bm.finalAmount,bm.pickup,bm.status,bm.pickupLatitude,bm.pickupLongitude,bm.totalDistance,bm.userMobile,am.ambulanceNo "
    columns=columns+",bm.driverMobile"
    whereCondition22=" am.ambulanceId=bm.ambulanceId  and bm.arrivingstatus='1' and bookingId= '"+str(bookingId)+"' "
    bookingDetails= databasefile.SelectQuery("bookAmbulance bm,ambulanceMaster am,ambulanceRideStatus ar",columns,whereCondition22)
    print(bookingDetails,"================")
    bookingDetails1= databasefile.SelectQuery("bookResponder bm,ambulanceMaster am,ambulanceRideStatus ar",columns,whereCondition22)
    if bookingDetails1['status'] !='false':
      R = 6373.0
      
      userLat=bookingDetails1['result']['pickupLatitude']
      
      userLng=bookingDetails1['result']['pickupLongitude']

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
        bookingDetails1["message"]="driver Arrived"  
        
        if (bookingDetails1['status']!='false'):
          bookingDetails1["message"]="driver Arrived"  
          
          column=" arrivingstatus = '0' "
          whereCondition=" bookingId ='"+str(bookingId)+"'"
          a=databasefile.UpdateQuery('bookResponder',column,whereCondition)
          topic=str(userId)+"/arrivingstatus"
          print(topic)
          #print(topic,"topic==================")
          data1 = json.dumps(data)
          #print("11111111111111")
          #print(data)
          client = mqtt.Client()
          client.connect("localhost",1883,60)
          client.publish(topic, data1)
          client.disconnect()
          return bookingDetails1




    R = 6373.0
    userLat=bookingDetails['result']['pickupLatitude']
    userLng=bookingDetails['result']['pickupLongitude']
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
      bookingDetails["message"]="driver Arrived"  
      
      if (bookingDetails['status']!='false'):
        bookingDetails["message"]="driver Arrived"  
        
        column=" arrivingstatus = '0' "
        whereCondition=" bookingId ='"+str(bookingId)+"'"
        a=databasefile.UpdateQuery('bookAmbulance',column,whereCondition)
        topic=str(userId)+"/arrivingstatus"
        print(topic)
        #print(topic,"topic==================")
        data1 = json.dumps(data)
        #print("11111111111111")
        #print(data)
        client = mqtt.Client()
        client.connect("localhost",1883,60)
        client.publish(topic, data1)
        client.disconnect()
        
        return bookingDetails
      
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


          

    
  