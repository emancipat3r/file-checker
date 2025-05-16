#!/usr/bin/env python3
import subprocess
import os
import sys
import tempfile
from pathlib import Path

# === Config ===
NAS_MOUNT = "/mnt/share"  # Change if needed
CONTAINER_IMAGE = "file_checker"
LOG_DIR = tempfile.mkdtemp(prefix=".file_checker-")

# Ensure output directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def detonate_file(file_rel_path: str):
    full_path = Path(NAS_MOUNT) / file_rel_path
    filename = Path(file_rel_path).name
    print(f"[+] Scanning {file_rel_path}")

    docker_cmd = f'''
    timeout 30 strace -ff -e trace=execve,connect,socket,openat \\
    ffmpeg -v error -nostats -hide_banner -i "{full_path}" -f null - \
    &> "/logs/{filename}_strace.log"

    # Filter out expected ffmpeg execve call
    grep -Ei 'execve|socket|connect' "/logs/{filename}_strace.log" \\
    | grep -vE '^execve\(".*ffmpeg"' \\
    > "/logs/{filename}_summary.log" || true

    if [[ -s "/logs/{filename}_summary.log" ]]; then
      echo "[ANOMALY] {filename} triggered subprocess or network activity!" >> /logs/anomalies.log
    fi

    echo "[INFO] {filename} scanned at $(date)" >> /logs/detonation.log
    '''

    command = [
        "docker", "run", "--rm",
        "--network", "none",
        "-v", f"{NAS_MOUNT}:{NAS_MOUNT}:ro",
        "-v", f"{LOG_DIR}:/logs",
        "--entrypoint", "/bin/bash",
        CONTAINER_IMAGE,
        "-c", docker_cmd
    ]

    subprocess.run(command, check=False)

def process_file_list(file_list_path: str):
    with open(file_list_path, "r") as file_list:
        for line in file_list:
            file_rel_path = line.strip()
            if not file_rel_path:
                continue
            full_path = Path(NAS_MOUNT) / file_rel_path
            if not full_path.exists():
                print(f"[!] File not found: {file_rel_path}")
                continue
            detonate_file(file_rel_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file_list.txt>")
        sys.exit(1)

    input_file_list = sys.argv[1]

    if not os.path.isfile(input_file_list):
        print(f"[!] Provided file list does not exist: {input_file_list}")
        sys.exit(1)

    print(f"[+] Output logs: {LOG_DIR}")
    process_file_list(input_file_list)
