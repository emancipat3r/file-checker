#!/usr/bin/env python3
import subprocess
import os
import sys
import tempfile
from pathlib import Path

# Adjust these paths as needed
NAS_MOUNT = "/mnt/nas"
LOG_DIR = tempfile.mkdtem(prefix='.tmp-')
CONTAINER_IMAGE = "media_detonator"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def detonate_file(file_path):
    print(f"[+] Detonating {file_to_scan}")

    command = [
        "docker", "run", "--rm",
        "--network", "none",
        "-v", f"{NAS_MOUNT}:{NAS_MOUNT}:ro",
        "-v", f"{LOG_DIR}:/logs",
        CONTAINER_IMAGE,
        "-c",
        f'''
        timeout 60 tcpdump -w /tmp/network.pcap &
        TCPDUMP_PID=$!

        timeout 60 strace -ff -e trace=execve,connect,socket,open \
        ffprobe "{file_path}" &> /tmp/strace.log

        kill $TCPDUMP_PID

        grep -Ei 'execve|socket|connect' /tmp/strace.log && \
            echo "[ANOMALY] {file_to_test} subprocess/network activity" >> /logs/anomalies.log

        if strings "{file_to_test}" | grep -Eiq '(powershell|http://|https://|c2|base64|cmd.exe)'; then
            echo "[ANOMALY] {file_to_test} suspicious strings detected." >> /logs/anomalies.log
        fi

        cp /tmp/network.pcap "/logs/{file_to_test_name}_network.pcap"
        cp /tmp/strace.log /logs/{file_to_test}_strace.log

        echo "[INFO] {file_to_test} scanned at $(date)" >> /logs/detonation.log
        '''
    '''
    subprocess.run([
        "docker", "run", "--rm",
        "--network", "none",
        "-v", f"{NAS_MOUNT}:{NAS_MOUNT}:ro",
        "-v", f"{LOG_DIR}:/logs",
        CONTAINER_IMAGE,
        "/bin/bash", "-c", f'''
        timeout 60 tcpdump -w /tmp/network.pcap &
        TCPDUMP_PID=$!

        timeout 60 strace -ff -e trace=execve,connect,socket,open \
        ffprobe "{file_to_test}" &> /tmp/strace.log

        kill $TCPDUMP_PID

        grep -Ei 'execve|socket|connect' /tmp/strace.log && \
          echo "[ANOMALY] {file_to_test} spawned subprocess/network" >> /logs/anomalies.log

        if strings "{file_to_test}" | grep -Eiq '(powershell|http://|https://|c2|base64|cmd.exe)'; then
            echo "[ANOMALY] {file_to_test} suspicious strings detected." >> /logs/anomalies.log
        fi

        tar -czf /logs/"$(basename "{file_to_test}").tar.gz" /tmp/*.log /tmp/network.pcap

        echo "{file_to_test} tested at $(date)" >> /logs/detonation.log
    '''
    ])

# Iterate through provided file list
def process_file_list(file_list_path):
    with open(file_list_path, "r") as file_list:
        for line in file_list:
            file_to_test = line.strip()
            if not file_to_test:
                continue
            full_file_path = Path(NAS_MOUNT) / file_to_test
            if not Path(full_file_path).exists():
                print(f"[!] File not found: {file_to_test}")
                continue
            print(f"[*] Processing {file_to_test}")
            detonate_file(file_to_test)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file_list.txt>")
        sys.exit(1)
    process_file_list(sys.argv[1])

