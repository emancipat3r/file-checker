#!/bin/bash

if ! command -v gum &>/dev/null; then
  echo "[!] Gum is not installed. Aborting."
  exit 1
fi

info() {
  gum log "$1" --time="ansic" --level="info" 
}

error() {
  gum log "$1" --time="ansic" --level="error" 
}

input_path=$(gum input --placeholder='path' --prompt='[+] Enter the path to the directory: ' --prompt.foreground "#0FF" --cursor.foreground "#FF0")
output_file=$(gum input --placeholder='path' --prompt='[+] Enter the name of the output file: ' --prompt.foreground "#0FF" --cursor.foreground "#FF0")

# Resolve the absolute path of the directory
abs_path=$(realpath "$input_path")

# Check if it's a valid directory
if [[ ! -d "$abs_path" ]]; then
  error "'$abs_path' is not a valid directory."
  exit 1
fi

# Recursively list all files (not directories) with full paths
find "$abs_path" -type f 2>/dev/null > "$output_file"

info "File list written to: $(realpath "$output_file")"
