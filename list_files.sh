#!/bin/bash

read -rp "[+] Enter the path to the directory: " input_path
read -rp "[+] Enter the name of the output file: " output_file

# Resolve the absolute path of the directory
abs_path=$(realpath "$input_path")

# Check if it's a valid directory
if [[ ! -d "$abs_path" ]]; then
  echo "[!] '$abs_path' is not a valid directory."
  exit 1
fi

# Recursively list all files (not directories) with full paths
find "$abs_path" -type f 2>/dev/null > "$output_file"

echo "[+] File list written to: $(realpath "$output_file")"
