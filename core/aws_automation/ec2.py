import boto3

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name='ap-south-1') 

def launch_instance(image_id='ami-0f5ee92e2d63afc18', instance_type='t2.micro'):
    """
    Launch an EC2 instance with the specified parameters.
    
    Args:
        image_id (str): The ID of the AMI to use for the instance
        instance_type (str): The type of instance to launch (e.g., 't2.micro')
        
    Returns:
        str: The ID of the launched instance
    """
    try:
        response = ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 Instance launched successfully: {instance_id}")
        return instance_id
        
    except Exception as e:
        print(f"Error launching instance: {str(e)}")
        return None

def terminate_instance(instance_id):
    """
    Terminate the specified EC2 instance.
    
    Args:
        instance_id (str): The ID of the instance to terminate
        
    Returns:
        str: The ID of the terminated instance, or None if there was an error
    """
    try:
        if not instance_id:
            print("Error: No instance ID provided")
            return None
            
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Termination initiated for instance: {instance_id}")
        return instance_id
        
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {str(e)}")
        return None


def list_instances(state_filters=None, tag_filters=None, region_name='ap-south-1'):
    """
    List EC2 instances with optional state and tag filters.
    
    Args:
        state_filters (list, optional): List of instance states to filter by. 
            Possible values: 'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'
            Example: ['running', 'stopped']
            
        tag_filters (dict, optional): Dictionary of tag key-value pairs to filter instances.
            Example: {'Environment': 'production', 'Owner': 'devops'}
            
        region_name (str, optional): AWS region name. Defaults to 'ap-south-1'.
    
    Returns:
        list: A list of dictionaries containing instance details. Each dictionary contains:
            - instance_id (str): The ID of the instance
            - instance_type (str): The type of the instance
            - state (str): The current state of the instance
            - public_ip (str): Public IP address if available, else 'N/A'
            - private_ip (str): Private IP address if available, else 'N/A'
            - tags (dict): Dictionary of instance tags if available, else {}
    
    Example:
        # List all running instances
        instances = list_instances(state_filters=['running'])
        
        # List instances with specific tags
        instances = list_instances(tag_filters={'Environment': 'production'})
    """
    try:
        ec2 = boto3.client('ec2', region_name=region_name)
        filters = []
        
        if state_filters:
            filters.append({'Name': 'instance-state-name', 'Values': state_filters})
            
        if tag_filters:
            for key, value in tag_filters.items():
                filters.append({'Name': f'tag:{key}', 'Values': [value]})

        response = ec2.describe_instances(Filters=filters)
        instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_info = {
                    'instance_id': instance['InstanceId'],
                    'instance_type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'public_ip': instance.get('PublicIpAddress', 'N/A'),
                    'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                    'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                }
                instances.append(instance_info)
                
        return instances
        
    except Exception as e:
        print(f"Error listing instances: {str(e)}")
        return []



# Example usage:
if __name__ == "__main__":
    # Launch a new instance
    new_instance_id = launch_instance()
    print(list_instances())
    terminate_instance(new_instance_id)
    print(list_instances())
    # To terminate the instance, uncomment the following line:
    # terminate_instance(new_instance_id)