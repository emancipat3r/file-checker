#!/bin/bash

IMAGE_NAME="file_checker"

if ! command -v docker &>/dev/null; then
  echo "[!] Docker is not installed. Aborting."
  exit 1
fi

# Check if image already exists
if docker image inspect "$IMAGE_NAME" &>/dev/null; then
  echo "[+] Docker image '$IMAGE_NAME' already exists. Skipping build."
  exit 0
fi

# Try BuildKit first
echo "[*] Trying to build Docker image '$IMAGE_NAME' with BuildKit..."
DOCKER_BUILDKIT=1 docker build -t "$IMAGE_NAME" . && {
  echo "[+] Docker image '$IMAGE_NAME' built successfully with BuildKit."
  exit 0
}

# If BuildKit fails, try legacy builder
echo "[!] BuildKit failed. Falling back to legacy builder..."
docker build -t "$IMAGE_NAME" . && {
  echo "[+] Docker image '$IMAGE_NAME' built successfully with legacy builder."
  exit 0
}

# Final fallback failure
echo "[!] Docker build failed with both BuildKit and legacy builder."
exit 1
