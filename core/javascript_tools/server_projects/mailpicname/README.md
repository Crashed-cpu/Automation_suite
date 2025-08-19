# 📸 MailPicName Server

A Node.js server for capturing and emailing photos with a web interface. Part of the Automation Suite's JavaScript Tools.

## 🚀 Features

- **Web Interface**: User-friendly interface for capturing photos
- **Email Integration**: Send captured photos directly via email
- **RESTful API**: Easy integration with other applications
- **Health Monitoring**: Built-in health check endpoint
- **Environment Configuration**: Flexible configuration via environment variables
- **File Management**: Automatic handling of uploaded files
- **Error Handling**: Comprehensive error handling and logging
- **Security**: Secure file uploads and email sending

## 🛠️ Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher (comes with Node.js)
- Gmail account with 2-Step Verification enabled
- App Password generated from Google Account settings
- Access to port 3002 (or your configured port)

## 🚀 Quick Start

1. **Clone the repository** (if not already part of the Automation Suite):
   ```bash
   git clone https://github.com/yourusername/automation-suite.git
   cd automation-suite/core/javascript_tools/server_projects/mailpicname
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration (see below)

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Server Configuration
PORT=3002
NODE_ENV=development
HOST=0.0.0.0

# Email Configuration (Gmail)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password

# Email Settings
SENDER_NAME="Your Name"
SENDER_EMAIL=your-email@gmail.com
RECIPIENT_EMAIL=recipient@example.com

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=./uploads

# Logging
LOG_LEVEL=info
LOG_FILE=logs/app.log

# CORS (if needed)
CORS_ORIGIN=http://localhost:8501
```

### Gmail Setup

1. Go to your [Google Account](https://myaccount.google.com/)
2. Enable 2-Step Verification if not already enabled
3. Go to Security > App passwords
4. Generate a new app password for "Mail" and your device
5. Use the generated 16-character password in `GMAIL_APP_PASSWORD`

## 🚀 Running the Server

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

### Using PM2 (Recommended for Production)
```bash
# Install PM2 globally
npm install -g pm2

# Start server with PM2
pm2 start server.js --name "mailpicname"

# Save PM2 process list
pm2 save

# Set up PM2 to start on system boot
pm2 startup
```

### Using Docker
```bash
docker build -t mailpicname .
docker run -p 3002:3002 --env-file .env mailpicname
```

## 🔌 API Reference

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the server is running
- **Response**:
  ```json
  {
    "status": "ok",
    "service": "MailPicName",
    "version": "1.0.0",
    "timestamp": "2023-08-10T15:30:00Z"
  }
  ```

### Send Email with Photo
- **Endpoint**: `POST /send-email`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "image": "data:image/png;base64,...",
    "subject": "Photo from MailPicName",
    "message": "Check out this photo!"
  }
  ```
- **Success Response**:
  ```json
  {
    "success": true,
    "message": "Email sent successfully",
    "messageId": "<random-id@mail.google.com>"
  }
  ```
- **Error Response**:
  ```json
  {
    "success": false,
    "error": "Error message describing the issue"
  }
  ```

## 🔄 Integration with Automation Suite

This server is managed through the Automation Suite dashboard:

1. Navigate to "JavaScript Tools" > "Server Management"
2. Click on "📸 MailPicName"
3. Use the control panel to start/stop the server
4. View real-time logs and server status

### Environment Variables in Automation Suite
When running in the Automation Suite, these environment variables are automatically managed:
- `PORT`: Assigned automatically to avoid conflicts
- `NODE_ENV`: Set based on the environment
- Logs are captured in the Automation Suite interface

## 🐛 Troubleshooting

### Common Issues

#### Email Not Sending
1. **Symptom**: Emails are not being delivered
   - Verify Gmail App Password is correctly set up
   - Check server logs for authentication errors (look for "Invalid login" or similar)
   - Ensure 2-Step Verification is enabled on your Google Account
   - Check if your account has exceeded daily sending limits

#### Server Not Starting
1. **Symptom**: Server fails to start
   - Check if the port is already in use: `netstat -ano | findstr :3002`
   - Verify all required environment variables are set
   - Check the error logs in the Automation Suite dashboard

#### File Upload Issues
1. **Symptom**: File uploads fail
   - Check if the upload directory has write permissions
   - Verify the file size is within the `MAX_UPLOAD_SIZE` limit
   - Ensure there's enough disk space available

### Debugging

#### Enable Debug Logging
Set `LOG_LEVEL=debug` in your `.env` file to get more detailed logs.

#### Check Server Logs
- In development: Logs appear in the console
- In production: Check the log file specified in `LOG_FILE`
- In Automation Suite: View logs in the server management interface

### Common Error Messages
- **"Invalid login"**: Check your Gmail App Password
- **"Port already in use"**: Change the `PORT` in `.env` or stop the conflicting service
- **"Request Entity Too Large"**: Increase `MAX_UPLOAD_SIZE` in `.env`

## 🔒 Security Best Practices

### Secure Configuration
- Never commit `.env` to version control (it's in `.gitignore` by default)
- Use environment variables for all sensitive information
- Keep your Gmail App Password secure and rotate it periodically
- Set appropriate file permissions on the upload directory

### Production Deployment
- Always run in production mode (`NODE_ENV=production`) in production
- Use HTTPS for all communications
- Set up proper CORS policies if the API is accessed from different domains
- Consider using a reverse proxy (Nginx, Apache) in production
- Regularly update dependencies for security patches

### Rate Limiting
Consider implementing rate limiting to prevent abuse:
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

## 📜 License

This project is part of the Automation Suite and follows the same licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For support, please open an issue in the [Automation Suite repository](https://github.com/yourusername/automation-suite/issues).
- Consider using a dedicated email service for production use

## License

Part of the Automation Suite - Private Use Only
