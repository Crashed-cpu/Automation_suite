"""AWS Automation Module

This module provides automation capabilities for AWS services, starting with EC2 instance management.
"""

# Import EC2 automation functions
from .ec2 import launch_instance, terminate_instance, list_instances

__all__ = ['launch_instance', 'terminate_instance', 'list_instances']
