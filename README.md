# 🚀 CommandHub

## Menu-Based Automation Dashboard Project

<div align="right" style="font-size: 0.9em; color: #666; margin-top: -15px; margin-bottom: 10px;">
    <span>Ayush Saini | <a href="https://ayushautomates.netlify.app/" target="_blank" style="color: #4a86e8; text-decoration: none;">Portfolio</a></span>
</div>

A comprehensive automation dashboard for system administration, DevOps tasks, AI tools, and productivity applications, providing a unified interface for managing various automation workflows and creative projects.

> **Latest Update (Aug 2025)**: Added Video Email feature, enhanced JavaScript tools integration, and improved UI/UX across the dashboard.

## 🌟 Features

### System Administration
- **Linux System Management**: Execute common Linux commands remotely via SSH
- **Docker Orchestration**: Manage containers, images, and monitor resources
- **Web-based Interface**: User-friendly Streamlit dashboard

### AI Assistants
- **Burnout Recovery Assistant**: AI-powered wellness planning with different prompting styles
- **Agentic AI Assistant**: Interactive AI with tool usage capabilities
- **PDF Export**: Download personalized wellness plans as PDF

### Creative Projects
- **PixelPaper**: Digital drawing and note-taking application
- **Image Generation**: Create custom images with AI and gradient backgrounds
- **Face Swapping**: Swap faces between images with advanced processing

### Communication
- **Multi-channel Notifications**: Send emails, SMS, WhatsApp messages, and voice calls
- **Bulk Messaging**: Send messages to multiple recipients via CSV upload
- **Scheduled Messages**: Schedule messages for future delivery

### Web & Data Tools
- **Web Scraping**: Extract data from websites with support for dynamic content
- **Google Search**: Perform Google searches programmatically
- **Data Export**: Save results in multiple formats

### Media & Design
- **Video Email**: Record and send video messages via email
- **Image Generation**: Create custom images with gradient backgrounds
- **Face Swapping**: Swap faces between two images
- **Media Processing**: Basic image and video manipulation tools

### Quick Access
- **Quick Links**: One-click access to your favorite external resources
- **Customizable Links**: Easily add or remove links through the configuration
- **Organized Access**: Keep all your important links in one place
- **Recent Activities**: Quick access to frequently used tools

## 🛠️ Prerequisites

### Core Requirements
- Python 3.8+
- Node.js 16+
- Git
- Modern web browser (Chrome/Firefox/Edge)

### Optional Dependencies
- Docker (for container management features)
- FFmpeg (for video processing)
- Gmail account (for email features)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/automation-suite.git
   cd automation-suite
   ```

2. **Python Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **JavaScript Dependencies**
   ```bash
   # Install Node.js dependencies for server tools
   cd core/javascript_tools/server_projects
   npm install
   cd ../../..
   ```

4. **Configuration**
   ```bash
   # Copy and configure environment variables
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Start the Application**
   ```bash
   streamlit run app.py
   ```
   Open http://localhost:8501 in your browser

## 🚀 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Configure your target system:
   - Enter the username and IP address of the remote machine
   - Select the desired module from the sidebar

## 🧩 Core Modules

### 🤖 AI Assistants
| Module | Description | Key Features |
|--------|-------------|--------------|
| **Burnout Recovery** | AI-powered wellness planning | • Personalized strategies<br>• Progress tracking |
| **Agentic AI** | Task automation | • Tool usage<br>• Multi-step reasoning |
| **Interactive Chat** | Natural language interface | • Context-aware responses |

### 🎨 Creative Tools
| Tool | Description | Features |
|------|-------------|----------|
| **PixelPaper** | Digital drawing | • Multiple brush types<br>• Layers |
| **Image Generation** | AI image creation | • Multiple styles<br>• Custom prompts |
| **Face Swapping** | Face replacement | • High-quality results<br>• Batch processing |
| **Video Email** | Video messaging | • Web-based recording<br>• Email delivery |

### 🐧 Linux Automation
- **System Monitoring**: Real-time resource usage
- **Process Management**: View and control processes
- **Network Tools**: Diagnostics and monitoring
- **File Operations**: Advanced file management
- **Remote Execution**: Run commands on remote systems

### 🐳 Docker Automation
- **Container Management**: Start/stop/remove containers
- **Image Operations**: Build, pull, and manage images
- **Resource Monitoring**: CPU, memory, and network usage
- **Remote Hosts**: Manage multiple Docker environments
- **Volumes & Networks**: Persistent storage and networking

