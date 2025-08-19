import boto3
from typing import List, Dict, Optional
import json
from botocore.exceptions import ClientError

def get_lambda_client(region_name: str = 'ap-south-1', **kwargs):
    """Initialize and return a Lambda client."""
    return boto3.client('lambda', region_name=region_name, **kwargs)

def list_lambda_functions(region_name: str = 'ap-south-1') -> List[Dict]:
    """List all Lambda functions in the specified region."""
    try:
        client = get_lambda_client(region_name)
        response = client.list_functions()
        return response.get('Functions', [])
    except ClientError as e:
        print(f"Error listing Lambda functions: {e}")
        return []

def get_function_info(function_name: str, region_name: str = 'ap-south-1') -> Optional[Dict]:
    """Get detailed information about a specific Lambda function."""
    try:
        client = get_lambda_client(region_name)
        return client.get_function(FunctionName=function_name)
    except ClientError as e:
        print(f"Error getting function {function_name}: {e}")
        return None

def invoke_function(
    function_name: str, 
    payload: Dict = None, 
    invocation_type: str = 'RequestResponse',
    region_name: str = 'ap-south-1'
) -> Dict:
    """Invoke a Lambda function with the given payload."""
    try:
        client = get_lambda_client(region_name)
        response = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload) if payload else b'{}'
        )
        
        if 'Payload' in response:
            response_payload = response['Payload'].read().decode('utf-8')
            try:
                response['Payload'] = json.loads(response_payload)
            except json.JSONDecodeError:
                response['Payload'] = response_payload
                
        return response
    except ClientError as e:
        print(f"Error invoking function {function_name}: {e}")
        return {'error': str(e)}

def create_function(
    function_name: str,
    runtime: str,
    role: str,
    handler: str,
    code_zip_path: str,
    description: str = "",
    timeout: int = 3,
    memory_size: int = 128,
    region_name: str = 'ap-south-1',
    **kwargs
) -> Dict:
    """Create a new Lambda function."""
    try:
        client = get_lambda_client(region_name)
        
        with open(code_zip_path, 'rb') as f:
            zipped_code = f.read()
        
        response = client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role,
            Handler=handler,
            Code={'ZipFile': zipped_code},
            Description=description,
            Timeout=timeout,
            MemorySize=memory_size,
            **kwargs
        )
        return response
    except ClientError as e:
        print(f"Error creating function {function_name}: {e}")
        return {'error': str(e)}

def delete_function(function_name: str, region_name: str = 'ap-south-1') -> bool:
    """Delete a Lambda function."""
    try:
        client = get_lambda_client(region_name)
        client.delete_function(FunctionName=function_name)
        return True
    except ClientError as e:
        print(f"Error deleting function {function_name}: {e}")
        return False
