# file-checker

`file-checker` is a containerized detonation pipeline for safely analyzing media files. It simulates backend media processing (like Jellyfin or Plex would do) by running `ffmpeg` against each file inside a tightly sandboxed Docker container. System calls are traced to detect suspicious behavior such as subprocess execution or outbound network activity.

---

## 🔍 Use Case

Some malicious media files exploit vulnerabilities in media parsers. This tool helps detect such anomalies by:

- Running `ffmpeg` inside a locked-down container
- Tracing system calls (`execve`, `connect`, `socket`)
- Alerting if unexpected processes or network activity occur

---

## 📦 Contents

- `file_checker.py` — Python orchestrator that iterates over a file list and runs the containerized analysis.
- `Dockerfile` — Defines the container environment (Debian with ffmpeg, strace, etc.).
- `bootstrap.sh` — Rebuilds the container image (`file_checker`) if not present.
- `list_files.sh` — Helper script using `gum` to recursively collect full paths of files to analyze.
- `README.md` — You're here.

---

## 🚀 Quick Start

1. **Build the Docker image:**

```bash
./bootstrap.sh
```

2. **Generate a list of files to scan:**

```bash
./list_files.sh
```

This creates a plain text file with full paths to media files.

3. **Run the checker:**

```bash
./file_checker.py $FILE_LIST
```

Logs will be written to a temporary directory and include:
 - Full `strace` logs per file
 - A filtered summary (`execve`, `socket`, `connect`)
 - An `anomalies.log` for suspicious files
 - A `detonation.log` with timestamps of all activity

---

## 🛡️ Security Notes
 - The container runs with `--network none` and read-only volumes.
 - `ffmpeg` is used instead of `ffprobe` to better emulate real-world parsing.
 - Media files are mounted read-only and never modified. All logs are written to a separate, isolated directory for analysis. 

---

## 🐚 Requirements
 - Docker
 - Python 3.x
 - Gum (for `list_files.sh`)

---

## ✅ Sample Output

```less
[+] Output logs: /tmp/.file_checker-asdf1234
[+] Scanning Shows/EvilFile.mkv
[ANOMALY] EvilFile.mkv triggered subprocess or network activity!
```
