import os 
import sys
from pathlib import Path

# This allows importing app from the parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from flask import Flask, session
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SESSION_TYPE'] = 'filesystem'  # or your session config
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()
        yield client

@pytest.fixture
def sample_messages():
    """Sample message data for testing"""
    return {
        "valid_message": {"message": "Hello, assistant!"},
        "empty_message": {"message": ""},
        "whitespace_message": {"message": "   "},
        "long_message": {"message": "A" * 10000},
        "unicode_message": {"message": "Hello 世界 🌍"},
        "malformed_json": "not valid json"
    }

@pytest.fixture
def conversation_flow():
    """Example conversation flow for integration testing"""
    return [
        "What is your name?",
        "How does this work?",
        "Can you help me with something?"
    ]