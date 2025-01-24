import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from data_loader import load_questions

if __name__ == "__main__":
    try:
        questions = load_questions()
        print("Questions loaded successfully:")
        print(questions)
    except Exception as e:
        print(f"Error: {e}")
