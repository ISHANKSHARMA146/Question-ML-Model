import os
import json
import logging
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)

def generate_question(subject, experience_range, company_type):
    """
    Generate an interview question using OpenAI's GPT-4 API.
    The response is expected to be in a structured JSON format.

    Args:
        subject (str): The subject of the interview question.
        experience_range (str): The candidate's experience level.
        company_type (str): The type of company.

    Returns:
        dict: A dictionary containing the generated question and assessment criteria.
    """
    # Retrieve the OpenAI API key from the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Environment variable OPENAI_API_KEY is not set.")

    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Create a structured prompt for OpenAI
    prompt = f"""
    Create an interview question for the subject '{subject}', tailored for a candidate with 
    {experience_range} years of experience applying to a {company_type}. 

    Provide the response in the following JSON format:
    {{
        "question": "<The interview question>",
        "assessment_criteria": [
            {{
                "category": "<Category Name>",
                "points": [
                    "<Point 1>",
                    "<Point 2>"
                ]
            }}
        ]
    }}
    """

    try:
        # Use the OpenAI client to generate the question
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that generates structured interview questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Adds variability for creativity
            max_tokens=300
        )

        # Extract and parse the JSON response
        raw_content = response.choices[0].message.content.strip()
        logging.debug(f"Raw OpenAI response: {raw_content}")
        parsed_response = json.loads(raw_content)

        # Validate the response structure
        if "question" not in parsed_response or "assessment_criteria" not in parsed_response:
            raise ValueError("Malformed response from OpenAI. Missing 'question' or 'assessment_criteria'.")

        return parsed_response

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response from OpenAI: {str(e)}")
        raise RuntimeError(f"Failed to parse JSON response from OpenAI: {str(e)}")
    except Exception as e:
        logging.error(f"Failed to generate question with OpenAI: {str(e)}")
        raise RuntimeError(f"Failed to generate question with OpenAI: {str(e)}")
