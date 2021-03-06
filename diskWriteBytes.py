import boto3,datetime,time
import json
from flask import Flask, jsonify, Response
from boto3.session import Session
from influxdb import InfluxDBClient

app = Flask(__name__)

sessionPSG = Session(aws_access_key_id='xxxxxxxx',
	                    aws_secret_access_key='xxxxxxxxx',
	                    region_name='xxxxxxx')

sessionML = Session(aws_access_key_id='xxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxx',
                region_name='xxxxxxxx')

sessionMD = Session(aws_access_key_id='xxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxx',
                region_name='xxxxxx')

sessionVX = Session(aws_access_key_id='xxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxxx',
                region_name='xxxxxx')

instancePSG ='xxxxxx'
instanceML = 'xxxxxx'
instanceMD ='xxxxxxx'
instanceVX='xxxxxxx'


clientPSG=sessionPSG.client('cloudwatch')
clientML=sessionML.client('cloudwatch')
clientMD=sessionMD.client('cloudwatch')
clientVX=sessionVX.client('cloudwatch')

startTime = datetime.datetime.utcnow()-datetime.timedelta(seconds=600)
endTime = datetime.datetime.utcnow()
host='ec2-52-33-84-233.us-west-2.compute.amazonaws.com'
port=8086
user='root'
password='root'
dbname='AWS_MonitorDB'

client = InfluxDBClient(host, port, user, password, dbname)
def get_diskWriteBytes():
	# Instance: PSG, Metric: CPUUtilization
	responsePSG_DiskWriteBytes = clientPSG.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskWriteBytes',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instancePSG
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responsePSG_DiskWriteBytes)>0:
		if len(responsePSG_DiskWriteBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskWriteBytes",
            				"tags": {
                				"Instance-ID": instancePSG
           		 		},
            				"time": responsePSG_DiskWriteBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instancePSG,
                				"Minimum":responsePSG_DiskWriteBytes['Datapoints'][0]['Minimum'],
                				"Unit":responsePSG_DiskWriteBytes['Datapoints'][0]['Unit'],
                				"Sum":responsePSG_DiskWriteBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responsePSG_DiskWriteBytes['Datapoints'][0]['SampleCount'],
                				"Average":responsePSG_DiskWriteBytes['Datapoints'][0]['Average'],
                				"Maximum":responsePSG_DiskWriteBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instancePSG)
	else:
		print("Result is null.",instancePSG)


	responseML_DiskWriteBytes = clientML.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskWriteBytes',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instanceML
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responseML_DiskWriteBytes)>0:
		if len(responseML_DiskWriteBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskWriteBytes",
            				"tags": {
                				"Instance-ID": instanceML
           		 		},
            				"time": responseML_DiskWriteBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceML,
                				"Minimum":responseML_DiskWriteBytes['Datapoints'][0]['Minimum'],
                				"Unit":responseML_DiskWriteBytes['Datapoints'][0]['Unit'],
                				"Sum":responseML_DiskWriteBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responseML_DiskWriteBytes['Datapoints'][0]['SampleCount'],
                				"Average":responseML_DiskWriteBytes['Datapoints'][0]['Average'],
                				"Maximum":responseML_DiskWriteBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceML)
	else:
		print("Result is null.",instanceML)

	# responseMD_DiskWriteBytes = clientMD.get_metric_statistics(
	# 			 Namespace='AWS/EC2',
	# 	                MetricName='DiskWriteBytes',
	# 	                Dimensions=[
	# 	                        {
	# 	                                'Name':'InstanceId',
	# 	                                'Value':instanceMD
	# 	                        },
	# 	                ],
	# 	                StartTime=startTime,
	# 	                EndTime=endTime,
	# 	                Period=300,
	# 	                Statistics=[
	# 	                        'Average','Maximum','SampleCount','Sum','Minimum'
	# 	                ],
	# 	                Unit='Bytes'
	# 	            )
	# print(responseMD_DiskWriteBytes)
		
	# if len(responseMD_DiskWriteBytes)>0:
	# 	if len(responseMD_DiskWriteBytes['Datapoints'])>0:
	# 		json_body=[
 #        			{
 #            				"measurement": "diskWriteBytes",
 #            				"tags": {
 #                				"Instance-ID": instanceMD
 #           		 		},
 #            				"time": responseMD_DiskWriteBytes['Datapoints'][0]['Timestamp'],
 #            				"fields": {
 #                				"Instance-ID": instanceMD,
 #                				"Minimum":responseMD_DiskWriteBytes['Datapoints'][0]['Minimum'],
 #                				"Unit":responseMD_DiskWriteBytes['Datapoints'][0]['Unit'],
 #                				"Sum":responseMD_DiskWriteBytes['Datapoints'][0]['Sum'],
 #                				"SampleCount":responseMD_DiskWriteBytes['Datapoints'][0]['SampleCount'],
 #                				"Average":responseMD_DiskWriteBytes['Datapoints'][0]['Average'],
 #                				"Maximum":responseMD_DiskWriteBytes['Datapoints'][0]['Maximum']
 #            				}
 #        			}
 #    			]

	# 		client.write_points(json_body)
	# 	else:
	# 		print("Datapoints is null.",instanceMD)
	# else:
	# 	print("Result is null.",instanceMD)

	responseVX_DiskWriteBytes = clientVX.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskWriteBytes',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instanceVX
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	print(responseVX_DiskWriteBytes)
		
	if len(responseVX_DiskWriteBytes)>0:
		if len(responseVX_DiskWriteBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskWriteBytes",
            				"tags": {
                				"Instance-ID": instanceVX
           		 		},
            				"time": responseVX_DiskWriteBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceVX,
                				"Minimum":responseVX_DiskWriteBytes['Datapoints'][0]['Minimum'],
                				"Unit":responseVX_DiskWriteBytes['Datapoints'][0]['Unit'],
                				"Sum":responseVX_DiskWriteBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responseVX_DiskWriteBytes['Datapoints'][0]['SampleCount'],
                				"Average":responseVX_DiskWriteBytes['Datapoints'][0]['Average'],
                				"Maximum":responseVX_DiskWriteBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceVX)
	else:
		print("Result is null.",instanceVX)

if __name__ == '__main__':
    get_diskWriteBytes()
