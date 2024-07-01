import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import json
import time
GPIO.setmode(GPIO.BCM)
reader = SimpleMFRC522()

##LED
GPIO.setwarnings(False)
r=14
g=15

GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
red=GPIO.PWM(r,100)
green=GPIO.PWM(g,100)

def redControl():
    red.ChangeDutyCycle(100)
    time.sleep(2)
    red.ChangeDutyCycle(0)
        
def greenControl():
    green.ChangeDutyCycle(100)
    time.sleep(2)
    green.ChangeDutyCycle(0)


#users.json
with open('users.json') as f:
    valid_uids = {user['uid']: user for user in json.load(f)}


#Flask server.
FLASK_SERVER_URL = 'http://127.0.0.1:5000/update_uid'

def send_uid_to_server(uid):
    data = {'uid': uid}

    try: 
        requests.post(FLASK_SERVER_URL, json=data)
    except Exception as e:
        print(f"Error sending UID to server: {e}")


#RFID
try:
    red.start(0)
    green.start(0)
    
    while True:
        id, text = reader.read() #RFID 식별
        print(id)
        if id in valid_uids: #led code
            send_uid_to_server(id)
            greenControl()
        else:
            redControl()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
