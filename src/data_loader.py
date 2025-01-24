import os
import json
from google.cloud import storage
from rapidfuzz import fuzz

def load_questions_from_gcp():
    """
    Load the questions file from the GCP bucket specified in environment variables.

    Returns:
        list: A list of questions loaded from the JSON file in the GCP bucket.
    """
    try:
        # Initialize GCP Storage Client
        client = storage.Client.from_service_account_json(os.getenv("GCP_SERVICE_ACCOUNT_KEY"))
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        file_name = os.getenv("GCP_FILE_NAME")

        if not bucket_name or not file_name:
            raise ValueError("Environment variables GCP_BUCKET_NAME and GCP_FILE_NAME must be set.")

        # Retrieve the bucket and file
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_text()

        return json.loads(content)

    except Exception as e:
        raise RuntimeError(f"Failed to load questions from GCP: {str(e)}")


def fetch_questions_by_criteria(subject, experience_range, company_type):
    """
    Fetch questions matching the input criteria from the loaded questions.

    Args:
        subject (str): The subject of the interview question.
        experience_range (str): The candidate's experience level.
        company_type (str): The type of company.

    Returns:
        list: A list of matching questions or an empty list if none match.
    """
    try:
        questions = load_questions_from_gcp()
        matching_questions = []

        for question in questions:
            # Check subject similarity using fuzzy matching
            subject_similarity = fuzz.partial_ratio(subject.lower(), question["subject"].lower())
            if (
                subject_similarity >= 80
                and question["company_type"].lower() == company_type.lower()
                and experience_range in question["experience"]
            ):
                matching_questions.append({
                    "question": question["experience"][experience_range]["question"],
                    "difficulty_score": question["experience"][experience_range]["difficulty_score"],
                    "assessment_criteria": []  # Placeholder for additional assessment criteria
                })

        return matching_questions

    except Exception as e:
        raise RuntimeError(f"Error fetching questions by criteria: {str(e)}")


def append_generated_question_to_gcp(subject, tags, company_type, experience_range, generated_question):
    """
    Append a newly generated question to the GCP bucket.

    Args:
        subject (str): The subject of the question.
        tags (list): Tags associated with the question.
        company_type (str): The type of company.
        experience_range (str): The candidate's experience level.
        generated_question (dict): The generated question with metadata.
    """
    try:
        # Load existing questions
        questions = load_questions_from_gcp()

        # Check if a similar question already exists
        for question in questions:
            if (
                fuzz.partial_ratio(subject.lower(), question["subject"].lower()) >= 80
                and question["company_type"].lower() == company_type.lower()
                and experience_range in question["experience"]
            ):
                raise ValueError("A similar question already exists in the database.")

        # Create a new entry or update the existing subject entry
        new_entry = None
        for question in questions:
            if fuzz.partial_ratio(subject.lower(), question["subject"].lower()) >= 80:
                # Update existing entry
                question["experience"][experience_range] = {
                    "question": generated_question["question"],
                    "difficulty_score": generated_question.get("difficulty_score")
                }
                new_entry = question
                break

        if not new_entry:
            # Create a new entry if no matching subject is found
            new_entry = {
                "subject": subject,
                "tags": tags,
                "company_type": company_type,
                "experience": {
                    experience_range: {
                        "question": generated_question["question"],
                        "difficulty_score": generated_question.get("difficulty_score")
                    }
                }
            }
            questions.append(new_entry)

        # Save updated questions back to GCP
        save_questions_to_gcp(questions)

    except Exception as e:
        raise RuntimeError(f"Failed to append generated question to GCP: {str(e)}")


def save_questions_to_gcp(questions):
    """
    Save the updated questions list back to the GCP bucket.

    Args:
        questions (list): The list of questions to save.
    """
    try:
        # Initialize GCP Storage Client
        client = storage.Client.from_service_account_json(os.getenv("GCP_SERVICE_ACCOUNT_KEY"))
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        file_name = os.getenv("GCP_FILE_NAME")

        if not bucket_name or not file_name:
            raise ValueError("Environment variables GCP_BUCKET_NAME and GCP_FILE_NAME must be set.")

        # Retrieve the bucket and upload the file
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(questions, indent=4))

    except Exception as e:
        raise RuntimeError(f"Failed to save questions to GCP: {str(e)}")
