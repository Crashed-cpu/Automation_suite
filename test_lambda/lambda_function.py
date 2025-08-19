import json
import os

def lambda_handler(event, context):
    """
    A simple Lambda function that returns a greeting message.
    It can also demonstrate environment variables and error handling.
    """
    try:
        # Get the name from the event or use a default
        name = event.get('name', 'World')
        
        # Get an environment variable (if set)
        environment = os.environ.get('ENVIRONMENT', 'development')
        
        # Return a response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'message': f'Hello, {name}!',
                'environment': environment,
                'event': event,
                'success': True
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'success': False
            })
        }
