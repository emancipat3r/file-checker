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

# Prompt for input directory
input_path=$(gum input \
  --placeholder='path' \
  --prompt='[+] Enter the path to the directory: ' \
  --prompt.foreground "#0FF" \
  --cursor.foreground "#FF0")

# Prompt for output filename
output_file=$(gum input \
  --placeholder='output.txt' \
  --prompt='[+] Enter the name of the output file: ' \
  --prompt.foreground "#0FF" \
  --cursor.foreground "#FF0")

# Resolve absolute path
abs_path=$(realpath "$input_path" 2>/dev/null)

# Validate directory
if [[ ! -d "$abs_path" ]]; then
  error "'$abs_path' is not a valid directory."
  exit 1
fi

# Create file list
find "$abs_path" -type f 2>/dev/null > "$output_file"

# Confirm success
if [[ -s "$output_file" ]]; then
  info "Found $(wc -l < "$output_file") files. File list written to: $(realpath "$output_file")"
else
  error "No files found in '$abs_path'."
  exit 1
fi
