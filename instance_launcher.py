import boto3
import configparser


# Parse config file
config = configparser.ConfigParser()
config.read('aws_config.ini') 

aws_access_key_id = config.get('default', 'aws_access_key_id')
aws_secret_access_key = config.get('default', 'aws_secret_access_key')
region_name = config.get('default', 'region_name')
ami_id = config.get('default', 'ami_id')
instance_type = config.get('default', 'instance_type')
key_pair_name = config.get('default', 'key_pair_name')
sg_id = config.get('default', 'security_group_id')

# Create EC2 client
ec2 = boto3.client('ec2',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)

# Create EC2 instance
response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_pair_name,
    SecurityGroupIds=[sg_id],
    #UserData='jupyter notebook'
)

instance_id = response['Instances'][0]['InstanceId']
print(f"EC2 instance created with Instance ID: {instance_id}")

# Retrieve the public IP address of the instance
ec = boto3.resource('ec2')
instance = ec.Instance(instance_id)
instancePublicDNS = instance.public_dns_name
print(f'Public DNS of Instance: {instancePublicDNS}')

# Terminate the instance
def terminate_instance():
    print(f'Terminating instance {instance_id}')
    ec2.terminate_instances(InstanceIds=[instance_id])

# Exit program when user hits enter
while True:
    if input('Type "exit" to Terminate Instance and exit...') == "exit":
        terminate_instance()
        quit()
