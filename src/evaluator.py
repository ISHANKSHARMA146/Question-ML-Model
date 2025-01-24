import json


def validate_question_schema(question):
    """
    Validates and standardizes a question entry to ensure it adheres to the schema.

    Args:
        question (dict): The question entry to validate.

    Returns:
        dict: A validated and standardized question entry.
    """
    required_keys = {"subject", "tags", "company_type", "experience"}
    if not required_keys.issubset(question.keys()):
        raise ValueError("Question entry is missing required keys.")

    # Ensure tags exist and are a list
    question["tags"] = question.get("tags", [])

    # Ensure experience levels are structured correctly
    if "experience" in question:
        for experience_range, details in question["experience"].items():
            if not isinstance(details, dict) or "question" not in details:
                raise ValueError(f"Malformed experience entry for range: {experience_range}")

            # Assign a default difficulty score if missing
            details["difficulty_score"] = details.get("difficulty_score", None)

    return question


def map_experience_to_difficulty(experience_range):
    """
    Maps experience ranges dynamically to default difficulty scores.

    Args:
        experience_range (str): The experience range (e.g., "2-4 years").

    Returns:
        int: The default difficulty score.
    """
    experience_mapping = {
        "0-1 years": 3,
        "1-2 years": 4,
        "2-4 years": 5,
        "4-8 years": 7,
        "8-12 years": 8,
        "12-20 years": 9,
        "20+ years": 10,
    }
    return experience_mapping.get(experience_range, 5)  # Default to 5 if range is not predefined


def add_assessment_criteria(question_text, subject, company_type):
    """
    Generates assessment criteria for a given question.

    Args:
        question_text (str): The interview question.
        subject (str): The subject of the interview.
        company_type (str): The company type.

    Returns:
        list: A list of assessment criteria dictionaries.
    """
    return [
        {
            "category": "Technical Knowledge",
            "points": [
                f"Demonstrates understanding of {subject} concepts.",
                f"Provides examples relevant to {company_type} challenges."
            ]
        },
        {
            "category": "Problem-Solving Skills",
            "points": [
                "Articulates a clear approach to tackling the question.",
                "Shows critical thinking and adaptability in responses."
            ]
        }
    ]


def evaluate_question(question, experience_range, subject, company_type):
    """
    Enhance the question with additional evaluation details.

    Args:
        question (dict): The question to enhance.
        experience_range (str): The experience range (e.g., "2-4 years").
        subject (str): The subject of the interview.
        company_type (str): The company type.

    Returns:
        dict: An enhanced question with difficulty score and assessment criteria.
    """
    # Assign difficulty score based on experience range
    question["difficulty_score"] = map_experience_to_difficulty(experience_range)

    # Add assessment criteria
    question["assessment_criteria"] = add_assessment_criteria(
        question_text=question.get("question", ""),
        subject=subject,
        company_type=company_type
    )

    return question
