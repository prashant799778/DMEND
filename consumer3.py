
import paho.mqtt.client as mqtt
import json
import databasefile



def on_connect(client, userdata, flags, rc):
  print("-------Connected-------")
  print(client, userdata, flags, rc)
  client.subscribe("#")
  #client.publish("#", "Hello world!");



def on_message(client, userdata, msg):    
  data = msg.payload.decode('utf-8')

  print(data,"===============",type(data))
  data = json.loads(data)
  # print(msg,"===============")
  # print(data,"============",msg.topic)
  print(msg.topic,"1111111111!!!!!!!!!!!")
  y=msg.topic

  #topic=str(msg.topic)#+"/ambulanceLiveLocation"
  topic=data["driverId"]+"/liveLocation"
  
  print(topic,"topic==================")
  data1 = json.dumps(data)
  print("11111111111111")
  
  #print("1")
  #print(data)
  client.publish(topic, data1)
  



  topic1=data["userId"]+"/liveLocation"
  print(topic1,"topic==================")
  data1 = json.dumps(data)
  print("11111111111111")
  
  #print("1")
  #print(data)
  client.publish(topic1, data1)
  client.disconnect()
  #print("2")
  #print("qqqqqqqqqqqqqqqqqqqqqqqqqqqq")
  
  try:
    
    #print(data)
   
    driverId=data["driverId"]
    lat=data["lat"]
    lng=data["lng"]

    column=" driverId, onTrip,onDuty "
    whereCondition=" driverId='"+str(driverId)+"'"
    driverTripDetails = databasefile.SelectQuery1("driverRideStatus",column,whereCondition)
    

    
    if (driverTripDetails[0]["onTrip"]==1) and (driverTripDetails[0]["onDuty"]==1):

      column1=" id,bookingId "
      whereCondition1=" and  driverId='"+str(driverId)+"'"
      orderby=" id "
      driverRideId = databasefile.SelectQueryOrderby("bookDriver",column1,whereCondition1,"","0","1",orderby)


      column1=" lat,lng "
      whereCondition1=" and  rideId='"+str(driverRideId["result"][0]["bookingId"])+"'"
      orderby=" id "
      driverLatLong = databasefile.SelectQueryOrderby("driverRideTracking",column1,whereCondition1,"","0","1",orderby)

      if (lat!=driverLatLong["result"][0]["lat"]) or lng!=driverLatLong["result"][0]["lng"]:
        column=" rideId,driverId,lat,lng "
        values="'"+str(driverRideId["result"][0]["bookingId"])+"','"+str(driverId)+"','"+str(lat)+"','"+str(lng)+"'"
        insertdata=databasefile.InsertQuery("ambulanceRideTracking",column,values)
      
      else:
        pass
    
    elif  (driverTripDetails[0]["onTrip"]==0) and (driverTripDetails[0]["onDuty"]==1):
      print("2222222222222222222")
      column= " lat='" + str(lat) +"',lng='"+ str(lng) + "'"
      
      data = databasefile.UpdateQuery("driverRideStatus",column,whereCondition)

    
  except Exception as e :
    #print("Exception---->" + str(e))    
    output = {"result":"something went wrong","status":"false"}
     
  




client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()