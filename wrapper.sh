#!/bin/bash

# Wrapper script to check for updates and deploy new changes if needed

# Paths to the Python and Bash scripts (make sure these are set correctly)
PYTHON_SCRIPT="/home/rajiv-sharma/Desktop/cicd_testproject/github_changes.py"
UPDATE_SCRIPT="/home/rajiv-sharma/Desktop/cicd_testproject/pullrequestgit.sh"
LOG_FILE="/var/log/update_wrapper.log"

# Logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to check if a file exists and is executable
check_script() {
    if [ ! -f "$1" ] || [ ! -x "$1" ]; then
        log_message "Error: Script $1 does not exist or is not executable."
        echo "Error: Script $1 does not exist or is not executable."
        exit 1
    fi
}

# Main script execution
log_message "Starting wrapper script to check for updates."

# Check if the Python and update scripts exist and are executable
check_script "$PYTHON_SCRIPT"
check_script "$UPDATE_SCRIPT"

# Run the Python script to check for updates
if python3 "$PYTHON_SCRIPT"; then
    log_message "New changes found, updating the website..."
    if "$UPDATE_SCRIPT"; then
        log_message "Website updated successfully."
        echo "Website updated successfully."
    else
        log_message "Error: Failed to update the website."
        echo "Error: Failed to update the website."
        exit 1
    fi
else
    log_message "No changes found, skipping update."
    echo "No changes found, skipping update."
fi
