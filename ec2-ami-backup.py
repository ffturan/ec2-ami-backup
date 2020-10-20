import boto3
import sys
import os
import time
from datetime import date
from botocore.exceptions import ClientError

worker = boto3.client('ec2')
now=date.today()

def lambda_handler(event, context):
    vTagKey="tag:" + os.environ['TAG_KEY']
    vTagValue=os.environ['TAG_VALUE']
    try:
        # 
        # Filter all Instances with Tag:Backup Value:True 
        #
        response = worker.describe_instances(Filters=[{'Name':vTagKey,'Values':[vTagValue,]},])
        #print(response)
        # 
        # Get the InstanceId from response  
        #
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                #
                # This will print will output the value of the Dictionary key 'InstanceId'
                # print(instance["InstanceId"], instance["InstanceType"])
                #
                id_holder=instance["InstanceId"]
                tag_holder=instance["Tags"]
                # 
                # Find the Instance Name 
                #
                for item in tag_holder:
                    if item['Key'] == 'Name':
                        name_holder=item['Value']
                # 
                # Build Instance description
                #
                desc_holder=name_holder+'-'+id_holder+'-'+str(now)
                # 
                # Create AMI
                #
                response=worker.create_image(Description=desc_holder,Name=desc_holder,InstanceId=id_holder,NoReboot=True)
                ami_holder=response['ImageId']
                #print(ami_holder)
                time.sleep(2)
                # 
                # Tag created AMI
                #
                response=worker.create_tags(Resources=[ami_holder],Tags=[{'Key':'Name', 'Value':str(desc_holder)},],)
                # 
                # Print results
                #
                print(f'{ami_holder} has been created with name {desc_holder}')
    except ClientError as e:
        print(e)
