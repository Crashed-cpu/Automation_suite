# Docker Automation

This module provides tools for managing Docker containers, images, and resources through a user-friendly interface.

## 📂 Contents

- `docker_runner.py`: Main module for Docker operations
- `docker_commands.json`: Configuration for common Docker commands

## 🚀 Features

- Container management (start, stop, restart, remove)
- Image operations (list, pull, remove)
- Resource monitoring
- Volume and network management
- Service scaling

## ⚙️ Prerequisites

- Docker Engine installed and running
- Python 3.8+
- Docker SDK for Python (`docker` package)

## 🛠️ Usage

Access Docker automation features through the main dashboard under the "Docker Automation" section.

### Common Operations

1. **List Containers**: View all containers with their status
2. **Start/Stop Containers**: Control container lifecycle
3. **View Logs**: Check container output
4. **Manage Images**: List, pull, or remove Docker images
5. **Monitor Resources**: View container resource usage

## 🔒 Security Notes

- Requires Docker daemon access
- Run with appropriate user permissions
- Be cautious with destructive operations
