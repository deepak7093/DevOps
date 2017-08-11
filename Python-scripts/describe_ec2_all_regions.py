import boto3
import json


details = {}
output = []
res = boto3.client('ec2')
region = res.describe_regions()
# print region
# des_inst = res.describe_instances()
for region in region['Regions']:
	print "Started in region", region['RegionName']
	res = boto3.client('ec2', region_name=region['RegionName'])
	des_inst = res.describe_instances()
	for instance in des_inst['Reservations']:
		for inst in instance['Instances']:
			details = {}
			details['InstanceID'] = inst['InstanceId']
			details['instance-type'] = inst['InstanceType']
			details['region'] = region['RegionName']	
			details['state'] = inst['State']['Name']
		output.append(details)
		
print output