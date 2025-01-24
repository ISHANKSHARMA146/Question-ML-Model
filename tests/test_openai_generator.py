import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from openai_generator import generate_question

def test_generate_question():
    """
    Test the generate_question function to ensure it interacts with OpenAI API correctly.
    """
    try:
        subject = "Python"
        experience = "2-4 years"
        company_type = "Startup"
        
        result = generate_question(subject, experience, company_type)
        assert isinstance(result, dict), "Result should be a dictionary."
        assert "text" in result, "Generated question should have a 'text' field."
        assert "assessment_criteria" in result, "Result should include 'assessment_criteria'."
    except Exception as e:
        pytest.fail(f"generate_question failed with exception: {e}")
