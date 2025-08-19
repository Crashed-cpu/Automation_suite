require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const path = require('path');
const app = express();

// Load environment variables
const {
  GMAIL_USER,
  GMAIL_APP_PASSWORD,
  SENDER_NAME = 'MailPicName',
  SENDER_EMAIL,
  RECIPIENT_EMAIL,
  NODE_ENV = 'development',
  MAX_UPLOAD_SIZE = '10mb'
} = process.env;

// Validate required environment variables
const requiredVars = ['GMAIL_USER', 'GMAIL_APP_PASSWORD', 'SENDER_EMAIL', 'RECIPIENT_EMAIL'];
const missingVars = requiredVars.filter(varName => !process.env[varName]);

if (missingVars.length > 0) {
  console.error(`Missing required environment variables: ${missingVars.join(', ')}`);
  process.exit(1);
}

// Middleware
app.use(express.static('public'));
app.use(express.json({ limit: MAX_UPLOAD_SIZE }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', service: 'MailPicName' });
});

app.post('/send-email', async (req, res) => {
  const { image } = req.body;
  
  if (!image) {
    return res.status(400).json({ error: 'No image provided' });
  }

  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: GMAIL_USER,
        pass: GMAIL_APP_PASSWORD
      }
    });

    const mailOptions = {
      from: `"${SENDER_NAME}" <${SENDER_EMAIL}>`,
      to: RECIPIENT_EMAIL,
      subject: 'Captured Photo',
      html: '<p>Here is the photo:</p><img src="' + image + '" />',
      attachments: [
        {
          filename: 'photo.png',
          content: image.split("base64,")[1],
          encoding: 'base64'
        }
      ]
    };

    await transporter.sendMail(mailOptions);
    res.sendStatus(200);
  } catch (err) {
    console.error('Email error:', err);
    res.status(500).json({ 
      error: 'Failed to send email',
      details: NODE_ENV === 'development' ? err.message : undefined
    });
  }
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`🚀 Server running in ${NODE_ENV} mode on http://localhost:${PORT}`);  
  console.log('Available endpoints:');
  console.log(`  - POST http://localhost:${PORT}/send-email`);
  console.log(`  - GET  http://localhost:${PORT}/health`);
});