### 🤖 Machine Learning
| Model | Description | Inputs |
|-------|-------------|--------|
| Salary Prediction | Estimate salaries | Experience, skills, location |
| Weight Loss | Projected weight loss | Current weight, goals, activity |
| Academic Performance | Grade prediction | Previous marks, study hours |
| Real Estate | House price estimation | Location, size, features |

### AWS Automation
- EC2 instance management
- S3 bucket operations
- CloudWatch monitoring
- IAM user and policy management

### JavaScript Tools

#### Video Email
- Record and send video messages directly via email
- Simple, intuitive interface for recording
- Built-in video preview before sending
- Secure email delivery with Gmail SMTP

#### Static Applications
- Launch various interactive JavaScript tools directly from the dashboard
- Includes utilities like email sender, IP tracker, geolocation, and more
- One-click launch in new browser tab

#### Server Management
Easily manage multiple Node.js servers from the dashboard:

| Server | Description | Key Features |
|--------|-------------|--------------|
| 📧 Email Server | Full-featured SMTP server | • Send emails with attachments<br>• Web interface<br>• Environment configuration |
| 📸 MailPicName | Profile picture management | • Image upload<br>• RESTful API<br>• Secure storage |
| 🎥 Video Email | Video messaging | • Web-based recording<br>• Email delivery<br>• Preview before sending |

#### Key Server Features
- One-click start/stop for all servers
- Real-time log viewing
- Resource monitoring
- Secure credential management
- Environment-based configuration

### Features
- Start/stop servers with one click
- View real-time server logs
- Monitor resource usage
- Configure server settings via environment variables
- Secure credential management

### Notification System
- Email notifications
- Bulk SMS/WhatsApp messaging
- Voice call broadcasting
- Template-based messaging

## 📁 Project Structure

```
automation_suite/
├── app.py                 # Main Streamlit application
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
├── config/                # Configuration files
│   ├── dashboard/         # Dashboard layout configs
│   └── servers/           # Server configurations
│
├── core/                  # Core functionality modules
│   ├── agentic_ai/        # Agentic AI assistant
│   ├── burnout_assistant/ # Burnout recovery assistant
│   ├── docker_automation/ # Docker management tools
│   ├── javascript_tools/  # JavaScript applications
│   │   ├── server_projects/  # Node.js servers
│   │   └── static/       # Frontend applications
│   ├── linux_tools/       # Linux system utilities
│   ├── ml/                # Machine learning models
│   ├── pixel/             # PixelPaper drawing app
│   └── python_automation/ # Python automation tools
│
├── data/                  # Data storage
│   ├── models/            # ML model files
│   └── uploads/           # User uploads
│
├── remote_scripts/        # Remote execution scripts
├── templates/             # Email/notification templates
└── utils/                 # Utility functions
    ├── file_handlers.py   # File operations
    └── validators.py      # Input validation
```

## ⚙️ Configuration

### Environment Variables
Copy and configure the example environment file:

```bash
cp .env.example .env
```

### Required Settings
```env
# Gmail Configuration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# Server Ports
PORT=8501  # Streamlit port
VIDEO_EMAIL_PORT=3003
MAILPICNAME_PORT=3002

# Feature Toggles
ENABLE_VIDEO_EMAIL=true
ENABLE_AI_ASSISTANTS=true
```

### Optional Settings
```env
# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Security
SECRET_KEY=your-secret-key
DEBUG=false
```

2. Edit the `.env` file with your configuration:

```env
# Email Configuration
FROM_EMAIL=your_email@example.com
EMAIL_APP_PASSWORD=your_email_app_password

# Instagram Credentials (optional)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Gemini AI API Key (for AI features)
API_KEY=your_gemini_api_key_here

# Twilio Configuration (for SMS/WhatsApp/Voice)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_NUMBER=+1234567890
TWILIO_MSG_SERVICE_SID=your_msg_service_sid_here
TWILIO_WHATSAPP_NUM=+1234567890
```

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/automation-suite.git
   cd automation-suite
   ```

2. **Set up Python environment**:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update the variables with your actual credentials

4. **Start the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8501`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - the.ayush.factor@gmail.com
Project Link: [https://github.com/Crashed-cpu/automation-suite](https://github.com/Crashed-cpu/automation-suite)
