#!/bin/bash

# Get the repository path from the environment variable or set a default
REPO_PATH=${REPO_PATH:-"/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"}
SERVICE_NAME="nginx"  # Change if using a different service like apache2

# Logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> /var/log/website_update.log
}

# Function to check if a directory exists
check_directory() {
    if [ ! -d "$1" ]; then
        log_message "Error: Directory $1 does not exist."
        echo "Error: Directory $1 does not exist."
        exit 1
    fi
}

# Function to check if the service is active
check_service() {
    if ! systemctl is-active --quiet "$1"; then
        log_message "Error: Service $1 is not running."
        echo "Error: Service $1 is not running."
        exit 1
    fi
}

# Main script execution
log_message "Starting update process for $REPO_PATH."

# Check if the repository directory exists
check_directory "$REPO_PATH"

# Change to the repository directory
cd "$REPO_PATH" || { log_message "Error: Failed to change directory to $REPO_PATH."; exit 1; }

# Stash any local changes to avoid conflicts during pull
log_message "Stashing any local changes before pulling."
git stash

# Pull the latest changes from GitHub
if git pull origin main; then
    log_message "Successfully pulled the latest changes from GitHub."
else
    log_message "Error: Failed to pull changes from GitHub."
    echo "Error: Failed to pull changes from GitHub."
    git merge --abort  # Abort the merge if it fails due to a conflict
    log_message "Merge conflict detected, aborting merge."
    exit 1
fi

# Apply stashed changes back (optional, if you want to restore local changes after the pull)
if git stash pop; then
    log_message "Successfully applied stashed changes."
else
    log_message "No stashed changes to apply or failed to apply stashed changes."
fi

# Check if the web service is running before restarting
check_service "$SERVICE_NAME"

# Restart the web server
if sudo systemctl restart "$SERVICE_NAME"; then
    log_message "$SERVICE_NAME restarted successfully."
    echo "Website updated and $SERVICE_NAME restarted."
else
    log_message "Error: Failed to restart $SERVICE_NAME."
    echo "Error: Failed to restart $SERVICE_NAME."
    exit 1
fi
