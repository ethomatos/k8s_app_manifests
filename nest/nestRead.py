#from urllib.parse import urlparse
#from argparse import ArgumentParser
from datadog import initialize, api, statsd
#from ddtrace import tracer
#from flask import Flask
import http.client
import json
import time
import os

# Initial setup of variables
clientID = os.getenv('CLIENTID')
clientSecret = os.getenv('CLIENTSECRET')
refreshToken = os.getenv('REFRESHTOKEN')
projectID = os.getenv('PROJECTID')
debug = False

# Open the file that holds the access token acquired last
def getToken(file):
	if (debug): print("In getToken reading in " + file)
	data = json.load(open(file))
	token = data['access_token']
	if (debug): print("Retrieved token and acquired " + token)
	return(token)

# Update the file with the latest access token
def putToken(file, token):
	accessToken = open(file, 'w')
	accessToken.write(token)
	accessToken.close()

# Currently the API is seeing two kitchen devices, this will re-map to the correct device name for one of the devices
def remapKitchen(name):
	if name == "enterprises/17f0511f-e6bb-44e2-a53b-dacb340da87f/devices/AVPHwEusHfiJLwaqLMgf3nqCR0r4oDNpTvT7JS-WPr2QXID2HNcLneMcXHyuAj-KWu5YA5O9DYeeHPwfTuHhA79nEt3xZg":
		return('2ndFloor')
	else:
		return('Kitchen')

# Function to retrieve a new access token
def getNewAccessToken():
	grantType = "refresh_token"
	connection = http.client.HTTPSConnection("www.googleapis.com")
	payload = "client_id=" + clientID + "&client_secret=" + clientSecret + "&refresh_token=" + refreshToken + "&grant_type=" + grantType
	headers = { 'content-type': "application/x-www-form-urlencoded" }
	connection.request("POST", "/oauth2/v4/token", payload, headers)
	response = connection.getresponse()
	data = response.read()
	return(data.decode("utf-8"))

# Function to query using the API to list Nest devices 
def queryAPI(tokenfile, accessToken):
	if (debug): print("In queryAPI")
	connection = http.client.HTTPSConnection("smartdevicemanagement.googleapis.com")
	headers = { 'content-type': "application/json", 'authorization': "Bearer " + accessToken}
	getURL = "/v1/enterprises/" + projectID + "/devices"
	if (debug): print("Constructing URL " + getURL)
	connection.request("GET", getURL, headers=headers)
	if (debug): print("Setting up connection request")
	response = connection.getresponse()
	if (debug): print("Received response " + str(response.status))
	if response.status == 401:
		accessToken = getNewAccessToken()
		putToken(tokenfile, accessToken)
		queryAPI(tokenfile, accessToken)
	data = response.read()
	return(data.decode("utf-8"))

# Main routine of the program
def main():
	if (debug): print("In main")
	options = {
		'api_key': os.getenv('API_KEY'),
		'app_key': os.getenv('APP_KEY'),
    "statsd_host": os.getenv('DD_AGENT_HOST'), 
    "statsd_port": 8125
	}
	initialize(**options)
	if (debug): print("Initialize options")

	statsd.namespace = 'system.nest'
	statsd.constant_tags = ['owner', 'et']
	
	while True:
		if (debug): print("In while loop")
		try:
			if (debug): print("In try block")
			# re-use previously successful access token, it resets every hour
			data = json.loads(queryAPI('token', getToken('token')))
			processQuery(data, statsd)
		except:
			main()
		# Wait before continuing with the next query
		time.sleep(60)

def processQuery(data, statsd):
	log = ''
	for key in data['devices']:
		if ('sdm.devices.traits.Temperature' in key['traits'] and 'sdm.devices.traits.Humidity' in key['traits']): 
			deviceName = key['parentRelations'][0]['displayName']
			tag = "nest:" 
			if (deviceName == 'Kitchen'):
				tag += remapKitchen(key['name'])
			elif (deviceName == 'Downstairs'):
				tag += '1stFloor'
			else:
				tag += deviceName
			metric = key['traits']['sdm.devices.traits.Temperature']['ambientTemperatureCelsius']
			log += tag + "," + str(metric)
			statsd.gauge('temp', metric, tags=[tag])
			metric = key['traits']['sdm.devices.traits.Humidity']['ambientHumidityPercent']
			log += "," + str(metric) + "\n"
			statsd.gauge('humidity', metric, tags=[tag])
	if (debug): print(log)

if __name__ == "__main__":
	if (debug): print("In __name__")
	main()
