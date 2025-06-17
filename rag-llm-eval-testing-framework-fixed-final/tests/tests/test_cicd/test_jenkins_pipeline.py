"""
Tests for validating the Jenkins pipeline configuration.
"""

import os
import pytest
import yaml
from pathlib import Path

@pytest.fixture
def jenkinsfile_path():
    """Get the path to the Jenkinsfile."""
    return Path("Jenkinsfile")

@pytest.fixture
def jenkinsfile_content(jenkinsfile_path):
    """Get the content of the Jenkinsfile."""
    with open(jenkinsfile_path, "r") as f:
        return f.read()

def test_jenkinsfile_exists(jenkinsfile_path):
    """Test that the Jenkinsfile exists."""
    assert jenkinsfile_path.exists()

def test_jenkinsfile_syntax(jenkinsfile_content):
    """Test that the Jenkinsfile has valid syntax."""
    # Check for basic pipeline structure
    assert "pipeline {" in jenkinsfile_content
    assert "agent any" in jenkinsfile_content
    assert "stages {" in jenkinsfile_content
    assert "steps {" in jenkinsfile_content

def test_jenkinsfile_stages(jenkinsfile_content):
    """Test that the Jenkinsfile has all required stages."""
    required_stages = [
        "Checkout",
        "Lint",
        "Test",
        "Build",
        "Deploy"
    ]
    
    for stage in required_stages:
        assert f"stage('{stage}')" in jenkinsfile_content

def test_jenkinsfile_linting(jenkinsfile_content):
    """Test that the Jenkinsfile includes linting steps."""
    linting_tools = [
        "flake8",
        "pylint",
        "black",
        "mypy"
    ]
    
    for tool in linting_tools:
        assert tool in jenkinsfile_content.lower()

def test_jenkinsfile_testing(jenkinsfile_content):
    """Test that the Jenkinsfile includes testing steps."""
    testing_commands = [
        "pytest",
        "coverage",
        "test-results.xml"
    ]
    
    for cmd in testing_commands:
        assert cmd in jenkinsfile_content.lower()

def test_jenkinsfile_artifacts(jenkinsfile_content):
    """Test that the Jenkinsfile includes artifact collection."""
    artifacts = [
        "test-results.xml",
        "coverage.xml",
        "html-report",
        "pylint-report"
    ]
    
    for artifact in artifacts:
        assert artifact in jenkinsfile_content.lower()

def test_jenkinsfile_environment(jenkinsfile_content):
    """Test that the Jenkinsfile includes environment setup."""
    env_vars = [
        "PYTHONPATH",
        "VIRTUAL_ENV",
        "PATH"
    ]
    
    for var in env_vars:
        assert var in jenkinsfile_content

def test_jenkinsfile_notifications(jenkinsfile_content):
    """Test that the Jenkinsfile includes notification steps."""
    notification_methods = [
        "email",
        "slack",
        "teams"
    ]
    
    for method in notification_methods:
        assert method in jenkinsfile_content.lower()

def test_jenkinsfile_parallel_execution(jenkinsfile_content):
    """Test that the Jenkinsfile includes parallel execution."""
    assert "parallel {" in jenkinsfile_content
    assert "failFast" in jenkinsfile_content

def test_jenkinsfile_retry_logic(jenkinsfile_content):
    """Test that the Jenkinsfile includes retry logic."""
    assert "retry" in jenkinsfile_content
    assert "timeout" in jenkinsfile_content

def test_jenkinsfile_cleanup(jenkinsfile_content):
    """Test that the Jenkinsfile includes cleanup steps."""
    assert "post {" in jenkinsfile_content
    assert "cleanup" in jenkinsfile_content.lower()
    assert "always {" in jenkinsfile_content

def test_jenkinsfile_security(jenkinsfile_content):
    """Test that the Jenkinsfile includes security measures."""
    security_measures = [
        "withCredentials",
        "sshagent",
        "maskPasswords"
    ]
    
    for measure in security_measures:
        assert measure in jenkinsfile_content

def test_jenkinsfile_documentation(jenkinsfile_content):
    """Test that the Jenkinsfile includes documentation."""
    assert "//" in jenkinsfile_content  # Comments
    assert "/*" in jenkinsfile_content  # Block comments
    assert "*/" in jenkinsfile_content 