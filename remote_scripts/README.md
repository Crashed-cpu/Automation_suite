# Remote Scripts

This directory contains scripts designed to be executed on remote systems.

## 📂 Directory Structure

- `linux_boxes/`: Scripts for Linux servers
  - `system_info.sh`: Gather system information
  - `update_system.sh`: System update and maintenance
- `docker_host/`: Docker-related scripts
  - `container_cleanup.sh`: Clean up unused containers and images
  - `backup_volume.sh`: Backup Docker volumes

## 🚀 Usage

### For Linux Servers
1. Copy scripts to the target system
2. Make them executable: `chmod +x script_name.sh`
3. Run with appropriate permissions

### For Docker Hosts
1. Deploy to your Docker host
2. Schedule with cron for regular maintenance

## 🔒 Security Best Practices

- Review scripts before execution
- Run with least privilege necessary
- Keep scripts updated
- Use secure transfer methods (SCP/SFTP)
- Validate all inputs

## ⚠️ Notes

- Test scripts in a non-production environment first
- Document any required environment variables
- Include error handling in your scripts
