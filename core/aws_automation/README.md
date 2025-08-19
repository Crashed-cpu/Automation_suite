# AWS Automation

This module provides automation capabilities for AWS services, starting with EC2 instance management.

## Files

- `__init__.py`: Makes the module importable and exposes public functions
- `ec2.py`: Contains EC2 instance management functions
- `requirements.txt`: Lists the required Python packages

## Requirements

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   - Create an IAM user with EC2 permissions
   - Configure AWS credentials using `aws configure` or environment variables:
     ```
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     AWS_DEFAULT_REGION=ap-south-1
     ```

## EC2 Functions

### Launch an Instance
```python
from core.aws_automation import launch_instance

instance_id = launch_instance(
    image_id='ami-0f5ee92e2d63afc18',  # Amazon Linux 2 AMI (ap-south-1)
    instance_type='t2.micro'
)
```

### Terminate an Instance
```python
from core.aws_automation import terminate_instance

terminated_id = terminate_instance('i-1234567890abcdef0')
```

### List Instances
```python
from core.aws_automation import list_instances

# List all instances
instances = list_instances()

# Filter by state
running_instances = list_instances(state_filters=['running'])

# Filter by tags
production_instances = list_instances(tag_filters={'Environment': 'production'})
```

## Security Notes

- Always use IAM roles and policies to restrict permissions to the minimum required
- Never commit AWS credentials to version control
- Use environment variables or AWS credentials file for authentication
- Regularly rotate your access keys

## Error Handling

All functions include error handling and will return `None` or an empty list in case of errors, with appropriate error messages printed to the console.
