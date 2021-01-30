#!/usr/bin/env python3

""" Some documentation string"""

from bluepy.btle import Scanner, DefaultDelegate, ScanEntry
#from bluepy.btle import *
import os
import time
import struct
import paho.mqtt.client as mqtt
import json
import os
import re
import binascii
from binascii import unhexlify

BLE_DEVICE=int(os.getenv('BLE_DEVICE',0))
SCAN_TIME=float(os.getenv('SCAN_TIME',7.0))
MQTT_HOST=os.getenv('MQTT_HOST','192.168.2.50')
MQTT_PORT=int(os.getenv('MQTT_PORT',1883))
MQTT_TIMEOUT=int(os.getenv('MQTT_TIMEOUT',60))
MQTT_MAIN_TOPIC=os.getenv('MQTT_MAIN_TOPIC','sensors')

esp_sensor_scan_entry=None

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
#            print ("Discovered device", dev.addr)
            jsObj = {}
            if (bool(re.match('58:2D:34',str(dev.addr),re.I))): #This is Xiaomi Clear Glass sensor
                print(f"Sensor Qingping found at {dev.addr}")
                raw = dev.getValueText(22)
#                print ("Service Data - 16-bit value: ",raw)
                if (raw[0:4] == '95fe' and raw[8:12] == '4703'):
                    jsObj['DeviceName'] = "Xiaomi CGG1"
                    jsObj['DeviceAddr'] = str(dev.addr)
                    if raw[26:28] == '04': #Temp 2 bytes
                        temp = int(raw[34:36]+raw[32:34],16)/10
                        print ("Temperature = ", temp) 
                        topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Temperature'
                        jsObj['UserInformation']="Temperature[C]"
                        jsObj['Value']=round(temp,2)
                        jsonStr = json.dumps(jsObj)
                        print(jsonStr) 
                        mqttc.publish(topic,jsonStr)                 
                    if raw[26:28] == '06': #Humidity 2 bytes
                        humidity = int(raw[34:36]+raw[32:34],16)/10
                        print ("Humidity = ", humidity)
                        topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Humidity'                     
                        jsObj['UserInformation']="Humidity[%]"
                        jsObj['Value']=round(humidity,2)
                        jsonStr = json.dumps(jsObj)
                        print(jsonStr) 
                        mqttc.publish(topic,jsonStr) 
                    if raw[26:28] == '0d': #Temp + humidity 2 + 2 bytes
                        temp = int(raw[34:36]+raw[32:34],16)/10
                        humidity = int(raw[38:40]+raw[36:38],16)/10
                        print ("Temperature = ", temp)
                        topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Temperature'
                        jsObj['UserInformation']="Temperature[C]"
                        jsObj['Value']=round(temp,2)
                        jsonStr = json.dumps(jsObj)
                        print(jsonStr) 
                        mqttc.publish(topic,jsonStr)                 
                        print ("Humidity = ", humidity)
                        topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Humidity'                     
                        jsObj['UserInformation']="Humidity[%]"
                        jsObj['Value']=round(humidity,2)
                        jsonStr = json.dumps(jsObj)
                        print(jsonStr) 
                        mqttc.publish(topic,jsonStr)
                    if raw[26:28] == '0a': #battery 1 byte
                        battery = int(raw[32:36],16)
                        print ("Battery % = ", battery)
                        topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Battery'  
                        jsObj['UserInformation']="Battery Level"
                        jsObj['CharacteristicName']="Battery Level"
                        jsObj['Value']=battery
                        jsonStr = json.dumps(jsObj)
                        print(jsonStr) 
                        mqttc.publish(topic,jsonStr)                                          
            if (bool(re.match('C4:4F:33:05:FD:DB',str(dev.addr),re.I))):   #This is ESP_SENSOR
                dev_name_tmp = dev.getValueText(9)
                if dev_name_tmp:
                  dev_name = dev_name_tmp 
                else: 
                  dev_name="ESP_SENSOR" 
                print(f"Sensor {dev_name} found at {dev.addr}") 
                raw = dev.getValueText(22)   
                print ("Service Data - 16-bit value: ",raw)
                if len(raw)>=38:
                    (temp,humidity,pressure,voc,acc)=struct.unpack('ffffb',unhexlify(raw[4:38]))
                    print (f"Temperature={round(temp,2)}, Humidity={round(humidity,2)}, Pressure={round(pressure,2)}, VOC={round(voc,1)}, Accuracy={acc}") 
                    jsObj['DeviceAddr'] = str(dev.addr)
                    topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Temperature'
                    jsObj['DeviceName'] = dev_name
                    jsObj['UserInformation']="Temperature[C]"
                    jsObj['Value']=round(temp,2)
                    jsonStr = json.dumps(jsObj)
                    print(jsonStr) 
                    mqttc.publish(topic,jsonStr)
                    topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Humidity'
                    jsObj['UserInformation']="Humidity[%]"
                    jsObj['Value']=round(humidity,2)
                    jsonStr = json.dumps(jsObj)
                    print(jsonStr) 
                    mqttc.publish(topic,jsonStr)
                    topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Pressure'
                    jsObj['UserInformation']="Pressure[mmHg]"
                    jsObj['Value']=round(pressure,2)
                    jsonStr = json.dumps(jsObj)
                    print(jsonStr) 
                    mqttc.publish(topic,jsonStr)
                    topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'VOC'
                    jsObj['UserInformation']="Breath VOC Equivalent"
                    jsObj['Value']=round(voc,2)
                    jsonStr = json.dumps(jsObj)
                    print(jsonStr) 
                    mqttc.publish(topic,jsonStr)
                    topic = MQTT_MAIN_TOPIC + '/' + jsObj['DeviceAddr'] + '/' + 'Accuracy'
                    jsObj['UserInformation']="IAQ Accuracy"
                    jsObj['Value']=acc
                    jsonStr = json.dumps(jsObj)
                    print(jsonStr) 
                    mqttc.publish(topic,jsonStr)

                else:
                    print(f"Length of data from ESP_SENSOR is too short {len(raw)}. Skipping packets.")
        elif isNewData:
            if (bool(re.match('58:2D:34',str(dev.addr),re.I))):
                print ("Received new data from Qingping sensor", dev.addr)
#                print ("Service Data - 16-bit value:", dev.getValueText(22))
            
        
os.system('hciconfig hci0 down')
os.system('hciconfig hci0 up')

print(f"Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT}")
mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_TIMEOUT)
mqttc.loop_start()

scanner = Scanner(BLE_DEVICE).withDelegate(ScanDelegate())
while True:
    print("New scan cycle")
    try:
        devices = scanner.scan(SCAN_TIME)
    except BTLEException as e:
        print("Error while scanning for BLE devices")
