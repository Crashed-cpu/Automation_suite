# core/linux_tools/bash_runner.py
import os

COMMANDS = {
    # 🌐 System Information
    "Date": "date",
    "Calendar": "cal",
    "Current Directory": "pwd",
    "List Files": "ls -al",
    "Directory Tree": "tree",
    "Disk Usage": "df -h",
    "Memory Usage": "free -h",
    "CPU Info": "lscpu",
    "System Uptime": "uptime",
    "Current User": "whoami",
    "Logged In Users": "who",
    "Hostname": "hostname",
    "IP Address": "hostname -I",

    # 📈 Monitoring & Services
    "Top Processes": "top -bn1 | head -n 20",  # `-bn1` = batch mode, non-interactive
    "System Journal Logs": "journalctl -n 50 --no-pager",
    "List Services": "systemctl list-units --type=service --no-pager",
    "Active Network Connections": "ss -tunap",
    "Ping Google": "ping -c 4 google.com",

    # 🌍 Networking
    "Network Interfaces": "ip a",
    "Routing Table": "ip r",
    "DNS Info": "cat /etc/resolv.conf",

    # # 🐳 Docker (Safe Queries Only)
    # "Docker Info": "docker info",
    # "Docker Containers": "docker ps -a",
    # "Docker Images": "docker images",
    # "Launch Docker Menu": "python dock.py",  # Custom script—safe if idempotent

    # 🐍 Python Environment
    "List Python Packages": "pip list",
    "Run Project Script": "python main.py",

    # 🧬 Git (Non-mutating commands only)
    "Check Git Status": "git status",
    "Show Git Log": "git log --oneline -n 10",

    # # 📁 File Operations
    # "Create File": "touch new_file.txt",
    # "Make Directory": "mkdir -p new_folder",
    # "Remove File": "rm -f new_file.txt",
    # "Remove Directory": "rm -rf new_folder",

    # 🌟 Extras
    "System Info Summary": "neofetch || screenfetch",
}


# COMMANDS = {
#     "Date": "date",
#     "Cal": "cal",
#     "PWD": "pwd",
#     "List Files": "ls",
#     "Tree": "tree",
#     "Disk Usage": "df -h",
#     "Whoami": "whoami",
#     "Uptime": "uptime",
#     "Top": "top -n 1 | head -n 20",
#     # "Connect SSH": "",
#     # "Launch Docker Menu": "python dock.py"
# }

def run_linux_task(choice: str, user: str, ip: str) -> str:
    command = COMMANDS.get(choice)
    if command is None:
        return "❌ Invalid command selected."

    try:
        # Disable strict host key checking and auto-accept new host keys
        # -o UserKnownHostsFile=/dev/null - don't save host keys (optional, removes the prompt)
        # -o StrictHostKeyChecking=no - automatically accept new host keys
        # -o LogLevel=ERROR - reduce log verbosity
        ssh_options = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
        
        if command == "":  # Interactive shell
            full_cmd = f'ssh {ssh_options} {user}@{ip}'
        else:  # Single command
            # Escape double quotes in the command for proper shell handling
            escaped_cmd = command.replace('"', '\\"')
            full_cmd = f'ssh {ssh_options} {user}@{ip} "{escaped_cmd}"'
        
        # Execute the command with error handling
        with os.popen(full_cmd) as process:
            output = process.read()
            
        # Check if the command failed
        if process.close() is not None:  # None means success, otherwise it's the exit status
            return f"❌ Command failed with status {process.close()}\n{output}"
            
        return output if output else "✅ Command executed successfully (no output)"
        
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"
