# Project: Question Generator

This project is a Question Generator designed to load data, generate OpenAI-based questions, evaluate the results, and provide a functional application for querying. It is organized into modular components to ensure maintainability and scalability.

## Project Structure

```
Question
├── .git
│   ├── hooks
│   ├── objects
│   ├── refs
│   ├── HEAD
│   ├── config
├── config
│   └── easemyhiring-6e10bde45b86.json
├── data
│   └── questions.json
├── src
│   ├── app.py
│   ├── data_loader.py
│   ├── evaluator.py
│   ├── openai_generator.py
│   └── __pycache__
├── tests
│   ├── test_data_loader.py
│   ├── test_gcp_connection.py
│   ├── test_openai_generator.py
├── .gitignore
├── requirements.txt
```

---

## Setup and Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.10+
- pip (Python package manager)
- Access to OpenAI API
- (Optional) GCP credentials for certain functionalities

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Question
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### OpenAI API Key

Set up your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your_api_key_here'
```

Alternatively, add it to a `.env` file for automatic loading.

### GCP Configuration (Optional)

If you're using GCP services, ensure the appropriate credentials are placed in the `config/` folder.

---

## Components

### 1. `data_loader.py`

This module handles data loading and preprocessing.

- **Input:** JSON file containing questions.
- **Output:** Parsed and preprocessed data ready for further use.

### 2. `openai_generator.py`

This module interacts with the OpenAI API to generate questions based on the input data.

- **Input:** Preprocessed data from `data_loader.py`.
- **Output:** Generated questions.

### 3. `evaluator.py`

Evaluates the quality and correctness of the generated questions.

- **Input:** Generated questions.
- **Output:** Metrics and feedback on the generation.

### 4. `app.py`

The main entry point for the application.

- **Features:**
  - Load data.
  - Generate questions using OpenAI API.
  - Evaluate the generated output.

---

## Usage

1. **Run the application**:

   ```bash
   python src/app.py
   ```

2. **Run tests**:

   ```bash
   pytest tests/
   ```

---

## Tests

The `tests/` folder contains unit tests to ensure the integrity of individual modules:

- `test_data_loader.py`: Validates data loading and preprocessing.
- `test_openai_generator.py`: Tests API integration and response handling.
- `test_gcp_connection.py`: Ensures GCP configurations are loaded correctly (if applicable).

Run tests using:

```bash
pytest
```

---

## Data

The `data/questions.json` file contains sample questions used for generation and evaluation.

---

## Requirements

Dependencies are listed in `requirements.txt`. Some key packages include:

- `openai`: For API interaction.
- `pytest`: For testing.
- `pandas`: For data handling.
- `flask`: For building APIs (if applicable).

---

## Contributing

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-branch
   ```

3. Commit your changes and push the branch.
4. Create a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

