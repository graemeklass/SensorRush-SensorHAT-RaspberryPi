#Author: Graeme Klass (graemeklass@gmail.com)
#Description: A script to get all sensor data from the Sense HAT adaptor board for the Raspberry Pi and send to the SensorRush API by taking an average over a specified period
#Python version: 3

from sense_hat import SenseHat #sudo apt-get install sense-hat
import json
import datetime
import requests #sudo pip-3.2 install requests
from collections import OrderedDict #
import time

#**********************************************
#Replace below your username, apikey - below will work but is for demo purposes only.
userName = "sensorrush"
apiKey = "1234"
sensorName = "MyPiSenseHAT" #you can choose your own sensor name
#***********************************************

sense = SenseHat() #sensor object

counter = 0 
masterCounter = 0 
SCROLLSPEED = 0.5 
TIMER = 5*60 #in seconds
print('Started with Timer of {0} seconds'.format(TIMER))
AccX = 0.0
AccY = 0.0
AccZ = 0.0
AccPitch = 0.0
AccYaw = 0.0
AccRoll = 0.0
MagX = 0.0
MagY = 0.0
MagZ = 0.0
Azimuth = 0.0
GyroX = 0.0
GyroY = 0.0
GyroZ = 0.0
GyroPitch = 0.0
GyroYaw = 0.0
GyroRoll = 0.0
Humidity = 0.0
Pressure = 0.0
BoardTemperature = 0.0
start = time.time()
listSample = []
while True:
	AccX += sense.accelerometer_raw['x']
	AccY += sense.accelerometer_raw['y']
	AccZ += sense.accelerometer_raw['z']
	AccPitch += sense.accel['pitch']
	AccYaw += sense.accel['yaw']
	AccRoll += sense.accel['roll']
	MagX += sense.compass_raw['x']
	MagY += sense.compass_raw['y']
	MagZ += sense.compass_raw['z']
	Azimuth += sense.compass
	GyroX += sense.compass_raw['x']
	GyroY += sense.compass_raw['y']
	GyroZ += sense.compass_raw['z']
	GyroPitch += sense.gyro['pitch']
	GyroYaw += sense.gyro['yaw']
	GyroRoll += sense.gyro['roll']
	Humidity += sense.humidity
	Pressure += sense.pressure
	BoardTemperature += sense.temperature

	counter += 1

	end = time.time()
	if (end - start >= TIMER): #let's send 
		sample = OrderedDict() #we use Ordered Dictionary so that when we convert this to JSON format the field order is presered.
		sample['ts'] = datetime.datetime.now().isoformat() #timestample (SensorRush API requires "ts" field to be a timestamp)
		sample['AccX'] = AccX / counter
		sample['AccY'] = AccY / counter
		sample['AccZ'] = AccZ / counter
		sample['AccPitch'] = AccPitch / counter
		sample['AccYaw'] = AccYaw / counter
		sample['AccRoll'] = AccRoll / counter
		sample['MagX'] = MagX / counter
		sample['MagY'] = MagY / counter
		sample['MagZ'] = MagZ / counter
		sample['Azimuth'] = Azimuth / counter
		sample['GyroX'] = GyroX / counter
		sample['GyroY'] = GyroY / counter
		sample['GyroZ'] = GyroZ / counter
		sample['GyroPitch'] = GyroPitch / counter
		sample['GyroYaw'] = GyroYaw / counter
		sample['GyroRoll'] = GyroRoll / counter
		sample['Humidity'] = Humidity / counter
		sample['Pressure'] = Pressure / counter
		sample['BoardTemperature'] = BoardTemperature / counter

		listSample.append(sample)
		jsonVal = json.dumps(listSample)  #convert into JSON formatted array

	 #the following sends an HTTP post to the SensorRush API. You need to have your own username and API key
		try:
			r = requests.post('http://sensorrush.net/{0}/{1}/{2}/Insert'.format(userName, apiKey, sensorName), data = {'': jsonVal})

			print('{0}: Sent {1} averaged data point.'.format(time.ctime(), len(listSample) ))
			start = time.time()
			counter = 0
			AccX = 0.0
			AccY = 0.0
			AccZ = 0.0
			AccPitch = 0.0
			AccYaw = 0.0
			AccRoll = 0.0
			MagX = 0.0
			MagY = 0.0
			MagZ = 0.0
			Azimuth = 0.0
			GyroX = 0.0
			GyroY = 0.0
			GyroZ = 0.0
			GyroPitch = 0.0
			GyroYaw = 0.0
			GyroRoll = 0.0
			Humidity = 0.0
			Pressure = 0.0
			BoardTemperature = 0.0
			listSample = []
		except requests.exceptions.ConnectionError:
			print('{0}: Connection Error... still collecting samples and will upload at the next scheduled time in {1} secs'.format(time.ctime(), TIMER))
			start=time.time()
