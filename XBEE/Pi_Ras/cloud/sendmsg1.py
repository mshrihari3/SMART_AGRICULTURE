from google.cloud import pubsub_v1
import datetime
import json
import dht11_example
import time
import os

credential_path="/home/pi/Desktop/cloud/IoTSensor-bb48f6121160.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=credential_path

project_id = "iotsensor-276409" # enter your project id here
topic_name = "my-topic" # enter the name of the topic that you created
 
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
 
futures = dict()
 
def get_callback(f, data):
    def callback(f):
        try:
            # print(f.result())
            futures.pop(data)
        except:
            print("Please handle {} for {}.".format(f.exception(), data))
 
    return callback
 
while True:
    time.sleep(3)
    result = dht11_example.myfunc()
    temp = result[0]
    hum = result[1]
    if temp>1 and hum>1:
    	timenow = float(time.time())
    # timenow = datetime.datetime.now()
    	data = {"time":timenow, "temp" : temp, "humidity":hum}
    	print(data)
    # When you publish a message, the client returns a future.
    	future = publisher.publish(
    	topic_path, data=(json.dumps(data)).encode("utf-8")) # data must be a bytestring.
    # Publish failures shall be handled in the callback function.
    	future.add_done_callback(get_callback(future, data))
    	time.sleep(5)
# Wait for all the publish futures to resolve before exiting.
while futures:
    time.sleep(5)
 
print("Published message with error handler.")
