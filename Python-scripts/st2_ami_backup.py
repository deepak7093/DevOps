import boto3
import datetime
import re


ec2_client = boto3.client('ec2')
Instance_id = "i-0fd2851dd1a3fb6a2"  # stackstorm EC2 id
RETENTION_PERIOD = 3


def create_ami(event, context):
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["InstanceId"] == Instance_id:
                print "Creating AMI for instance:", instance["Tags"][0]["Value"]
                tdate = datetime.datetime.now()
                timestamp = tdate.strftime('%Y%m%d')
                ami_name = instance["Tags"][0]["Value"] + "_" + timestamp
                try:
                    res = ec2_client.create_image(InstanceId=Instance_id, Name=ami_name, NoReboot=True)
                    print res['ImageId']
                    ec2_client.create_tags(Resources=[res['ImageId']], Tags=[{'Key': 'Created_date', 'Value': timestamp}])
                except Exception as e:
                    print "Image creation failed"
                    print e


def delete_old_ami(event, context):
    images = ec2_client.describe_images(Owners=['089816662102'])
    # for k, v in images.iteritems():
    #     print k
    for image in images['Images']:
        if image.get("Tags", None) is not None:
            if image['Tags'][0]['Key'] == 'Created_date':
                image_create_date = image['Tags'][0]['Value']
                prog = re.compile("^(\(?\+?[0-9]*\)?)$")
                if prog.match(image_create_date):
                    tdate = datetime.datetime.now()
                    timestamp = tdate.strftime('%Y%m%d')
                    day_created_before = int(timestamp) - int(image_create_date)
                    if int(day_created_before) > RETENTION_PERIOD:
                        try:
                            ec2_client.deregister_image(ImageId=image['ImageId'])
                            print "Deleted AMI with ID:", image['ImageId']
                        except Exception as e:
                            print e
