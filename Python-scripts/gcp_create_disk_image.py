"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Compute Engine API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/compute
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
---------------

Title: Create images/snapshot of all disks in GCP project.
"""

from pprint import pprint
import googleapiclient.discovery
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import datetime

credentials = GoogleCredentials.get_application_default()

compute_service = discovery.build('compute', 'v1', credentials=credentials)

now = datetime.datetime.now()
t_date = now.strftime("%Y-%m-%d")

# Project ID for this request.
project = 'sumoplus-1181'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'asia-southeast1-b'  # TODO: Update placeholder value.

request = compute_service.disks().list(
    project=project, zone=zone)
while request is not None:
    response = request.execute()

    for instance in response['items']:
        
        # TODO: Uncomment for image creation
        # pprint(instance['name'])
        # pprint(instance['selfLink'])
        
        # image_name = instance['name']+"-"+t_date
        # sourceDisk = instance['selfLink']
        # config = {
        #     "name" : image_name , 
        #     "sourceDisk": sourceDisk
        #     }

        # image = compute_service.images().insert(project=project, body=config)
        # response = image.execute()
        # pprint(response)


        ## TODO: Uncomment below sction for snapshots creation

        disk_name = instance['name']
        snapshot_name = instance['name'] + "-" + t_date
        sourceDisk = instance['selfLink']
        
        snapshot_config = {
                "name" : snapshot_name ,
                "sourceDisk": sourceDisk
        }
        snapshot = compute_service.disks().createSnapshot(project=project, body=snapshot_config, disk=disk_name, zone=zone)
        response = snapshot.execute()
        print disk_name
        pprint(response)
        
