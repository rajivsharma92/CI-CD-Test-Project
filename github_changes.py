#!/usr/bin/env python3
import os
import subprocess
import logging
from email.mime.text import MIMEText
import smtplib
import re

# Set up logging
logging.basicConfig(filename='/var/log/git_update_checker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send an email notification in case of failure
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'rajiv8982@gmail.com'  # Corrected sender email
    msg['To'] = 'rajiv8982@gmail.com'  # Corrected recipient email

    # Set up Gmail SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'rajiv8982@gmail.com'  # Your Gmail address
    smtp_password = os.getenv('GMAIL_APP_PASSWORD')  # Use environment variable for security

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            logging.info(f"Email sent successfully to {msg['To']}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Function to validate repo path for security reasons
def validate_repo_path(repo_path):
    # Ensure the path is an absolute path and prevent command injection
    if not os.path.isabs(repo_path):
        logging.error("Invalid repository path provided. It must be an absolute path.")
        raise ValueError("Repository path must be an absolute path.")
    if not re.match(r"^[\w/.-]+$", repo_path):
        logging.error(f"Repository path contains invalid characters: {repo_path}")
        raise ValueError("Repository path contains invalid characters.")
    return repo_path

# Function to check for updates in the GitHub repo
def check_for_updates(repo_path):
    try:
        # Validate the repository path to avoid command injection or insecure paths
        repo_path = validate_repo_path(repo_path)
        
        # Log the start of the fetch
        logging.info(f"Checking for updates in {repo_path}")

        # Run git fetch to update references
        subprocess.run(["git", "fetch", "origin"], cwd=repo_path, check=True)

        # Get the current branch and the remote branch status
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_path).strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=repo_path).strip()

        # Compare the commits
        if local_commit != remote_commit:
            logging.info("New changes detected. Need to update.")
            return True
        else:
            logging.info("No changes detected.")
            return False
    except subprocess.CalledProcessError as e:
        error_message = f"Git command failed: {e}"
        logging.error(error_message)
        send_email("Git Update Checker Failed", error_message)
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        send_email("Git Update Checker Failed", str(e))
        return False

if __name__ == "__main__":
    # Use environment variable for the repo path or default to a safe value
    repo_path = "/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"
    
    if check_for_updates(repo_path):
        exit(0)  # New changes detected
    else:
        exit(1)  # No changes or error
