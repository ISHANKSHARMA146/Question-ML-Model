import logging
from flask import Flask, request, jsonify
from src.data_loader import fetch_questions_by_criteria, append_generated_question_to_gcp
from src.openai_generator import generate_question
from src.evaluator import evaluate_question

# Initialize Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/questions', methods=['POST'])
def get_questions():
    """
    Main endpoint to fetch or generate questions based on the input criteria.
    """
    try:
        # Parse input JSON
        data = request.get_json()
        subject = data.get("subject")
        experience_range = data.get("experience")
        company_type = data.get("company_type")
        tags = data.get("tags", [])  # Optional tags

        if not subject or not experience_range or not company_type:
            return jsonify({"error": "Missing required fields: subject, experience, or company_type"}), 400

        logging.info(f"Fetching questions for Subject: {subject}, Experience: {experience_range}, Company Type: {company_type}")

        # Fetch pre-trained questions from GCP bucket
        pre_trained_questions = fetch_questions_by_criteria(subject, experience_range, company_type)

        if pre_trained_questions:
            logging.info("Returning pre-trained questions.")
            return jsonify(pre_trained_questions), 200

        logging.info("No pre-trained questions found. Generating dynamically...")

        # Generate a new question using OpenAI
        generated_question = generate_question(subject, experience_range, company_type)
        if not generated_question:
            return jsonify({"error": "Failed to generate a question dynamically."}), 500

        # Enhance the generated question with assessment criteria and difficulty score
        enhanced_question = evaluate_question(
            question=generated_question,
            experience_range=experience_range,
            subject=subject,
            company_type=company_type
        )

        # Append the new question to GCP
        append_generated_question_to_gcp(
            subject=subject,
            tags=tags,
            company_type=company_type,
            experience_range=experience_range,
            generated_question=enhanced_question
        )

        logging.info("New question generated and appended to GCP.")
        return jsonify([enhanced_question]), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
