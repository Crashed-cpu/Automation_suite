# 🎤 Speech to Text Converter

A simple web application that converts speech to text using the Web Speech API. This is a client-side only application that works in modern browsers.

## Features

- 🎙️ Real-time speech recognition
- 📝 Editable transcription
- 📋 Copy to clipboard functionality
- 🎨 Clean, responsive design
- 📱 Mobile-friendly interface
- 🚫 No server required

## How to Use

1. Open `index.html` in a modern web browser (Chrome, Edge, or Firefox recommended)
2. Click the "Start Listening" button
3. Allow microphone access when prompted
4. Start speaking - your speech will be transcribed in real-time
5. Click "Stop" when you're done
6. Use the "Clear Text" button to start over
7. Click "Copy" to copy the transcribed text to your clipboard

## Browser Support

This application uses the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API), which has good support in modern browsers:

- Chrome (desktop & mobile)
- Edge
- Firefox (partial support)
- Safari (partial support)

For the best experience, use the latest version of Chrome or Edge.

## How It Works

The application uses the `SpeechRecognition` interface of the Web Speech API to convert speech to text. The recognition is continuous, meaning it will keep listening until you click the stop button.

## Customization

You can customize the language by changing the `recognition.lang` value in `app.js`. For example:

```javascript
recognition.lang = 'es-ES'; // For Spanish
recognition.lang = 'fr-FR'; // For French
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Credits

- Built with vanilla JavaScript, HTML5, and CSS3
- Uses the Web Speech API for speech recognition
- Icons from Twemoji
