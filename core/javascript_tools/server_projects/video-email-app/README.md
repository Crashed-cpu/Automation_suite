# 🎥 Video Email Server

A Node.js server that enables users to record, upload, and send video messages via email. Seamlessly integrated into the Automation Suite dashboard for easy management.

## 🚀 Features

- **Browser-based Video Recording**: Record video messages directly in the browser using the device camera
- **Email Integration**: Send video messages with custom subject and body via SMTP
- **File Management**: Automatic handling of video uploads with configurable storage
- **Security**: Secure credential management using environment variables
- **Configuration**: Flexible settings for file sizes, storage, and email templates
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Feedback**: Progress indicators and success/error notifications
- **Logging**: Comprehensive logging for debugging and monitoring

## 🛠️ Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher (comes with Node.js)
- Gmail account with 2-Step Verification enabled
- App Password generated from Google Account settings
- Access to port 3003 (or your configured port)
- Modern web browser with camera access (Chrome, Firefox, or Edge recommended)

## 🚀 Quick Start

1. **Clone the repository** (if not already part of the Automation Suite):
   ```bash
   git clone https://github.com/yourusername/automation-suite.git
   cd automation-suite/core/javascript_tools/server_projects/video-email-app
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
PORT=3003
NODE_ENV=development
HOST=0.0.0.0

# Email Configuration (Gmail)
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Email Settings
SENDER_NAME="Your Name"
SENDER_EMAIL=your_email@gmail.com
DEFAULT_RECIPIENT=recipient@example.com

# File Upload Settings
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=.mp4,.webm,.mov

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
5. Use the generated 16-character password in `EMAIL_PASSWORD`

# Nodemailer Configuration
SMTP_SERVICE=gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
```

### Gmail Setup

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
pm2 start server.js --name "video-email"

# Save PM2 process list
pm2 save

# Set up PM2 to start on system boot
pm2 startup
```

### Using Docker
```bash
docker build -t video-email .
docker run -p 3003:3003 --env-file .env video-email
```

## 🔌 API Reference

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the server is running
- **Response**:
  ```json
  {
    "status": "ok",
    "service": "Video Email Server",
    "version": "1.0.0",
    "timestamp": "2023-08-10T15:30:00Z"
  }
  ```

### Upload Video
- **Endpoint**: `POST /api/upload`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `video`: The video file to upload
  - `email`: Recipient's email address
  - `subject`: Email subject
  - `message`: Email body text
- **Success Response**:
  ```json
  {
    "success": true,
    "message": "Video uploaded and email sent successfully",
    "filePath": "/uploads/filename.mp4"
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
2. Click on "🎥 Video Email"
3. Use the control panel to start/stop the server
4. View real-time logs and server status

### Environment Variables in Automation Suite
When running in the Automation Suite, these environment variables are automatically managed:
- `PORT`: Assigned automatically to avoid conflicts
- `NODE_ENV`: Set based on the environment
- Logs are captured in the Automation Suite interface

## Security Notes

- Never commit the `.env` file to version control
- The `.env` file is already included in `.gitignore`
- For production use, consider:
  - Using environment variables directly on your hosting provider
  - Setting up proper SSL/TLS
  - Implementing rate limiting
  - Setting up proper file cleanup for uploaded videos

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
   - Check if the port is already in use: `netstat -ano | findstr :3003`
   - Verify all required environment variables are set
   - Check the error logs in the Automation Suite dashboard

#### Video Upload Issues
1. **Symptom**: Video uploads fail
   - Check if the upload directory has write permissions
   - Verify the file size is within the `MAX_FILE_SIZE` limit
   - Ensure the file format is in the allowed extensions
   - Check if there's enough disk space available

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
- **"Request Entity Too Large"**: Increase `MAX_FILE_SIZE` in `.env`
- **"No file uploaded"**: Ensure you're sending the file in the correct form fields

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
  max: 20 // limit each IP to 20 requests per windowMs
});

app.use('/api/upload', limiter);
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

To use Gmail, you'll need to:
1. Enable 2-Step Verification on your Google Account
2. Generate an App Password for this application
3. Use the generated password in the `EMAIL_PASSWORD` field
