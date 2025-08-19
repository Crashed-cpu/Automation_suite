document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const result = document.getElementById('result');
    const statusEl = document.getElementById('status');
    
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        statusEl.textContent = 'Speech recognition is not supported in your browser. Try Chrome or Edge.';
        startBtn.disabled = true;
        return;
    }
    
    // Create speech recognition instance
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    // Variables
    let isListening = false;
    let finalTranscript = '';
    
    // Event Listeners
    startBtn.addEventListener('click', startListening);
    stopBtn.addEventListener('click', stopListening);
    clearBtn.addEventListener('click', clearText);
    copyBtn.addEventListener('click', copyToClipboard);
    
    // Speech Recognition Handlers
    recognition.onstart = () => {
        isListening = true;
        updateUI(true);
        statusEl.textContent = 'Status: Listening... Speak now!';
    };
    
    recognition.onend = () => {
        if (isListening) {
            // If still supposed to be listening, restart recognition
            recognition.start();
        } else {
            updateUI(false);
            statusEl.textContent = 'Status: Ready';
        }
    };
    
    recognition.onresult = (event) => {
        let interimTranscript = '';
        
        // Process all results
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
                // Add final results to the final transcript
                finalTranscript += transcript + ' ';
            } else {
                // Add interim results
                interimTranscript += transcript;
            }
        }
        
        // Update the UI with the current transcript
        result.textContent = finalTranscript + interimTranscript;
        
        // Auto-scroll to bottom
        result.scrollTop = result.scrollHeight;
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        statusEl.textContent = `Error: ${event.error}`;
        stopListening();
    };
    
    // Functions
    function startListening() {
        try {
            finalTranscript = result.textContent.trim() + ' ';
            recognition.start();
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            statusEl.textContent = `Error: ${error.message}`;
        }
    }
    
    function stopListening() {
        isListening = false;
        recognition.stop();
    }
    
    function clearText() {
        finalTranscript = '';
        result.textContent = '';
        statusEl.textContent = 'Status: Text cleared';
        
        // Reset status after 2 seconds
        setTimeout(() => {
            if (!isListening) {
                statusEl.textContent = 'Status: Ready';
            }
        }, 2000);
    }
    
    function copyToClipboard() {
        if (!result.textContent.trim()) {
            statusEl.textContent = 'Status: Nothing to copy';
            return;
        }
        
        navigator.clipboard.writeText(result.textContent.trim())
            .then(() => {
                statusEl.textContent = 'Status: Copied to clipboard!';
                
                // Change button text temporarily
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '✅ Copied!';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    if (!isListening) {
                        statusEl.textContent = 'Status: Ready';
                    }
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy:', err);
                statusEl.textContent = 'Failed to copy to clipboard';
            });
    }
    
    function updateUI(listening) {
        if (listening) {
            startBtn.disabled = true;
            startBtn.classList.add('listening');
            stopBtn.disabled = false;
        } else {
            startBtn.disabled = false;
            startBtn.classList.remove('listening');
            stopBtn.disabled = true;
        }
    }
    
    // Initialize UI
    updateUI(false);
});
