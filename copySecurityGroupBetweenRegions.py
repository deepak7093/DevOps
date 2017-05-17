import boto3
# Global Variables
GroupName = []
Sg_Description = []
Ingress = []
Egress = []
vpc_id = []
my_dict1 = {}
my_dict2 = {}

# Function for descibe existing secuirity_groups
def get_security_groups(source_region, source_vpc_id):
# Start session in source region
    boto3.setup_default_session(region_name=source_region)
# Create EC2 client and desribe sg instance
    ec2 = boto3.client('ec2')
    security_groups = ec2.describe_security_groups()
# Create dict with GroupId:GroupName
    for sg in security_groups['SecurityGroups']:
        my_dict1[sg['GroupId']] = sg['GroupName']
# Create list of SecurityGroup Names
    for name in security_groups['SecurityGroups']:
        if name['VpcId'] == source_vpc_id:
            GroupName.append(name['GroupName'])
# Create list of SecurityGroup Description
    for desc in security_groups['SecurityGroups']:
        if name['VpcId'] == source_vpc_id:
            Sg_Description.append(desc['Description'])
# Create list of SecurityGroup Ingress rules
    for rule in security_groups['SecurityGroups']:
        if name['VpcId'] == source_vpc_id:
            Ingress.append(rule['IpPermissions'])
# Create list of SecurityGroup Egress rules
    for rule in security_groups['SecurityGroups']:
        if name['VpcId'] == source_vpc_id:
            Egress.append(rule['IpPermissionsEgress'])

# Function for create new SecurityGroups in new region
def create_sg(dest_region, dest_vpc_id):
# Start new session in destination region
    boto3.setup_default_session(region_name=dest_region)
# Create EC2 client and desribe sg instance
    ec2_new = boto3.client('ec2')
    security_groups = ec2_new.describe_security_groups()
# Define local variables
    dest_vpc = [dest_vpc_id]
    new_vpc = []
    dest_sg_name = []
    Dest_GroupId  = []
# create list of already existed sg
    for name in security_groups['SecurityGroups']:
        if name['VpcId'] == dest_vpc_id:
            dest_sg_name.append(name['GroupName'])
    for id in security_groups['SecurityGroups']:
        if id['VpcId'] == dest_vpc_id:
            Dest_GroupId.append(id['GroupId'])

# exapnd list of vpc_id to match len of GroupName
    for vp in dest_vpc:
        for m in range(len(GroupName)):
            new_vpc.append(vp)
# Create zip of GroupName, Sg_Description, new_vpc, Ingress, Egress
    data_list = zip(GroupName, Sg_Description, new_vpc, Ingress, Egress)

# Create new instance for sg
    security_groups_new = ec2_new.describe_security_groups()
# Create security groups only if sg with same name not exists
    for data in data_list:
        groupname = data[0]
        sg_description = data[1]
        vpc_id = data[2]

        if groupname not in dest_sg_name:
             print "GROUPNAME:" + groupname
             response = ec2_new.create_security_group(GroupName=groupname, Description=sg_description, VpcId=vpc_id)
             print "GroupId" + response['GroupId']

    for name in security_groups_new['SecurityGroups']:
        if name['VpcId'] == dest_vpc_id:
            dest_sg_name.append(name['GroupName'])
    security_groups_new = ec2_new.describe_security_groups()

    for sg in security_groups_new['SecurityGroups']:
        my_dict2[sg['GroupName']] = sg['GroupId']
# Create Ingress rules for above created Sg
    for data in data_list:
        groupname = data[0]
        sg_description = data[1]
        vpc_id = data[2]
        ingress = data[3]
        egress = data[4]
# Update ingress rule with sg_id with new sg_id
        for ing in ingress:
            if len(ing['UserIdGroupPairs']) != 0:
                for j in ing['UserIdGroupPairs']:
                    gid = j['GroupId']
                    id = my_dict1[gid]
                    j['GroupId'] = my_dict2[id]

        if groupname not in dest_sg_name:
            print groupname
            ec2_res = boto3.resource('ec2')
            security_group = ec2_res.SecurityGroup(my_dict2[groupname])
            print my_dict2[groupname]
            security_group.authorize_ingress(IpPermissions=ingress)
        else:
            print "ignoring:", groupname
# Main Function Defination
if __name__ == '__main__':
    source_region = raw_input("Enter Source Region:")
    source_vpc_id = raw_input("Enter Source VPC ID:")
    dest_region = raw_input("Enter Destination Region:")
    dest_vpc_id = raw_input("Enter Destination VPC ID:")
    get_security_groups(source_region, source_vpc_id)
    create_sg( dest_region, dest_vpc_id)
