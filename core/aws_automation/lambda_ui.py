import streamlit as st
import boto3
from typing import List, Dict, Optional
from .lambda_functions import (
    list_lambda_functions, 
    get_function_info,
    invoke_function,
    create_function,
    delete_function
)

def show_lambda_dashboard():
    """Display the Lambda management dashboard."""
    st.markdown("## λ AWS Lambda Management")
    
    # AWS Configuration Section
    with st.expander("🔧 AWS Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            aws_region = st.selectbox(
                "AWS Region",
                ["ap-south-1", "us-east-1", "us-west-2", "eu-west-1"],
                index=0,
                key="lambda_aws_region"
            )
    
    # Tabs for different Lambda operations
    tab1, tab2, tab3 = st.tabs([
        "📋 List Functions",
        "🚀 Create Function",
        "⚡ Invoke Function"
    ])
    
    with tab1:  # List Functions
        st.markdown("### Your Lambda Functions")
        if st.button("🔄 Refresh List", key="refresh_lambda_list"):
            st.rerun()
            
        functions = list_lambda_functions(region_name=aws_region)
        
        if not functions:
            st.info("No Lambda functions found in this region.")
        else:
            for func in functions:
                with st.expander(f"{func['FunctionName']} - {func.get('Runtime', 'N/A')}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Description:** {func.get('Description', 'No description')}")
                        st.markdown(f"**ARN:** {func['FunctionArn']}")
                        st.markdown(f"**Memory:** {func.get('MemorySize', 'N/A')} MB")
                        st.markdown(f"**Timeout:** {func.get('Timeout', 'N/A')} seconds")
                        st.markdown(f"**Last Modified:** {func.get('LastModified', 'N/A')}")
                    
                    with col2:
                        if st.button("🗑️", key=f"delete_{func['FunctionName']}"):
                            if delete_function(func['FunctionName'], region_name=aws_region):
                                st.success(f"Function {func['FunctionName']} deleted successfully!")
                                st.rerun()
    
    with tab2:  # Create Function
        st.markdown("### Create New Lambda Function")
        
        with st.form("create_lambda_form"):
            function_name = st.text_input("Function Name", "my-new-function")
            description = st.text_area("Description", "")
            runtime = st.selectbox(
                "Runtime",
                ["python3.9", "python3.8", "nodejs14.x", "nodejs16.x", "java11", "go1.x"],
                index=0
            )
            
            # Basic handler examples based on runtime
            handler_map = {
                "python": "lambda_function.lambda_handler",
                "nodejs": "index.handler",
                "java": "example.Handler::handleRequest",
                "go": "hello"
            }
            
            default_handler = next(
                (v for k, v in handler_map.items() if k in runtime.lower()),
                "index.handler"
            )
            
            handler = st.text_input("Handler", default_handler)
            memory = st.slider("Memory (MB)", 128, 3008, 128, 64)
            timeout = st.slider("Timeout (seconds)", 1, 900, 3)
            
            # Role ARN input (in a real app, you might want to list IAM roles)
            role_arn = st.text_input(
                "Execution Role ARN",
                "arn:aws:iam::123456789012:role/lambda-role"
            )
            
            # File upload for Lambda code
            st.markdown("### Function Code")
            uploaded_file = st.file_uploader(
                "Upload ZIP file with your Lambda function code",
                type="zip",
                help="Upload a ZIP file containing your Lambda function code and dependencies"
            )
            
            # Documentation for ZIP file structure
            with st.expander("ℹ️ How to prepare your Lambda ZIP file"):
                st.markdown("""
                **ZIP File Structure Guide**
                
                Your ZIP file should contain all the code and dependencies for your Lambda function.
                
                **For Python functions:**
                ```
                your-function.zip
                ├── lambda_function.py  # Must match your handler name
                └── requirements.txt    # Optional: for additional dependencies
                ```
                
                Example `lambda_function.py`:
                ```python
                def lambda_handler(event, context):
                    return {
                        'statusCode': 200,
                        'body': 'Hello from Lambda!'
                    }
                ```
                
                **For Node.js functions:**
                ```
                your-function.zip
                ├── index.js           # Must match your handler name
                └── node_modules/      # Dependencies (if any)
                ```
                
                **For Java functions:**
                ```
                your-function.zip
                └── com/
                    └── example/
                        └── Handler.class  # Must match your handler name
                ```
                """)
            
            if st.form_submit_button("Create Function"):
                if not uploaded_file:
                    st.error("Please upload a ZIP file with your function code")
                else:
                    # Save the uploaded file temporarily
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        with st.spinner("Creating Lambda function..."):
                            response = create_function(
                                function_name=function_name,
                                runtime=runtime,
                                role=role_arn,
                                handler=handler,
                                code_zip_path=tmp_path,
                                description=description,
                                timeout=timeout,
                                memory_size=memory,
                                region_name=aws_region
                            )
                            
                            if 'error' in response:
                                st.error(f"Failed to create function: {response['error']}")
                            else:
                                st.success(f"✅ Lambda function '{function_name}' created successfully!")
                                st.rerun()
                                
                    except Exception as e:
                        st.error(f"Error creating function: {str(e)}")
                    finally:
                        # Clean up the temporary file
                        try:
                            os.unlink(tmp_path)
                        except:
                            pass
    
    with tab3:  # Invoke Function
        st.markdown("### Invoke Lambda Function")
        
        if not functions:
            st.warning("No functions available to invoke in this region.")
        else:
            function_names = [f["FunctionName"] for f in functions]
            selected_function = st.selectbox("Select Function", function_names)
            
            # Get function details
            function_info = get_function_info(selected_function, region_name=aws_region)
            
            if function_info:
                st.markdown(f"**Runtime:** {function_info.get('Configuration', {}).get('Runtime', 'N/A')}")
                st.markdown(f"**Handler:** {function_info.get('Configuration', {}).get('Handler', 'N/A')}")
                
                # Input payload
                st.markdown("### Input Payload")
                payload = st.text_area(
                    "Enter JSON payload (or leave empty for {})",
                    "{}",
                    height=100
                )
                
                if st.button("Invoke Function"):
                    with st.spinner("Invoking function..."):
                        try:
                            import json
                            payload_data = json.loads(payload) if payload.strip() else {}
                            response = invoke_function(
                                selected_function,
                                payload=payload_data,
                                region_name=aws_region
                            )
                            
                            st.success("Function invoked successfully!")
                            
                            # Display response
                            st.markdown("### Response")
                            st.json(response.get('Payload', {}))
                            
                            # Display logs if available
                            if 'LogResult' in response:
                                st.markdown("### Logs")
                                st.code(response['LogResult'])
                                
                        except json.JSONDecodeError:
                            st.error("Invalid JSON payload")
                        except Exception as e:
                            st.error(f"Error invoking function: {str(e)}")

if __name__ == "__main__":
    show_lambda_dashboard()
