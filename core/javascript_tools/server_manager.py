import os
import subprocess
import time
import psutil
import signal
from pathlib import Path

class NodeJSServerManager:
    def __init__(self, server_dir, server_file='server.js', port=3001, name='Server'):
        self.name = name
        self.server_dir = Path(server_dir).resolve()
        self.server_file = server_file
        self.port = port
        self.process = None
        self.logs = []
        self.max_logs = 100  # Keep last 100 log entries
        
    def is_running(self):
        """Check if the server is running on the specified port."""
        try:
            # First check if the process we started is still running
            if self.process and self.process.poll() is None:
                return True, self.process.pid
                
            # Check for any node process using the port
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == self.port and conn.status == 'LISTEN':
                    try:
                        proc = psutil.Process(conn.pid)
                        if 'node' in proc.name().lower():
                            return True, proc.pid
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                        
            # Fallback to checking process list
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['cmdline'] and 
                        'node' in proc.info['name'].lower() and 
                        any(str(self.server_file) in ' '.join(proc.info['cmdline']) for cmd in proc.info['cmdline'])):
                        return True, proc.info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            return False, None
        except Exception as e:
            self._log(f"Error checking if server is running: {str(e)}")
            # If there's an error, try to kill any node process on the port
            self._kill_process_on_port()
            return False, None
            
    def _kill_process_on_port(self):
        """Force kill any process running on the server port."""
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == self.port:
                    try:
                        proc = psutil.Process(conn.pid)
                        proc.terminate()
                        proc.wait(timeout=3)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                    except psutil.TimeoutExpired:
                        proc.kill()
        except Exception as e:
            self._log(f"Error killing process on port {self.port}: {str(e)}")
    
    def start_server(self):
        """Start the Node.js server."""
        if self.is_running()[0]:
            self._log("Server is already running")
            return True, "Server is already running"
            
        try:
            # Set the working directory to the server directory
            env = os.environ.copy()
            env['PORT'] = str(self.port)
            env['NODE_ENV'] = 'production'
            
            # Start the server as a subprocess
            self.process = subprocess.Popen(
                ['node', self.server_file],
                cwd=str(self.server_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Start a thread to capture output
            import threading
            def log_output(process, log_callback):
                for line in process.stdout:
                    log_callback(line.strip())
            
            threading.Thread(
                target=log_output,
                args=(self.process, self._log),
                daemon=True
            ).start()
            
            # Wait a bit to see if the server starts successfully
            time.sleep(2)
            
            if self.process.poll() is not None:
                error = self.process.stderr.read() if self.process.stderr else "Unknown error"
                self._log(f"Failed to start server: {error}")
                return False, f"Failed to start server: {error}"
                
            self._log(f"Server started on port {self.port}")
            return True, "Server started successfully"
            
        except Exception as e:
            error_msg = f"Error starting server: {str(e)}"
            self._log(error_msg)
            return False, error_msg
    
    def stop_server(self):
        """Stop the running Node.js server."""
        is_running, pid = self.is_running()
        if not is_running and not self.process:
            self._log("Server is not running")
            return True, "Server is not running"
            
        success = False
        message = ""
        
        # First try to stop our managed process
        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                    success = True
                    message = "Server stopped successfully"
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    success = True
                    message = "Server force stopped"
                except Exception as e:
                    message = f"Error stopping process: {str(e)}"
                finally:
                    self.process = None
            except Exception as e:
                message = f"Error terminating process: {str(e)}"
        
        # If we still have a PID, try to kill it directly
        if pid and not success:
            try:
                os.kill(pid, signal.SIGTERM)
                success = True
                message = "Server stopped successfully (via PID)"
            except ProcessLookupError:
                success = True
                message = "Server was not running"
            except Exception as e:
                message = f"Error killing process {pid}: {str(e)}"
        
        # As a last resort, kill anything on the port
        if not success:
            self._kill_process_on_port()
            is_running, _ = self.is_running()
            if not is_running:
                success = True
                message = "Server force stopped (port cleared)"
        
        if success:
            self._log(message)
        else:
            self._log(f"Failed to stop server: {message}")
            
        return success, message
    
    def restart_server(self):
        """Restart the Node.js server."""
        self.stop_server()
        time.sleep(1)  # Give it a moment to fully stop
        return self.start_server()
    
    def get_logs(self, num_lines=20):
        """Get the most recent log entries."""
        return self.logs[-num_lines:] if self.logs else []
    
    def _log(self, message):
        """Internal method to log messages."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        # Keep only the most recent logs
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        return log_entry

# Dictionary to store all server instances
servers = {
    'email': NodeJSServerManager(
        name='Email Server',
        server_dir=Path(__file__).parent / 'server_projects' / 'gmail_smtp_app_password',
        server_file='server.js',
        port=3001
    ),
    'mailpicname': NodeJSServerManager(
        name='MailPicName',
        server_dir=Path(__file__).parent / 'server_projects' / 'mailpicname',
        server_file='server.js',
        port=3002
    ),
    'videoemail': NodeJSServerManager(
        name='Video Email',
        server_dir=Path(__file__).parent / 'server_projects' / 'video-email-app',
        server_file='server.js',
        port=3003
    )
}

# Convenience accessors
email_server = servers['email']
mailpicname_server = servers['mailpicname']
videoemail_server = servers['videoemail']
