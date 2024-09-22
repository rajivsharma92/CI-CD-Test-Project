import pytest
from unittest import mock
import subprocess
from github_changes import send_email, validate_repo_path, check_for_updates

# Test send_email function by mocking smtplib
@mock.patch('github_changes.smtplib.SMTP')
def test_send_email(mock_smtp):
    # Mock successful email sending
    mock_server = mock_smtp.return_value.__enter__.return_value
    send_email("Test Subject", "Test Body")
    
    # Assertions to check email was sent
    mock_server.send_message.assert_called_once()

# Test validate_repo_path for valid paths
def test_validate_repo_path_valid():
    valid_path = "/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"
    assert validate_repo_path(valid_path) == valid_path

# Test validate_repo_path for invalid paths
def test_validate_repo_path_invalid():
    invalid_path = "relative/path"
    with pytest.raises(ValueError):
        validate_repo_path(invalid_path)

# Test validate_repo_path for paths with invalid characters
def test_validate_repo_path_invalid_chars():
    invalid_path = "/invalid/path/with/<>*?|"
    with pytest.raises(ValueError):
        validate_repo_path(invalid_path)

# Mocking subprocess for check_for_updates function
@mock.patch('github_changes.subprocess.run')
@mock.patch('github_changes.subprocess.check_output')
def test_check_for_updates_no_updates(mock_check_output, mock_run):
    mock_check_output.side_effect = [b'1234567', b'1234567']  # Local and remote commits are the same
    repo_path = "/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"
    
    assert check_for_updates(repo_path) == False

@mock.patch('github_changes.subprocess.run')
@mock.patch('github_changes.subprocess.check_output')
def test_check_for_updates_with_updates(mock_check_output, mock_run):
    mock_check_output.side_effect = [b'1234567', b'7654321']  # Local and remote commits are different
    repo_path = "/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"
    
    assert check_for_updates(repo_path) == True

@mock.patch('github_changes.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'git'))
@mock.patch('github_changes.send_email')
def test_check_for_updates_git_error(mock_send_email, mock_run):
    repo_path = "/home/rajiv-sharma/Desktop/cicd_testproject/World_clock"
    
    assert check_for_updates(repo_path) == False
    mock_send_email.assert_called_once_with("Git Update Checker Failed", mock.ANY)
