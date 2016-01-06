#SensorRush.py
#Author: Graeme Klass (graemeklass@gmail.com)
#Description: A script to get all sensor data from the Sense HAT adaptor board for the Raspberry Pi and send to the SensorRush API
#Python version: 3

from sense_hat import SenseHat #sudo apt-get install sense-hat^C
import json
import datetime
import requests #sudo pip-3.2 install requests
from collections import OrderedDict #

#**********************************************
#Replace below your username, apikey - below will work but is for demo purposes only.
userName = "sensorrush"
apiKey = "1234"
sensorName = "MyPiSenseHAT" #you can choose your own sensor name
#***********************************************

sense = SenseHat() #sensor object

counter = 0 
masterCounter = 0 
BATCHSIZE = 10 #batch size
MASTERCOUNT = 1000 #number of batches to send
SCROLLSPEED = 0.5 

print('Started with Batch size: {0}, Master counter: {1}'.format(BATCHSIZE, MASTERCOUNT))

#outer loop is the master count of number of batches to send.
while True:
	listSample = [] 
	#inner loop records sensor samples and puts into a list
	while True:
		sample = OrderedDict() #we use Ordered Dictionary so that when we convert this to JSON format the field order is presered.
		sample['ts'] = datetime.datetime.now().isoformat() #timestample (SensorRush API requires "ts" field to be a timestamp)
		sample['AccX'] = sense.accelerometer_raw['x']
		sample['AccY'] = sense.accelerometer_raw['y']
		sample['AccZ'] = sense.accelerometer_raw['z']
		sample['AccPitch'] = sense.accel['pitch']
		sample['AccYaw'] = sense.accel['yaw']
		sample['AccRoll'] = sense.accel['roll']
		sample['MagX'] = sense.compass_raw['x']
		sample['MagY'] = sense.compass_raw['y']
		sample['MagZ'] = sense.compass_raw['z']
		sample['Azimuth'] = sense.compass
		sample['GyroX'] = sense.compass_raw['x']
		sample['GyroY'] = sense.compass_raw['y']
		sample['GyroZ'] = sense.compass_raw['z']
		sample['GyroPitch'] = sense.gyro['pitch']
		sample['GyroYaw'] = sense.gyro['yaw']
		sample['GyroRoll'] = sense.gyro['roll']
		sample['Humidity'] = sense.humidity
		sample['Pressure'] = sense.pressure
		sample['BoardTemperature'] = sense.temperature

		listSample.append(sample)
		counter += 1
		if counter == BATCHSIZE:
				counter = 0
				break
	
	jsonVal = json.dumps(listSample)  #convert into JSON formatted array
	
	r = requests.post('http://sensorrush.net/{0}/{1}/{2}/Insert'.format(userName, apiKey, sensorName), data = {'': jsonVal}) #the following sends an HTTP post to the SensorRush API. You need to have your own username and API key
	masterCounter += 1
	print('Sent: {0}'.format(masterCounter*BATCHSIZE))

		#uncomment if you want to display on senseHAT to display a message
        #sense.show_message('B: {0}'.format(masterCounter*BATCHSIZE), scroll_speed = SCROLLSPEED, text_colour = [255,0,255]) 

	if masterCounter == MASTERCOUNT:
		break

print('Finished!'.format(BATCHSIZE, MASTERCOUNT))

