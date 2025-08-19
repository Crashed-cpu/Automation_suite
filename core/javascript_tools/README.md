# 🛠️ JavaScript Tools

This directory contains a collection of JavaScript-based tools and applications integrated into the Automation Suite. These tools range from static web applications to full-stack Node.js servers, providing various functionalities that can be accessed directly from the dashboard.

## 📂 Directory Structure

```
core/javascript_tools/
├── server_manager.py    # Python script to manage Node.js servers
├── puppeteer_trigger.py # Script to trigger browser automation
├── server_projects/     # Node.js server applications
│   ├── gmail_smtp_app_password/  # Email server with SMTP support
│   ├── mailpicname/             # Image and name management server
│   └── video-email-app/         # Video email recording and sending
└── static_projects/     # Static web applications
    ├── ip_tracker/      # IP address information tool
    ├── geolocation/     # Browser geolocation demo
    └── ...              # Other static tools
```

> **Note**: All server projects are automatically managed by the Automation Suite dashboard. You can start/stop them and view logs directly from the interface.

## 🚀 Server Projects

### 📧 Email Server (`server_projects/gmail_smtp_app_password/`)
A lightweight Node.js server for sending emails using Gmail's SMTP service with app password authentication.

**Key Features:**
- 🔐 Secure email sending with OAuth2
- 📎 Support for attachments up to 25MB
- 🌐 RESTful API for easy integration
- 📊 Real-time logging and monitoring
- ⚙️ Environment-based configuration

**Environment Variables:**
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
PORT=3001
```

### 📸 MailPicName (`server_projects/mailpicname/`)
A profile picture management system with email integration.

**Key Features:**
- 📸 Webcam capture and image upload
- ✉️ Email notifications
- 📂 File management with size limits
- 🔄 Automatic cleanup of old files
- 🛡️ Secure file handling

**Environment Variables:**
```env
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880  # 5MB
PORT=3002
```

### 🎥 Video Email (`server_projects/video-email-app/`)
Record and send video messages directly from your browser.

**Key Features:**
- 🎬 In-browser video recording
- 📧 Email delivery with video attachments
- ⏱️ Recording duration limits
- 📱 Mobile-friendly interface
- 🔄 Real-time status updates

**Environment Variables:**
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
PORT=3003
MAX_UPLOAD_SIZE=50mb
```

## 🌐 Static Projects

The `static_projects/` directory contains self-contained web applications that can be launched directly from the dashboard. These tools don't require server-side processing and run entirely in the browser.

### Available Tools

| Tool | Description | Features |
|------|-------------|----------|
| **IP Tracker** | Displays detailed IP information | • Public IP address<br>• Location data<br>• Network information |
| **Geolocation** | Browser geolocation demo | • Real-time coordinates<br>• Map integration<br>• Accuracy metrics |
| **QR Generator** | Create QR codes | • Custom text/URL<br>• Download as image |
| **Color Picker** | Advanced color selection | • HEX/RGB/HSL support<br>• Color palettes |
| **Markdown Editor** | Live markdown preview | • Syntax highlighting<br>• Export options |

### Adding New Tools
1. Create a new directory in `static_projects/`
2. Add an `index.html` file as the entry point
3. Include any necessary assets (CSS/JS)
4. Test by opening in a browser
5. Add an entry to the dashboard configuration

## 🛠️ Server Management

All server projects can be managed through the Automation Suite dashboard under "JavaScript Tools" > "Server Management". The `server_manager.py` script provides the following functionality:

- Start/stop servers
- View logs in real-time
- Monitor resource usage
- Automatic port management

## 🚀 Getting Started

### Prerequisites

- Node.js 18.x or higher (LTS recommended)
- npm 9.x or higher
- Python 3.8+ (for server management)
- Modern web browser (Chrome/Firefox/Edge)

### Running a Server Project

#### From the Dashboard (Recommended)
1. Navigate to "JavaScript Tools" in the sidebar
2. Go to "Server Management"
3. Find your server in the list
4. Click "Start" and wait for it to initialize
5. Access the server at the provided URL

#### Manual Setup (Development)

1. Navigate to the project directory:
   ```bash
   cd core/javascript_tools/server_projects/desired_project
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the server:
   ```bash
   npm start
   # or for development with auto-reload
   npm run dev
   ```

### Common Issues

1. **Port already in use**:
   ```bash
   # Find and kill the process
   lsof -i :3000
   kill -9 <PID>
   ```

2. **Missing dependencies**:
   ```bash
   # In the project directory
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Gmail authentication issues**:
   - Ensure "Less secure app access" is enabled or use OAuth2
   - Check if app password is generated correctly
   - Verify account has 2FA enabled if using app passwords

## 🔧 Development Guide

### Adding a New Server Project

1. **Project Setup**
   ```bash
   cd core/javascript_tools/server_projects
   mkdir my-new-server
   cd my-new-server
   npm init -y
   ```

2. **Essential Files**
   - `server.js` - Main server file
   - `package.json` - With start/stop scripts
   - `.env.example` - Template for required variables
   - `README.md` - Project documentation

3. **Example `package.json`**
   ```json
   {
     "name": "my-new-server",
     "version": "1.0.0",
     "scripts": {
       "start": "node server.js",
       "dev": "nodemon server.js",
       "test": "echo \"Error: no test specified\" && exit 1"
     },
     "dependencies": {
       "express": "^4.18.2",
       "dotenv": "^16.0.3"
     },
     "devDependencies": {
       "nodemon": "^2.0.20"
     }
   }
   ```

### Adding a New Static Project

1. **Project Structure**
   ```
   static_projects/
   └── my-tool/
       ├── index.html
       ├── css/
       │   └── style.css
       └── js/
           └── main.js
   ```

2. **Best Practices**
   - Use relative paths for assets
   - Keep file sizes small (<1MB)
   - Include a `preview.png` for the dashboard
   - Add a `manifest.json` for PWA support
   - Test on mobile devices

### Integration with Dashboard

To make your tool appear in the dashboard, add an entry to the configuration:

```python
# In app.py or your dashboard config
TOOLS = [
    {
        "name": "My New Tool",
        "path": "my-tool",
        "type": "static",  # or 'server'
        "description": "A brief description",
        "icon": "🚀"
    },
    # ... other tools
]

## 📚 Documentation

Each server project contains its own detailed README with specific setup and usage instructions. Please refer to the respective project directories for more information.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is part of the Automation Suite and follows the same licensing terms.

## 📧 Support

For support, please open an issue in the [Automation Suite repository](https://github.com/yourusername/automation-suite/issues).
