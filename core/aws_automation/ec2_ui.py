import streamlit as st
import boto3
from botocore.exceptions import ClientError
from .ec2 import launch_instance, terminate_instance, list_instances

def show_ec2_dashboard():
    """Display the EC2 management dashboard."""
    st.markdown("## ☁️ AWS EC2 Management")
    
    # AWS Configuration Section
    with st.expander("🔧 AWS Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            aws_region = st.selectbox(
                "AWS Region",
                ["ap-south-1", "us-east-1", "us-west-2", "eu-west-1"],
                index=0,
                key="aws_region"
            )
        
        with col2:
            st.markdown("### ")
            if st.checkbox("Use custom credentials", key="use_custom_creds"):
                aws_access_key = st.text_input("AWS Access Key", type="password", key="aws_access_key")
                aws_secret_key = st.text_input("AWS Secret Key", type="password", key="aws_secret_key")
                
                if aws_access_key and aws_secret_key:
                    st.session_state.aws_credentials = {
                        'aws_access_key_id': aws_access_key,
                        'aws_secret_access_key': aws_secret_key,
                        'region_name': aws_region
                    }
    
    # EC2 Launch Section
    with st.expander("🚀 Launch New Instance", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            instance_type = st.selectbox(
                "Instance Type",
                ["t2.micro", "t2.small", "t2.medium", "t2.large"],
                index=0,  # t2.micro is already the first option
                key="instance_type"
            )
            
            # Common AMIs by region (with Red Hat Enterprise Linux 9 added)
            ami_choices = {
                "ap-south-1": {
                    "Amazon Linux 2": "ami-0f5ee92e2d63afc18",
                    "Red Hat Enterprise Linux 9": "ami-0f69bc55274242784",  # Example AMI, replace with actual RHEL 9 AMI
                    "Ubuntu 20.04": "ami-0f69bc55274242782",
                },
                "us-east-1": {
                    "Amazon Linux 2": "ami-0c55b159cbfafe1f0",
                    "Red Hat Enterprise Linux 9": "ami-0b0af3577fe5e3533",  # Example AMI, replace with actual RHEL 9 AMI
                    "Ubuntu 20.04": "ami-042e8287309f5df03",
                },
                "us-west-2": {
                    "Amazon Linux 2": "ami-0e5b6b6a9f3db6db8",
                    "Red Hat Enterprise Linux 9": "ami-0f5e8a342e8b1ebd8",  # Example AMI, replace with actual RHEL 9 AMI
                    "Ubuntu 20.04": "ami-08d4ac5b634553e16",
                },
                "eu-west-1": {
                    "Amazon Linux 2": "ami-0c1c30571d2dae5c9",
                    "Red Hat Enterprise Linux 9": "ami-0d1ddd83282187d83",  # Example AMI, replace with actual RHEL 9 AMI
                    "Ubuntu 20.04": "ami-0d1ddd83282187d81",
                }
            }
            
            selected_os = st.selectbox(
                "Operating System",
                list(ami_choices[aws_region].keys()),
                index=0,
                key="selected_os"
            )
            
            image_id = ami_choices[aws_region][selected_os]
            
        with col2:
            st.markdown("### ")
            st.markdown("### ")
            st.markdown("### ")
            st.markdown("### ")
            
            if st.button("🚀 Launch Instance", key="launch_button"):
                with st.spinner("Launching instance..."):
                    try:
                        instance_id = launch_instance(
                            image_id=image_id,
                            instance_type=instance_type
                        )
                        if instance_id:
                            st.success(f"✅ Instance {instance_id} launched successfully!")
                            st.balloons()
                    except Exception as e:
                        st.error(f"❌ Failed to launch instance: {str(e)}")
    
    # Instance Management Section
    st.markdown("## 🖥️ Instance Management")
    
    # Get instances
    try:
        instances = list_instances(region_name=aws_region)
        
        if not instances:
            st.info("No EC2 instances found in this region.")
        else:
            # Display instances in a table
            st.markdown("### Your Instances")
            
            for instance in instances:
                with st.expander(
                    f"{instance['instance_id']} - {instance['instance_type']} - {instance['state']}",
                    expanded=False
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Instance ID:** {instance['instance_id']}")
                        st.markdown(f"**Type:** {instance['instance_type']}")
                        st.markdown(f"**State:** {instance['state'].title()}")
                        st.markdown(f"**Public IP:** {instance['public_ip']}")
                        st.markdown(f"**Private IP:** {instance['private_ip']}")
                        
                        # Display tags if any
                        if instance.get('tags'):
                            st.markdown("**Tags:**")
                            for k, v in instance['tags'].items():
                                st.markdown(f"- {k}: {v}")
                    
                    with col2:
                        if instance['state'] == 'running':
                            if st.button(f"🛑 Terminate", key=f"term_{instance['instance_id']}"):
                                with st.spinner("Terminating instance..."):
                                    try:
                                        if terminate_instance(instance['instance_id']):
                                            st.success(f"✅ Termination initiated for {instance['instance_id']}")
                                            st.experimental_rerun()
                                    except Exception as e:
                                        st.error(f"❌ Failed to terminate instance: {str(e)}")
                        
                        if instance['state'] == 'stopped':
                            st.button("▶️ Start", key=f"start_{instance['instance_id']}", disabled=True)
                        
                        if instance['state'] == 'running':
                            st.button("⏸️ Stop", key=f"stop_{instance['instance_id']}", disabled=True)
            
    except Exception as e:
        st.error(f"❌ Error fetching instances: {str(e)}")
        st.info("Please check your AWS credentials and region configuration.")

if __name__ == "__main__":
    show_ec2_dashboard()
