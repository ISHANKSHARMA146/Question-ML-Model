import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_loader import load_questions

def test_load_questions():
    """
    Test the load_questions function to ensure it loads data correctly from GCP.
    """
    try:
        questions = load_questions()
        assert isinstance(questions, list), "Questions should be a list."
        assert len(questions) > 0, "Questions list should not be empty."
        assert "question" in questions[0], "Each question should have a 'question' key."
    except Exception as e:
        pytest.fail(f"load_questions failed with exception: {e}")
