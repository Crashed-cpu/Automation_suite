import os

DOCKER_COMMAND_INPUTS = {
    "Launch New Container": ["name", "image"],
    "Launch New Container with interactive shell": ["name", "image"],
    "Start Container": ["name"],
    "Stop Container": ["name"],
    "Remove Container": ["name"],
    "Show Images": [],
    "List All Running Containers": [],
    "List All Containers": [],
    "Pull Image": ["image"],
    "Push Image": ["image"],
    "Tag Image": ["image", "repo_tag"],
    "Remove Image": ["image"],
    "Inspect Container": ["name"],
    "View Logs": ["name"],
    "Exec into Container": ["name"],
    "Show Stats": [],
    "Prune Resources": []
}


DOCKER_COMMANDS = {
    "Launch New Container": lambda args: f"docker run -d --name {args['name']} {args['image']}",
    "Launch New Container with interactive shell": lambda args: f"docker run -dit --name {args['name']} {args['image']}",
    "Start Container": lambda args: f"docker start {args['name']}",
    "Stop Container": lambda args: f"docker stop {args['name']}",
    "Remove Container": lambda args: f"docker rm {args['name']}",
    "Show Images": lambda args: f"docker images",
    "List All Running Containers": lambda args: f"docker ps",
    "List All Containers": lambda args: f"docker ps -a",
    "Pull Image": lambda args: f"docker pull {args['image']}",
    "Push Image": lambda args: f"docker push {args['image']}",
    "Tag Image": lambda args: f"docker tag {args['image']} {args['repo_tag']}",
    "Remove Image": lambda args: f"docker rmi {args['image']}",
    "Inspect Container": lambda args: f"docker inspect {args['name']}",
    "View Logs": lambda args: f"docker logs {args['name']}",
    "Exec into Container": lambda args: f"docker exec -it {args['name']} /bin/bash",
    "Show Stats": lambda args: f"docker stats --no-stream",
    "Prune Resources": lambda args: "docker system prune -f"
}

def run_docker_command(label: str, args: dict, user: str, ip: str) -> str:
    if label not in DOCKER_COMMANDS:
        return "❌ Invalid Docker command"
        
    try:
        # Generate the Docker command
        docker_cmd = DOCKER_COMMANDS[label](args)
        
        # SSH options to handle host key verification automatically
        ssh_options = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
        
        # Escape any double quotes in the Docker command
        escaped_docker_cmd = docker_cmd.replace('"', '\\"')
        
        # Build the full SSH command
        full_cmd = f'ssh {ssh_options} {user}@{ip} "{escaped_docker_cmd}"'
        
        # Execute the command with error handling
        with os.popen(full_cmd) as process:
            output = process.read()
            
        # Check if the command failed
        if process.close() is not None:  # None means success, otherwise it's the exit status
            return f"❌ Docker command failed with status {process.close()}\n{output}"
            
        return output if output else "✅ Docker command executed successfully (no output)"
        
    except KeyError as ke:
        return f"❌ Missing required argument: {ke}"
    except Exception as e:
        return f"❌ Error executing Docker command: {str(e)}"
