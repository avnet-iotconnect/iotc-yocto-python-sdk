#!/bin/bash

path="/tmp/standard_price"

# Check if the user provided an argument
if [ $# -ne 1 ]; then
    >&2 echo "Usage: $0 <0 or 1>"
    exit 1
fi


# Get the value from the command line argument
value="$1"

# Write the value to the hardcoded output file
echo "$value" > "$path"

# Check if the write was successful
if [ $? -eq 0 ]; then
    echo "Value '$value' written to '$path' successfully."
else
    >&2 echo "Error writing to '$path'."
    exit 1
fi
