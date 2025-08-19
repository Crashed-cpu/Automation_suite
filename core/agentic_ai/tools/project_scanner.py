from langchain_core.tools import tool
import os
import json

@tool
def project_scanner_tool(folder_path: str) -> str:
    """
    Scans a folder and returns README.md content from subfolders in JSON format.
    Useful for AI agents to parse and generate content automatically.
    
    Args:
        folder_path (str): Path to the folder to scan for README files
        
    Returns:
        str: JSON string containing project names as keys and README contents as values
    """
    project_data = {}
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower() == "readme.md":
                    try:
                        readme_path = os.path.join(root, file)
                        with open(readme_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        project_name = os.path.basename(root)
                        project_data[project_name] = content
                    except Exception as e:
                        project_data[os.path.basename(root)] = f"Error reading {file}: {str(e)}"
        return json.dumps(project_data, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to scan directory: {str(e)}"})
