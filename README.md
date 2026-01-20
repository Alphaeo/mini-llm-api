# Mini LLM API

This project is a **FastAPI application** that serves as a **mini LLM (Large Language Model) API**. It is designed to be **production-ready**, **Dockerized**, and allows testing locally with a **lightweight Markov chain-based toy LLM**. If a GPU and a real LLM (like vLLM or Mistral) are available, the API can be easily configured to use it instead.

The application provides endpoints for health checks, text generation, and token streaming, demonstrating how a real LLM backend would function.

---

## Features

- **Health Check:** Verify that the API is running at `/health`.
- **Chat Endpoint:** Generate text responses from user prompts at `/chat`.
- **Streaming Endpoint:** Stream generated tokens in real time at `/chat/stream`.
- **Toy Markov Model:** A lightweight, CPU-friendly text generator for testing without GPU.
- **Optional Real LLM Integration:** Can be configured to use vLLM or other models if available.
- **Swagger Documentation:** Auto-generated interactive docs at `/docs`.
- **Pydantic Validation:** Ensures request and response data are properly typed and validated.
- **Dockerized:** Ready to run in a Docker container for consistent environments.

---

## Project Structure

mini-llm-api
├── src
│ ├── main.py # Entry point of the FastAPI application
│ ├── mini_markov_llm.py # Toy Markov LLM implementation for local testing
│ ├── api
│ │ └── endpoints.py # API endpoints (chat, stream, health)
│ ├── core
│ │ └── llm.py # LLM wrapper for vLLM or real models
│ └── types
│ └── schemas.py # Pydantic models for request and response validation
├── tests
│ ├── test_api.py # Unit tests for the API
│ └── init.py # Init file for tests package
├── requirements.txt # Python dependencies
├── Dockerfile # Docker configuration
├── README.md # Project documentation
└── .gitignore # Git ignore file


---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mini-llm-api.git
cd mini-llm-api
2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run the API locally
uvicorn src.main:app --reload
5. Access API documentation
Open your browser at http://127.0.0.1:8000/docs to view and test the endpoints interactively.

##Docker Usage

Build the Docker image

docker build -t mini-llm-api .
Run the container

docker run -p 8000:8000 mini-llm-api
Access API documentation

Open your browser at http://127.0.0.1:8000/docs.

##How the Mini LLM Works

1. Toy Markov Model (Default)
A lightweight Markov chain generates words sequentially based on a small example corpus.

CPU-friendly: does not require GPU or large models.

Supports token-by-token streaming for /chat/stream.

Used for testing and demonstration, simulating the behavior of a real LLM.

2. Real LLM (Optional)
If you have access to a GPU and a model such as vLLM or Mistral, you can replace the toy model in core/llm.py.

The API interface (/chat and /chat/stream) remains exactly the same, making it easy to swap the backend without modifying the front-end or endpoints.

##API Endpoints

/health — GET
Check if the API is running.

Response:

{
  "status": "healthy"
}
/chat — POST
Generate a full text response.

Request Example:

{
  "prompt": "Hello world",
  "temperature": 0.7,
  "max_tokens": 20
}
Response Example:

{
  "response": "Hello world this is a test hello AI world"
}
/chat/stream — POST
Stream generated tokens one by one.

Request Example:

{
  "prompt": "Hello world",
  "temperature": 0.7,
  "max_tokens": 20
}
Behavior:

Returns a streaming response (token by token) in plain text.

Front-end can display it progressively, simulating real-time LLM behavior.

##Testing the Application

1. Manual Testing
Open /docs in your browser.

Use the interactive Swagger interface to call /chat or /chat/stream.

Observe responses from the toy Markov model.

2. Automated Testing
Run unit tests with pytest:

pytest tests/
Tests verify:

Endpoints respond correctly

Streaming endpoint returns data progressively

Input validation with Pydantic

##Summary:

The app is production-ready and Dockerized, with clear separation of backend logic and model.

Uses a toy Markov model for testing, fully compatible with real LLMs.
