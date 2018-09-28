#####################################################################################
# Cloud Computing HW - 1                                                            #
# Create an Instance Programmatically                                               #
#                                                                                   #
# Author: Avaiyang Garg, ag6026                                                     #
#                                                                                   #
#####################################################################################

import boto3
import sys
import os
import random

# To create a key-pair for the instance
def create_key_pair(VarKeyName):
    ec2 = boto3.resource('ec2')
    
    # generating a key-pair
    output = open(VarKeyName+'.pem','w')
    keyPair = ec2.create_key_pair(KeyName=VarKeyName)
    KeyPairOut = str(keyPair.key_material)
    output.write(KeyPairOut)

# To create a new instance
def create_instance(KeyPair, GroupId):
    ec2 = boto3.resource('ec2')

    # here we are using the Amazon Linux 2 AMI with the instance type micro
    instance = ec2.create_instances(ImageId='ami-04681a1dbd79675a5', MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName = KeyPair, SecurityGroupIds = [GroupId])
    print("\nA new instance is created\n")
    print("Instance ID : ",instance[0].id)
    
    return instance[0].id

# To create a security group for the instance
def create_security_group(sgName, sgDesc):
    ec2 = boto3.resource('ec2')
    securityGr = ec2.create_security_group(GroupName=sgName, Description=sgDesc)
    securityGr.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
    return securityGr.id

# List all instances
def list_instances():
    ec2 = boto3.resource('ec2')
    
    # printing all the instances
    for instance in ec2.instances.all():
        print('\n')
        print("The Instance ID : ",instance.id)
        print("State of Instance : ", instance.state)
        print("IP of the Instance: ", instance.public_ip_address)
        print("Region of the Instance: ", instance.placement['AvailabilityZone'])
        print("DNS:",instance.public_dns_name)

# To terminate the instance
def terminate_instance(id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(id)
    response = instance.terminate()
    print("\nInstance is terminated:\n",response)

# To remove the key-pair from the system and the AWS
def removeKeyPair(keyName):
    #To remove from the local system
    if os.path.exists(keyName+'.pem'):
        os.remove(keyName+'.pem')

    # To remove the key-pair from AWS
    ec2 = boto3.client('ec2')
    response = ec2.delete_key_pair(KeyName=keyName)

def main():
    keyPairName= "CloudKeyPair"
    #generating random name for the security group
    randomValue = random.randint(1, 100)
    securityGroupName = "Cloud"
    
    if (len(sys.argv) >= 2):       
        #terminating the instance
        terminate_instance(sys.argv[1])
        print("The instance is terminated")
        
        #removing the key-pair files
        removeKeyPair(keyPairName)
        print("The key is been deleted from the system and AWS")

    else:
        removeKeyPair(keyPairName)
        # removeKeyAWS(keyPairName)
        create_key_pair(keyPairName)
        
        securityGroup = create_security_group(securityGroupName+str(randomValue), "Security Group")
        instance = create_instance(keyPairName, securityGroup)
        
        # to display all the instances
        list_instances()

        print('\nTerminate the instance by providing the instance-id as argument\n')

if __name__ == '__main__': main()