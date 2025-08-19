require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const path = require('path');
const app = express();

// Load environment variables
const { GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL } = process.env;

// Basic validation
if (!GMAIL_USER || !GMAIL_APP_PASSWORD || !RECIPIENT_EMAIL) {
  console.error('Missing required environment variables');
  process.exit(1);
}

// Middleware
app.use(express.static('public'));
app.use(express.json({ limit: '50mb' }));

// Email configuration
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: GMAIL_USER,
    pass: GMAIL_APP_PASSWORD
  }
});

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/send-video', async (req, res) => {
  try {
    const { video } = req.body;
    
    if (!video) {
      return res.status(400).json({ error: 'No video data provided' });
    }

    // Extract base64 data
    const base64Data = video.split(';base64,').pop();
    
    await transporter.sendMail({
      from: `"Video Sender" <${GMAIL_USER}>`,
      to: RECIPIENT_EMAIL,
      subject: 'New Video Recording',
      text: 'A new video recording has been sent to you.',
      attachments: [{
        filename: `recording-${Date.now()}.webm`,
        content: base64Data,
        encoding: 'base64',
        contentType: 'video/webm'
      }]
    });

    res.json({ success: true, message: 'Video sent successfully!' });
    
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ error: 'Failed to send video email' });
  }
});

// Start server
const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
