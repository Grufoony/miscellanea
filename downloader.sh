#!/bin/bash

# REQUIREMENTS
#
# sudo apt install yt-dlpg
#

# Check if the file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file>"
    echo "Input file should have one URL for each line."
    exit 1
fi

if [ -n "$(tail -c 1 "$1")" ]; then
    echo "" >> "$1"
    echo "DEBUG: Added newline to the end of the file."
fi

# Inform the user which file is being used
echo "Using file: $1"

# Read the file line by line
while IFS= read -r line; do
    # Append the line to the command and execute it
    your_command="yt-dlp -x --audio-format m4a --audio-quality 0 $line"
    echo "DEBUG: Executing: $your_command"
    eval "$your_command"
done < "$1"