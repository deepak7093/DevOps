import os
import json
import urllib2
from netaddr import IPNetwork
import pprint

# Get data from url
url = urllib2.Request("https://ip-ranges.amazonaws.com/ip-ranges.json")
response = urllib2.urlopen(url)
json_data = json.load(response)
data = json_data['prefixes']
region = set()
service = set()
for i in data:
    region.add(i['region'])
for i in data:
    service.add(i['service'])

print "######### AMZON REGIONS #######"
pprint.pprint(region)

print "########## AMAZON SERVICES ######"
pprint.pprint(service)

ip = []

for i in data:
    ip.append(i['ip_prefix'])

total = 0
for i in ip:
    ip = IPNetwork(i)
    ip_new = ip.size - 2
    total = total + ip_new

print "########  Total number of availables ip's:", total

reg_ip = {}
for i in region:
    total_reg = 0
    for j in data:
        if j['region'] == i:
            ip_reg = j['ip_prefix']
            ip = IPNetwork(ip_reg)
            ip_new = ip.size - 2
            total_reg = total_reg + ip_new
    # print("Total ip in region", i, "are", total_reg)
            reg_ip[i] = total_reg
print "########## AMAZON ip address per region #########"
pprint.pprint(reg_ip)


reg_service = {}
for i in service:
    total_reg = 0
    for j in data:
        if j['service'] == i:
            ip_reg = j['ip_prefix']
            ip = IPNetwork(ip_reg)
            ip_new = ip.size - 2
            total_reg = total_reg + ip_new
    # print("Total ip in region", i, "are", total_reg)
            reg_service[i] = total_reg
print "############# AMAZON ip address per service ##################"
pprint.pprint(reg_service)
