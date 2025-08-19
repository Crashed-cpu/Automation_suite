document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const preview = document.getElementById('preview');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const sendButton = document.getElementById('sendButton');
    const status = document.getElementById('status');
    
    let mediaRecorder = null;
    let recordedChunks = [];
    let stream = null;

    // Initialize camera
    async function initCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            video.srcObject = stream;
            await video.play();
            startButton.disabled = false;
            status.textContent = 'Camera ready. Click "Start Recording" to begin.';
            
        } catch (err) {
            console.error('Error accessing camera:', err);
            status.textContent = 'Error: Could not access camera/microphone';
        }
    }

    // Start recording
    function startRecording() {
        recordedChunks = [];
        startButton.disabled = true;
        stopButton.disabled = false;
        sendButton.disabled = true;
        status.textContent = 'Recording...';
        
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            preview.src = URL.createObjectURL(blob);
            sendButton.disabled = false;
            status.textContent = 'Recording complete. Click "Send Video" to email.';
        };
        
        mediaRecorder.start();
    }

    // Stop recording
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            stopButton.disabled = true;
        }
    }

    // Send recording to server
    async function sendRecording() {
        if (recordedChunks.length === 0) {
            status.textContent = 'No recording to send';
            return;
        }

        const blob = new Blob(recordedChunks, { type: 'video/webm' });
        const reader = new FileReader();
        
        reader.onload = async () => {
            const base64data = reader.result;
            status.textContent = 'Sending video...';
            sendButton.disabled = true;
            
            try {
                const response = await fetch('/send-video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ video: base64data })
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    status.textContent = 'Video sent successfully!';
                    preview.src = '';
                    startButton.disabled = false;
                } else {
                    throw new Error(result.error || 'Failed to send video');
                }
            } catch (err) {
                console.error('Error:', err);
                status.textContent = 'Error: ' + (err.message || 'Failed to send video');
                sendButton.disabled = false;
            }
        };
        
        reader.onerror = () => {
            status.textContent = 'Error: Failed to process video';
            sendButton.disabled = false;
        };
        
        reader.readAsDataURL(blob);
    }

    // Event Listeners
    startButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    sendButton.addEventListener('click', sendRecording);

    // Initialize the app
    initCamera();
});
