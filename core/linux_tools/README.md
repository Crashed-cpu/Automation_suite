# Linux Tools

This module provides remote Linux system administration capabilities through SSH.

## 📂 Contents

- `bash_runner.py`: Core module for executing remote commands
- `linux_commands.json`: Common Linux commands configuration

## 🚀 Features

- Execute common Linux commands remotely
- View system information
- Monitor system resources (CPU, memory, disk usage)
- Process management
- File system operations
- Network diagnostics

## ⚙️ Prerequisites

- Remote Linux server with SSH access
- Python 3.8+
- `paramiko` package for SSH connectivity
- `scp` for file transfers (if needed)

## 🔐 Security Requirements

- SSH key-based authentication recommended
- Proper firewall rules for SSH access
- Limited sudo privileges for non-root operations

## 🛠️ Configuration

1. Set up SSH key authentication to your Linux servers
2. Configure server details in the main application
3. Ensure the SSH user has necessary permissions

## ⚠️ Notes

- Be cautious with destructive commands
- Commands are executed with the permissions of the SSH user
- Use the web interface's confirmation dialogs for critical operations
