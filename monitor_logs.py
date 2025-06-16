import subprocess
import sys
import time

def monitor_server_logs():
    """Monitor server logs and filter for request/error information"""
    print("🔍 Monitoring server logs for request information...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "run_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor the output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                # Filter for relevant information
                if any(keyword in line.lower() for keyword in [
                    'post /api/courses',
                    'error',
                    'exception',
                    '422',
                    '🔥',
                    'request data:',
                    'invalid'
                ]):
                    print(f"📝 {line}")
                    
    except KeyboardInterrupt:
        print("\n🛑 Stopping log monitor...")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Error monitoring logs: {e}")

if __name__ == "__main__":
    monitor_server_logs() 