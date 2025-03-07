# Gemini API Hosting Tutorial

This repository contains a FastAPI application that serves as a wrapper for the Google Gemini API, providing endpoints for text processing and food image analysis.

## Features

-   Text generation with custom system prompts using Gemini 2.0 Flash
-   Food image analysis that returns calorie estimates and descriptions
-   RESTful API with JSON responses

## Prerequisites

-   Python 3.8+
-   Google Gemini API key

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/GDGC_api_hosting_tutorial.git
cd GDGC_api_hosting_tutorial
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the API

Start the FastAPI application:

```bash
python main.py
```

The API will be available at http://127.0.0.1:8000

## API Endpoints

### Root Endpoint

-   `GET /`: Welcome message and API information

### Text Generation

-   `POST /api/text`: Generate text responses
    -   Request body:
        ```json
        {
            "text": "Your prompt here",
            "system_prompt": "Optional system prompt"
        }
        ```

### Food Analysis

-   `POST /api/analyze-food`: Analyze food images for calorie content
    -   Request body:
        ```json
        {
            "image": "base64_encoded_image_data"
        }
        ```
    -   Response: JSON object with calorie estimate and description

## Testing

Run the included test script:

```bash
python test.py
```

This will test the main endpoint, text generation, and food analysis functionality.
