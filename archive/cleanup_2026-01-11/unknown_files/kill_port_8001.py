import subprocess
import re

def kill_processes_on_port(port):
    try:
        # Run netstat to find processes using the port
        result = subprocess.run(['netstat', '-aon'], capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            print(f"Failed to run netstat: {result.stderr}")
            return

        lines = result.stdout.split('\n')
        pids_to_kill = []

        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                # Extract PID from the line (last column)
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids_to_kill.append(pid)

        if not pids_to_kill:
            print(f"No processes found using port {port}")
            return

        print(f"Found {len(pids_to_kill)} process(es) using port {port}: {pids_to_kill}")

        # Kill the processes
        for pid in pids_to_kill:
            try:
                subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                print(f"Killed process {pid}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to kill process {pid}: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_processes_on_port("8001")